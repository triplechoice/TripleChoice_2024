import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from order.models.request import Request, RequestReview, SelectedRequestReview, RequestHistory
from django.views import View
from authentication.mixins import PermissionMixin
from product.apis.product import HomePageView
from product.models.product_models import Part
from order.models.order import OrderInfo, OrderInfoHistory
from django.core.exceptions import PermissionDenied


class DashboardView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        requests = Request.objects.filter(user=request.user)
        orders = OrderInfo.objects.filter(user=request.user)
        request_info = {
            'total': requests.count(),
            'submitted': requests.filter(customer_status='submitted').count(),
            'processing': requests.filter(customer_status='processing').count(),
            'in_review': requests.filter(customer_status='in_review').count(),
            'results': requests.filter(customer_status='results').count(),
            'cancelled': requests.filter(customer_status='cancelled').count()
        }

        order_info = {
            'total': orders.count(),
            'received': orders.filter(status='received').count(),
            'processing': orders.filter(status='processing').count(),
            'processed': orders.filter(status='processed').count(),
            'delivered': orders.filter(status='delivered').count(),
            'returned': orders.filter(status='returned').count(),
            'canceled': orders.filter(status='canceled').count()
        }

        context = {
            'request_info': request_info,
            'order_info': order_info
        }
        return render(request, 'customer/dashboard.html', context)


class RequestsView(PermissionMixin, View):
    permission_required = ('order.view_request',)

    def get(self, request):
        return render(request, 'customer/requests.html')


class RequestDetailsView(PermissionMixin, View):
    permission_required = ('order.view_request',)

    def get(self, request, order_id):
        order = Request.objects.filter(order_id=order_id, user=request.user).first()
        if order:
            context = {"order": order}
            return render(request, 'customer/request-details.html', context)
        raise PermissionDenied


class RequestReviewView(PermissionMixin, View):
    permission_required = ('order.view_requestreview',)

    def get(self, request, request_id, *args, **kwargs):
        reviews = RequestReview.all_objects.filter(selectedrequestreview__request=request_id,
                                                   request__user=request.user)
        request_info = Request.objects.filter(id=request_id).first()
        # context = {"reviews": reviews, 'request_id': request_id, 'request_info': request_info}
        context = {
            "request_id": request_id
        }
        return render(request, 'customer/reviews/index.html', context)


class RequestsHistoryView(PermissionMixin, View):
    permission_required = ('order.view_request',)

    def get(self, request, order_id):
        order = RequestHistory.objects.filter(order_id=order_id).first()
        if order:
            if not RequestHistory.objects.filter(order_id=order_id, user=request.user).exists():
                raise PermissionDenied
        context = {
            "order_id": order_id
        }
        return render(request, 'customer/requests-history.html', context)


class RequestHisoryDetailsView(PermissionMixin, View):
    permission_required = ('order.view_request',)

    def get(self, request, id):
        order = RequestHistory.objects.filter(id=id, user=request.user).first()
        if order:
            context = {"order": order}
            return render(request, 'customer/request-details.html', context)
        raise PermissionDenied


class OrdersView(PermissionMixin, View):
    permission_required = ('order.view_orderinfo',)

    def get(self, request):
        orders = OrderInfo.objects.filter(user=request.user).order_by('-id')
        paginator = Paginator(orders, 10)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        orders = paginator.get_page(page_number)
        context = {
            'orders': orders
        }
        return render(request, 'customer/order/orders.html', context)


class OrdersHistoryView(PermissionMixin, View):
    permission_required = ('order.view_orderinfo',)

    def get(self, request, order_id):
        orders = OrderInfoHistory.objects.filter(order_id=order_id)
        paginator = Paginator(orders, 10)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        orders = paginator.get_page(page_number)
        context = {
            'orders': orders
        }
        context['title'] = 'Request List'

        return render(request, 'customer/order/order-history.html', context)


class OrdersHistoryDetailsView(PermissionMixin, View):
    permission_required = ('order.view_orderinfo',)

    def get(self, request, pk):
        order = OrderInfoHistory.objects.filter(id=pk).first()
        context = {
            'order': order,
        }
        return render(request, 'customer/order/order-details.html', context)
