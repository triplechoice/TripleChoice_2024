import json
import os
import random
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authentication.mixins import PermissionMixin
from order.filters.request import SupplierReviewRequestFilter, ModeratorReviewRequestFilter
from order.forms.review_form import RequestReviewForm
from order.models.order import OrderInfo
from order.models.request import Request, RequestReview, RequstReviewAttachment, SelectedRequestReview
from order.forms.request_estimation_form import RequestEstimation
from rest_framework.views import APIView

from order.paginations import RequestPagination
from order.serealizer.request import GetRequestInfoSerializer, GetRequestReviewSerializer, \
    SupplierRequestReviewSerializer
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import transaction
from order.serealizer.order import OrderSerializer, BillingAddressSerializer, ShippingAddressSerializer

error_messages = {}


def addAttachmentsToReview(files, review, type):
    for file in files:
        if not file.name.endswith(type):
            error_messages['error'] = 'File field is required'
            raise ValidationError({'file': "Only Pdf file is allowed"})
        file_size = int(os.environ.get('MAX_FILE_SIZE_IN_MB', '20'))
        if float(file.size / 1048576) > file_size:
            error_messages['error'] = f"File size should be less than {file_size} MB"
            raise ValidationError({'file': "File size can't be more than 20 MB"})
        request_review_attachment = RequstReviewAttachment(file=file, request_review=review)
        request_review_attachment.save()


class RequestReviewCreateView(PermissionMixin, View):
    permission_required = ('order.add_requestreview',)

    def get(self, request, request_id, *args, **kwargs):
        form = RequestReviewForm(initial={'request': request_id, 'user': request.user})
        context = {"order_id": request_id, 'form': form}
        return render(request, 'reviews/create.html', context)

    def post(self, request, request_id):
        form = RequestReviewForm(request.POST, request.FILES)
        files = request.FILES

        if len(files) <= 0:
            messages.error(request, "File field is required", extra_tags='error')
            return render(request, 'reviews/create.html', {'form': form})

        if form.is_valid():

            try:
                with transaction.atomic():
                    review = form.save()
                    review.user = request.user
                    review.save()

                    addAttachmentsToReview(files.getlist('attachment'), review, ".pdf")
                    request_obj = Request.objects.filter(id=request_id).first()
                    if request_obj:
                        request_obj.admin_status = 'received_results_from_supplier'
                        request_obj.moderator_status = 'new_review'
                        request_obj.customer_status = 'in_review'
                        request_obj.supplier_status = 'submitted'
                        request_obj.save()

            except ValidationError as e:
                messages.error(request, error_messages.get('error'), extra_tags='error')
                return render(request, 'reviews/create.html', {'form': form})

            messages.success(request, 'Data store successfully', extra_tags='success')
            return redirect(
                reverse('order:request.review', args=(request_id,)))

        return render(request, 'reviews/create.html', {'form': form})


class SupplierReviewView(ModelViewSet):
    serializer_class = SupplierRequestReviewSerializer
    queryset = RequestReview.objects.all()
    pagination_class = RequestPagination
    filterset_class = SupplierReviewRequestFilter

    def get_queryset(self):
        order_by = '-id'
        if self.request.GET.get('order_by'):
            order_by = self.request.GET.get('order_by').lower()
        return RequestReview.objects.filter(request=self.request.query_params.get('request_id'),
                                            user=self.request.user).order_by(order_by)


class ModeratorReviewView(ModelViewSet):
    serializer_class = SupplierRequestReviewSerializer
    queryset = RequestReview.objects.all()
    pagination_class = RequestPagination
    filterset_class = ModeratorReviewRequestFilter

    def get_queryset(self):
        # self.pagination_class.page_size = self.request.GET.get('page_num')
        order_by = '-id'
        if self.request.GET.get('order_by'):
            order_by = self.request.GET.get('order_by').lower()
        return RequestReview.objects.filter(request=self.request.query_params.get('request_id')).order_by(order_by)


class RequestReviewView(PermissionMixin, View):
    permission_required = ('order.view_requestreview',)

    def get(self, request, request_id, *args, **kwargs):
        request_info = Request.objects.get(id=request_id)
        context = {'request_id': request_id, "request_info": request_info}
        return render(request, 'reviews/index.html', context)


class RequestReviewEditView(PermissionMixin, View):
    permission_required = ('order.change_requestreview',)

    def get(self, request, pk):
        review = RequestReview.objects.get(id=pk)
        form = RequestReviewForm(instance=review)

        context = {'form': form,
                   'review': review,
                   'view': "edit"
                   }
        return render(request, 'reviews/create.html', context)

    def post(self, request, pk):
        review = RequestReview.objects.get(id=pk)
        form = RequestReviewForm(request.POST, instance=review)
        files = request.FILES

        if form.is_valid():

            try:
                with transaction.atomic():
                    form.save()

                    addAttachmentsToReview(files.getlist('attachment'), review, ".pdf")

            except ValidationError:
                messages.error(request, error_messages.get('error'), extra_tags='error')
                return render(request, 'reviews/create.html', {'form': form, 'review': review, 'view': "edit"})

            messages.success(request, 'Data update successfully', extra_tags='success')
            return redirect(reverse('order:request.review', args=(request.POST.get('request'),)))
        return render(request, 'reviews/create.html', {'form': form, 'review': review, 'view': "edit"})


class RequestReviewDeleteView(View):
    permission_required = ('order.delete_requestreview',)

    def get(self, request, pk):
        review = RequestReview.objects.get(id=pk)
        review.is_deleted = True
        review.save()

        messages.success(request, 'Data deleted successfully', extra_tags='success')
        return redirect(request.META.get('HTTP_REFERER'))


class RequestReviewAttachmentDelete(View):

    def get(self, request, pk):
        req_id = ""
        review_attachmet = RequstReviewAttachment.objects.filter(pk=pk).first()
        if review_attachmet:
            req_id = review_attachmet.request_review.request.id
            review_attachmet.delete()
        return redirect('order:request.review', request_id=req_id)


class RequestEstimationView(View):
    def get(self, request, pk):
        request_obj = Request.objects.get(id=pk)
        form = RequestEstimation(instance=request_obj)
        context = {
            "form": form,
            "request_obj": request_obj
        }
        return render(request, 'request_estimation_page.html', context)

    def post(self, request, pk):
        request_obj = Request.objects.get(id=pk)
        form = RequestEstimation(request.POST, instance=request_obj)
        if form.is_valid():
            form.save()
            request_obj.is_estimated = True
            request_obj.save()
            return redirect('/super-admin/order/request/')
        return redirect('order:request.estimation')


class GetQuoteView(PermissionMixin, View):
    permission_required = ('order.add_request',)

    def post(self, request, pk, review_id):
        request_object = Request.objects.get(id=pk)
        order_id = request_object.order_id
        request_object.pk = None
        request_object.order_id = random.randrange(1000, 1000000000)
        request_object.type = 'quote'
        request_object.admin_status = 'pending'
        request_object.customer_status = 'submitted'
        request_object.moderator_status = None
        request_object.supplier_status = None
        request_object.ref_request = order_id
        request_object.is_estimated = False
        request_object.review_id = review_id

        prev_req = Request.objects.get(order_id=order_id)
        prev_req.admin_status = "completed"
        prev_req.customer_status = "query_submitted"
        prev_req.supplier_status = "query_submitted"
        prev_req.moderator_status = "query_submitted"
        prev_req.save()
        request_object.save()

        return redirect('customer:customer_requests')


class RequestOrderView(PermissionMixin, View):
    permission_required = ('order.add_orderinfo',)

    def get(self, request, pk, review_id=None):

        if not Request.objects.filter(id=pk, user=request.user).exists():
            raise PermissionDenied

        if OrderInfo.objects.filter(review_id=review_id, request_id=pk).exists():
            messages.error(request, "You already ordered using this review", extra_tags='error')
            return render(request, 'customer/reviews/index.html', context={'request_id': pk})

        if review_id == 0:
            review_id = None
        context = {
            'request_id': pk,
            'review_id': review_id
        }
        return render(request, 'request_order/request_order_page.html', context)


class GetRequestInfo(APIView):
    def get(self, request, pk):
        request_obj = Request.objects.get(id=pk)
        serializer = GetRequestInfoSerializer(request_obj)
        return Response(serializer.data)


class GetReviewInfo(APIView):
    def get(self, request, pk):
        review_obj = RequestReview.objects.filter(id=pk).first()
        serializer = GetRequestReviewSerializer(review_obj)
        return Response(serializer.data)


class CheckOutView(PermissionMixin, APIView):
    permission_required = ('order.add_orderinfo',)

    def get(self, request):
        if not Request.objects.filter(id=request.GET.get('request_id'), user=request.user).exists():
            raise PermissionDenied

        if OrderInfo.objects.filter(review_id=request.GET.get('review_id'),
                                    request_id=request.GET.get('request_id')).exists():
            messages.error(request, "You already ordered using this review", extra_tags='error')
            return render(request, 'customer/reviews/index.html', context={'request_id': request.GET.get('request_id')})

        context = {
            "request_id": request.GET.get('request_id', None),
            "quantity": request.GET.get('quantity', None),
            "review_id": request.GET.get('review_id', None),
            "user_id": request.user.id,
            'stripe_pk': os.environ.get('STRIPE_PUBLISH_KEY')
        }
        return render(request, 'checkout/checkout_page.html', context)


class OrderDetailsView(PermissionMixin, View):
    permission_required = ('order.view_orderinfo',)

    def get(self, request, pk):
        order = OrderInfo.objects.filter(id=pk, user=request.user).first()
        if order is None:
            raise PermissionDenied
        context = {
            'order': order,
        }
        return render(request, 'customer/order/order-details.html', context)


class OrderUpdateView(PermissionMixin, View):
    permission_required = ('order.change_orderinfo',)

    def get(self, request, pk):
        order = OrderInfo.objects.filter(id=pk).first()
        context = {
            'order_id': order.id,
            'user_id': request.user.id
        }
        return render(request, 'customer/order/order-update.html', context)


class RequestReviewSelectView(PermissionMixin, APIView):
    permission_required = ('order.add_selectedrequestreview',)

    def post(self, request):
        reviews_id = request.data.get('form').replace('"', "")[1:-1].split(',')
        request_id = request.data.get('request_id')
        obj = SelectedRequestReview.objects.filter(request_id=request_id).first()

        request_obj = Request.objects.get(id=request_id)

        if not obj:
            obj = SelectedRequestReview.objects.create(request_id=request_id)
            obj.save()
        if '' not in reviews_id:
            obj.review.set(RequestReview.objects.filter(id__in=reviews_id))
        else:
            obj.review.clear()
        if obj.review.all().count() > 0:
            request_obj.admin_status = 'completed'
            request_obj.moderator_status = 'completed'
            request_obj.customer_status = 'results'
            request.supplier_status = 'submitted'
        else:
            request_obj.admin_status = 'received_results_from_supplier'
            request_obj.moderator_status = 'new_review'
            request_obj.customer_status = 'in_review'
            request.supplier_status = 'submitted'
        request_obj.save()
        return redirect(f'/request/{request_id}/review')


# request submit helper view
def request_submit_helper(request):
    return render(request, 'request_submit_helper/index.html')
