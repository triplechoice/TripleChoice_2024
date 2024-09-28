from django.urls import path, include

from product.apis.product import AttributeList, ClassificationList, AttributeByClassification, PartApiView, \
    HomePageView, PartView, PartDetailsApiView, WizardView, AddPartSupplierView, DeletePartSupplierView, \
    PartDetailsByIdView
from product.apis.supplier import PartSupplierView
from product.apis.supplier import SupplierView

app_name = 'product'

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('part/<slug:slug>/', PartView.as_view(), name="part.details"),
    path('part/supplier/<int:id>/', PartSupplierView.as_view(), name="part.supplier"),
    # TODO:form wizard
    path('wizard/<slug:slug>/', WizardView.as_view(), name="wizard"),
    path('add/part-supplier/', AddPartSupplierView.as_view(), name='add.part.supplier'),
    path('delete/part-supplier/<int:id>', DeletePartSupplierView.as_view(), name='delete.part.supplier')
]

# url for api
urlpatterns += [
    path('api/', include([
        path('attribute/', AttributeList.as_view()),
        path('classification/', ClassificationList.as_view()),
        path('attribute/<int:id>', AttributeByClassification.as_view()),
        path('part/', PartApiView.as_view()),
        path('part-update/<int:id>/', PartApiView.as_view()),
        path('part/<slug:slug>', PartDetailsApiView.as_view()),
        path('part/supplier/', SupplierView.as_view()),
        path('part-details/<str:id>/', PartDetailsByIdView.as_view())
    ]))
]
