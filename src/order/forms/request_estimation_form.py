from django import forms
from order.models.request import Request


class RequestEstimation(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RequestEstimation, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Request
        fields = ('quantity', 'cost', 'lead_time')
