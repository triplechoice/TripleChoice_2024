from django import forms
from django.core.exceptions import ValidationError

from order.models.request import RequestReview, Request


class RequestReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RequestReviewForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = RequestReview
        fields = ['title', 'description', 'supplier_cost', 'supplier_lead_time', 'quantity', 'supplier_unit', 'request',
                  'user', 'supplier_cost_unit']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def clean(self):
        cd = self.cleaned_data

        supplier_cost = cd.get("supplier_cost")
        supplier_lead_time = cd.get("supplier_lead_time")

        if supplier_cost < 0:
            self.errors['supplier_cost'] = 'Cost cannot be negative'
            raise ValidationError("Cost cannot be negative")

        if supplier_lead_time < 0:
            self.errors['supplier_lead_time'] = 'Lead time cannot be negative'
            raise ValidationError("Lead time cannot be negative")

        return cd

    def save(self, commit=True):
        instance = super().save()
        if instance.lead_time is None:
            instance.lead_time = instance.supplier_lead_time
            instance.cost = instance.supplier_cost
            instance.unit = instance.supplier_unit
            instance.cost_unit = instance.supplier_cost_unit
            instance.save()
        request_order_id = instance.request.order_id
        request_obj = Request.objects.get(order_id=request_order_id)
        if request_obj.admin_status != "sent_review_to_customer":
            request_obj.admin_status = "supplier_sent_review"
            request_obj.save()

        return instance
