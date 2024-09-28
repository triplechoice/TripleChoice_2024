import json

from django.core.paginator import Paginator
from django.shortcuts import render
from order.filters.request import RequestFilter, ModeratorRequestFilter
from order.models.request import Request, RequestReview, SelectedRequestReview
from django.views import View
from authentication.mixins import PermissionMixin
from rest_framework.viewsets import ModelViewSet

from order.paginations import RequestPagination
from order.serealizer.request import ModeratorRequestApiSerializer, SupplierRequestApiSerializer


class SupplierRequestView(PermissionMixin, View):
    permission_required = ('order.view_request',)

    def get(self, request, *arge, **kwargs):
        requests = Request.objects.filter(part__partsupplier__supplier__pk=request.user.id).exclude(
            supplier_status="pending").exclude(user_id=request.user.id).order_by('-id')
        paginator = Paginator(requests, 10)
        page_number = request.GET.get('page')
        requests = paginator.get_page(page_number)
        can_add = False
        if request.user.groups.filter(name='supplier').exists():
            can_add = True
        context = {
            "actions": {'details': "/supplier/request-details/order_id",
                        'add': "/request/id/review/create",
                        'list': "/request/id/review"}
        }
        return render(request, 'supplier/requests.html', context)


class SupplierRequestDetailsView(PermissionMixin, View):
    permission_required = ('order.view_request',)

    def get(self, request, order_id):
        order = Request.objects.filter(order_id=order_id).first()
        context = {"order": order}
        return render(request, 'supplier/request-details.html', context)


class ModeratorRequestDetailsView(PermissionMixin, View):
    permission_required = ('order.view_request',)

    def get(self, request, order_id):
        order = Request.objects.filter(order_id=order_id).first()
        context = {"order": order}
        return render(request, 'moderator/request-details.html', context)


class ModeratorRequestView(PermissionMixin, View):
    permission_required = ('order.view_request',)

    def get(self, request, *arge, **kwargs):
        requests = Request.objects.all().order_by('-id')
        paginator = Paginator(requests, 10)
        page_number = request.GET.get('page')
        requests = paginator.get_page(page_number)
        context = {
            "requests": requests,
        }
        return render(request, 'moderator/requests.html', context)


class ModeratorRequestReviewList(PermissionMixin, View):
    permission_required = ('order.view_requestreview',)

    def get(self, request, request_id, *args, **kwargs):
        # reviews = RequestReview.objects.filter(request=request_id)
        # selected_review = SelectedRequestReview.objects.filter(request_id=request_id).first()
        # selected_reviews_ids = []
        # if selected_review:
        #     selected_reviews = selected_review.review.all().values("id", "title")
        #     for sele_re in selected_reviews:
        #         selected_reviews_ids.append(str(sele_re['id']))
        request_info = Request.objects.get(id=request_id)
        # paginator = Paginator(reviews, 10)  # Show 10 contacts per page.
        # page_number = request.GET.get('page')
        # reviews = paginator.get_page(page_number)
        # context = {"reviews": reviews, 'request_id': request_id, "request_info": request_info,
        #            "selected_reviews": json.dumps(selected_reviews_ids)}
        context = {'request_id': request_id, "request_info": request_info}
        return render(request, 'moderator/moderator_requests.html', context)


class RequestReviewApiView(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = SupplierRequestApiSerializer
    pagination_class = RequestPagination
    filterset_class = RequestFilter
    http_method_names = ['get']

    def get_queryset(self):
        order_by = '-id'
        if self.request.GET.get('order_by'):
            order_by = self.request.GET.get('order_by').lower()
            if 'request' in order_by:
                order_by = order_by.replace('request', 'order_id')
            if 'date' in order_by:
                order_by = order_by.replace('date', 'updated_at')
            if 'status' in order_by.lower():
                order_by = order_by.replace('status', 'supplier_status')
        return Request.objects.filter(part__partsupplier__supplier__pk=self.request.user.id).exclude(
            supplier_status=None).exclude(supplier_status="").exclude(user_id=self.request.user.id).order_by(
            order_by)


class ModeratorRequestApiView(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = ModeratorRequestApiSerializer
    pagination_class = RequestPagination
    filterset_class = ModeratorRequestFilter
    http_method_names = ['get']

    def get_queryset(self):
        order_by = '-id'
        if self.request.GET.get('order_by'):
            order_by = self.request.GET.get('order_by').lower()
            if 'request' in order_by:
                order_by = order_by.replace('request', 'order_id')
            if 'date' in order_by:
                order_by = order_by.replace('date', 'updated_at')
            if 'status' in order_by.lower():
                order_by = order_by.replace('status', 'moderator_status')
        return Request.objects.exclude(user_id=self.request.user.id).order_by(
            order_by)
