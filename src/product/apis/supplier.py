from django.shortcuts import render
from django.views import View
from authentication.models import User
from product.models.product_models import Part
from rest_framework.views import APIView
from product.serializer.supplier import SupplierSerializer
from rest_framework.response import Response


class PartSupplierView(View):
    def get(self, request, id):
        context = {
            "user_id": request.user.id,
            "part_id": id
        }
        return render(request, './admin/product/supplier/create.html', context)


class SupplierView(APIView):
    def get(self, request):
        part = Part.objects.get(id=request.GET["part_id"])
        part_suppliers = SupplierSerializer(part.supplier.all(), many=True)
        suppliers = SupplierSerializer(User.objects.filter(role='supplier'), many=True)
        return Response({"part_suppliers": part_suppliers.data, "suppliers": suppliers.data})

    def post(self, request):
        part = Part.objects.get(id=request.data.get('part_id'))
        part.supplier.set(User.objects.filter(id__in=request.data.get('suppliers')))
        return Response("Success")
