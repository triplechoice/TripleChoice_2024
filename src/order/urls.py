from django.urls import path, include
from rest_framework.routers import DefaultRouter

from order.apis.order import (
    RequestView, CheckDisposableEmail, RequestPartView, RequestDeleteView,
    ApiRequestReviewView, ApiRequestReviewCreateView, OrderView, OrderDeleteView,
    GetOrderView, StripCheck, PumpDataView, OrderPumpMatchView, PumpMatchInputAPIView
)
from order.apis.request import (
    GetReviewIds, GetSelectedReview, SetSelectedReview, GetReviewIdInOrderInfo
)
from order.views import (
    RequestReviewCreateView, RequestReviewView, RequestReviewEditView, 
    RequestReviewDeleteView, RequestReviewAttachmentDelete, RequestEstimationView, 
    GetQuoteView, RequestOrderView, GetRequestInfo, CheckOutView, 
    OrderDetailsView, OrderUpdateView, RequestReviewSelectView, 
    GetReviewInfo, SupplierReviewView, ModeratorReviewView, request_submit_helper
)
from product.apis.product import PartView

router = DefaultRouter()
router.register(r'api/order', OrderView, basename='order')
router.register(r'api/supplier/review', SupplierReviewView, basename='supplier_review')
router.register(r'api/moderator/review', ModeratorReviewView, basename='moderator_review')  # Unique basename

app_name = 'order'
urlpatterns = [
    path('part/<slug:slug>/request/<int:order_id>/update/', PartView.as_view(), name="request.part.update"),
    path('request/delete/<int:pk>', RequestDeleteView.as_view(), name="request.delete"),
    path('request/<int:request_id>/review', RequestReviewView.as_view(), name="request.review"),
    path('request/<int:request_id>/review/create', RequestReviewCreateView.as_view(), name="request.review.create"),
    path('request/review/<int:pk>/edit', RequestReviewEditView.as_view(), name="request.review.edit"),
    path('api/request/review/select', RequestReviewSelectView.as_view(), name='request.review.select'),
    path('request/review/<int:pk>/delete', RequestReviewDeleteView.as_view(), name="request.review.delete"),
    path('request/review_attachment/<int:pk>/delete', RequestReviewAttachmentDelete.as_view(),
         name="request.review_attachment.delete"),
    path('request/<int:pk>/estimation/', RequestEstimationView.as_view(), name='request.estimation'),
    path('request/<int:pk>/get_quote/<int:review_id>', GetQuoteView.as_view(), name='get_quote'),
    path('request/<int:pk>/order_now/<int:review_id>', RequestOrderView.as_view(), name='request_order'),

    # API endpoints
    # path('api/pump-data/', PumpDataView.as_view(), name='pump-data'),
    path('api/pump-match-input/', PumpMatchInputAPIView.as_view(), name='pump-match'),
    path('api/pump-data/', OrderPumpMatchView.as_view(), name='pump-data'),
    path('api/get_request/<int:pk>', GetRequestInfo.as_view(), name='get_request_info'),
    path('api/get_review/<int:pk>', GetReviewInfo.as_view(), name='get_review_info'),
    path('api/request/', RequestView.as_view()),
    path('api/request/update/<int:pk>', RequestView.as_view()),
    path('api/request/part/<int:pk>', RequestPartView.as_view()),
    path('api/disposable-email/', CheckDisposableEmail.as_view()),

    path('api/request_reviews/<int:request_id>', ApiRequestReviewView.as_view(), name="api.request.review"),
    path('api/request_reviews_create/', ApiRequestReviewCreateView.as_view(), name='api.request.review.create'),

    path('request-checkout/', CheckOutView.as_view(), name='checkout'),

    path('order-details/<int:pk>', OrderDetailsView.as_view(), name='order_detail'),
    path('order/delete/<int:pk>', OrderDeleteView.as_view(), name='order_delete'),
    path('order/<int:pk>/update', OrderUpdateView.as_view(), name='order_update'),
    path('api/order-info/<int:order_id>', GetOrderView.as_view()),
    path('api/get-review-ids/<int:request_id>', GetReviewIds.as_view(), name='get_review_ids'),
    path('api/get-order-ids/<int:request_id>', GetReviewIdInOrderInfo.as_view()),
    path('api/get-selected-review/<int:request_id>', GetSelectedReview.as_view()),
    path('api/selected-review-id/', SetSelectedReview.as_view()),

    # Stripe payment
    path('v1/payment_intents', StripCheck.as_view(), name='checkout'),

    # Request submit helper
    path('request/submit/helper', request_submit_helper, name='request_submit_helper'),
]

urlpatterns += router.urls
