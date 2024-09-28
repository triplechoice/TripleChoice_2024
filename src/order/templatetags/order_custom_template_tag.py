from django import template
import ast
from order.models.request import Request

register = template.Library()


@register.simple_tag
def create_dict(str_dict):
    return ast.literal_eval(str_dict)


@register.filter(name='get_dict_item')
def get_dict_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name="disable_based_on_status")
def disable_based_on_status(status):
    if status != "pending":
        return "btn disabled"
    return ""


@register.filter(name="disable_add_review_based_on_status")
def disable_add_review_based_on_status(status):
    if status != "in_review":
        return "btn disabled"
    return ""


@register.filter(name='ref_object_id')
def ref_object_id(user, ref_request):
    obj = Request.objects.filter(order_id=ref_request).first()
    if obj:
        return obj.id
    return ""
