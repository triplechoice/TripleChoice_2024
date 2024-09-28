from django.urls import path, include
from supplier import views
from supplier.views import ModeratorRequestReviewList
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# Assign unique basenames to prevent conflicts
router.register("api/supplier-requests", views.RequestReviewApiView, basename='supplier_requests')
router.register("api/moderator-requests", views.ModeratorRequestApiView, basename='moderator_requests')

app_name = "supplier"

urlpatterns = [
    path("requests", views.SupplierRequestView.as_view(), name="supplier_requests"),
    path('moderator-requests/', views.ModeratorRequestView.as_view(), name='moderator_request'),
    path('moderator-request/<int:request_id>/review', ModeratorRequestReviewList.as_view(),
         name='moderator.request.review'),
    path('request-details/<str:order_id>', views.SupplierRequestDetailsView.as_view(), name="supplier_request_details"),
    path('moderator/request-details/<str:order_id>', views.ModeratorRequestDetailsView.as_view(),
         name="moderator_request_details"),

    path('', include(router.urls))
]
