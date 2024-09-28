from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models.order import OrderInfo
from order.models.request import Request, SelectedRequestReview, RequestReview


class GetReviewIds(APIView):
    def get(self, request, request_id):
        review_ids = []
        request_object = Request.objects.filter(id=request_id).first()
        if request_object:
            objs = Request.objects.filter(ref_request=request_object.order_id)
            for obj in objs:
                review_ids.append(obj.review_id)
        return Response(review_ids)


class GetSelectedReview(APIView):

    def get(self, request, request_id):
        selected_review = SelectedRequestReview.objects.filter(request_id=request_id).first()
        selected_reviews_ids = []
        if selected_review:
            selected_reviews = selected_review.review.all().values("id")
            for sele_re in selected_reviews:
                selected_reviews_ids.append(sele_re['id'])

        return Response(selected_reviews_ids)


class SetSelectedReview(APIView):
    def post(self, request):
        selected_review = SelectedRequestReview.objects.filter(request_id=request.data.get('request_id')).first()
        if selected_review is None:
            selected_review = SelectedRequestReview.objects.create(request_id=request.data.get('request_id'))
            selected_review.save()
        selected_reviews_ids = []
        if selected_review:
            selected_reviews = selected_review.review.all().values("id")
            for sele_re in selected_reviews:
                selected_reviews_ids.append(sele_re['id'])
            # for review_id in request.data.get('review_ids'):
            #     if review_id in selected_reviews_ids:
            #         selected_reviews_ids.remove(review_id)
            #     else:
            #         selected_reviews_ids.append(review_id)
            if int(request.data.get('id')) in selected_reviews_ids:
                selected_reviews_ids.remove(int(request.data.get('id')))
            else:
                selected_reviews_ids.append(int(request.data.get('id')))
            selected_review.review.set(RequestReview.objects.filter(id__in=selected_reviews_ids))
            request_obj = Request.objects.filter(id=request.data.get('request_id')).first()
            if selected_review.review.all().count() > 0:
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
            return Response("success", status=status.HTTP_200_OK)
        return Response("error", status=status.HTTP_400_BAD_REQUEST)


class GetReviewIdInOrderInfo(APIView):
    def get(self, request, request_id):
        orders = OrderInfo.objects.filter(request_id=request_id)
        review_ids = []
        for obj in orders:
            review_ids.append(obj.review_id)

        return Response(review_ids, status=status.HTTP_200_OK)
