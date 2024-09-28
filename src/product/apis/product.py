import json
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView

from authentication.models import User
from order.models.request import Request
from product.filters.part_filter import PartFilter, PartExactTitleFilter
from product.models import Attribute, Classification
from product.models.product_models import Part, PartClassification, PartClassificationAttribute, PartSupplier
from product.serializer.product import AttributeSerializer, ClassificationSerializer, PartSerializer, \
    PartDetailsSerializer
from utils.services.disposable_email import DisposableEmail
from authentication.mixins import PermissionMixin


class AttributeList(ListAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


class ClassificationList(ListAPIView):
    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer
    pagination_class = None


class AttributeByClassification(ListAPIView):
    queryset = Attribute.objects.all()
    serializer_class = ClassificationSerializer
    pagination_class = None

    def get_queryset(self):
        id = self.kwargs['id']
        data = Attribute.objects.filter(classification=id)
        return data


class PartApiView(CreateAPIView, ListAPIView, UpdateAPIView):
    serializer_class = PartSerializer
    queryset = Part.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        self.__get_query()
        data = Part.objects.all()
        return data

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def __get_query(self):
        if self.request.GET.get('exact') == 'true':
            self.filterset_class = PartExactTitleFilter
            self.serializer_class = PartDetailsSerializer
        else:
            self.filterset_class = PartFilter
        if self.request.GET.get('pagination') == 'false':
            self.pagination_class = None


class HomePageView(View):
    def get(self, request):
        contex = {}
        return render(request, 'frontend/index.html', contex)


class PartView(View, DisposableEmail):

    def get(self, request, slug, order_id=None):
        if order_id:
            order = Request.objects.filter(id=order_id, user=request.user).first()
            if order is None:
                raise PermissionDenied
            if order.customer_status != 'submitted':
                messages.error(request, 'you can  edit order only pending state', extra_tags='error')
                return redirect(request.META.get('HTTP_REFERER'))
        part = Part.objects.values('id', 'title', 'slug').filter(slug=slug).first()
        context = {'part': json.dumps(part), 'order_id': order_id, 'title': part.get('title')}
        return render(request, 'frontend/part.html', context)


class PartDetailsApiView(RetrieveAPIView):
    serializer_class = PartDetailsSerializer
    queryset = Part.objects.all()
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class PartDetailsByIdView(RetrieveAPIView):
    serializer_class = PartDetailsSerializer
    queryset = Part.objects.all()
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# TODO:form wizard
class WizardView(View):
    def get(self, request, slug, order_id=None):
        if order_id:
            order = Request.objects.filter(id=order_id).first()
            if order.status != 'pending':
                messages.error(request, 'you can  edit order only pending state', extra_tags='error')
                return redirect(request.META.get('HTTP_REFERER'))
        part = Part.objects.values('id', 'title', 'slug').filter(slug=slug).first()
        context = {'part': json.dumps(part), 'order_id': order_id}
        return render(request, 'frontend/wizard.html', context)


class AddPartSupplierView(View):

    def post(self, request):
        if request.user.is_superuser:
            if request.POST.get('update'):
                part_supplier_obj = PartSupplier.objects.filter(part_id=request.POST['part']).first()
                if not part_supplier_obj:
                    part_supplier_obj = PartSupplier.objects.create(part_id=request.POST['part'])
                part_supplier_obj.supplier.set(User.objects.filter(id__in=request.POST.getlist('supplier')))
            else:
                part_supplier_obj = PartSupplier.objects.filter(part_id=request.POST['part']).first()
                if part_supplier_obj:
                    for id in request.POST.getlist('supplier'):
                        part_supplier_obj.supplier.add(id)
                else:
                    part_supplier_obj = PartSupplier.objects.create(part_id=request.POST['part'])
                    part_supplier_obj.supplier.set(User.objects.filter(id__in=request.POST.getlist('supplier')))
            return redirect('/super-admin/product/partsupplier/')
        return HttpResponse('Page not found')


class DeletePartSupplierView(View):
    def post(self, request, id):
        if request.user.is_superuser:
            obj = PartSupplier.objects.get(id=id)
            obj.delete()
            return redirect('/super-admin/product/partsupplier/')
        return HttpResponse('Page not found')
