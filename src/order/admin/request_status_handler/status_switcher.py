from django_q.tasks import async_task

from product.models.product_models import PartSupplier


def status_changer(obj, moderator_status="", supplier_status="", customer_status=""):
    obj.customer_status = customer_status
    obj.supplier_status = supplier_status
    obj.moderator_status = moderator_status
    obj.save()


def email_sent_to_suppliers(obj):
    part = obj.part
    part = PartSupplier.objects.filter(part=part).first()
    if part:
        async_task('order.jobs.emails.send_email_to_suppliers_review', part)
    obj.customer_status = 'processing'
    obj.supplier_status = 'new_request'
    obj.save()


def update_request_status(request, obj):
    if obj.admin_status == 'sent_to_supplier':
        email_sent_to_suppliers(obj)

    elif obj.admin_status == 'pending':
        status_changer(obj=obj, moderator_status="", customer_status="submitted", supplier_status="")

    elif obj.admin_status == 'received_results_from_supplier':
        status_changer(obj=obj, moderator_status="new_review", customer_status="in_review", supplier_status="submitted")

    elif obj.admin_status == 'completed':
        status_changer(obj=obj, moderator_status="completed", customer_status='results', supplier_status='submitted')

    elif obj.admin_status == 'cancelled':
        status_changer(obj=obj, moderator_status='cancelled', supplier_status='cancelled', customer_status='cancelled')
