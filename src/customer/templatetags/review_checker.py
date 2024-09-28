from django import template
from order.models.request import Request

register = template.Library()


@register.filter(name='check_review')
def check_review(request_id, review_id):
    request_object = Request.objects.filter(id=request_id).first()
    if request_object:
        obj = Request.objects.filter(ref_request=request_object.order_id).first()
        if obj:
            if obj.review_id == review_id:
                return False
    return True
