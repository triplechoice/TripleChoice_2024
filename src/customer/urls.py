from django.urls import path, include

from customer.views import DashboardView, RequestsView, RequestDetailsView, RequestReviewView, RequestsHistoryView, \
    RequestHisoryDetailsView, OrdersView, OrdersHistoryView, OrdersHistoryDetailsView

from customer.api_views import CustomerRequestView, CustomerOrderView, RequestHistoryApiView, RequestReviewApiView, \
    RequestCancelView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/customer-request', CustomerRequestView)
router.register(r'api/customer-order', CustomerOrderView)
router.register(r'api/customer-request-history', RequestHistoryApiView)
router.register(r'api/customer-request-review', RequestReviewApiView)

app_name = 'customer'

urlpatterns = [
    path('profile/', DashboardView.as_view(), name="customer_dashboard"),
    path('requests/', RequestsView.as_view(), name="customer_requests"),
    path('request-details/<str:order_id>', RequestDetailsView.as_view(), name="customer_request_details"),
    path('request/<int:request_id>/review', RequestReviewView.as_view(), name="request.review"),
    path('requests-history/<str:order_id>', RequestsHistoryView.as_view(), name="customer_requests_history"),
    path('request-history-details/<str:id>', RequestHisoryDetailsView.as_view(),
         name="customer_request_history_details"),

    path('orders/', OrdersView.as_view(), name='customer_orders'),
    path('order-history/<str:order_id>', OrdersHistoryView.as_view(), name='order_history'),
    path('order-history-details/<int:pk>', OrdersHistoryDetailsView.as_view(), name='order_history_details')
]

# api urls
urlpatterns += [
    path('', include(router.urls)),
    path('api/requests-cancel/<int:pk>', RequestCancelView.as_view())
]
