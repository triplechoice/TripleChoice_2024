from django import forms

from authentication.models import User
from product.models.product_models import PartSupplier


class PartSupplierForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PartSupplierForm, self).__init__(*args, **kwargs)
        self.fields['supplier'].queryset = User.objects.filter(groups__name='supplier')
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control col-2 m-2'

    class Meta:
        model = PartSupplier
        fields = ['part', 'supplier']

