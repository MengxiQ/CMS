from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from CMS.apps.configManage.models import TempType, UnitType, Function
from CMS.apps.typesManage.serializers.TypeSerializers import TempTypesSeralizers, \
    UnitTypeSerializers, FunctionSerializers, VendorSerializers
from CMS.apps.equipment.models import NeType, Vendor
from CMS.apps.equipment.serializers import NeTypeSerializers


class TempTypesView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = TempType.objects.all()
    serializer_class = TempTypesSeralizers


class UnitTypesView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = UnitType.objects.all()
    serializer_class = UnitTypeSerializers

    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     unitType = UnitType.objects.create(name=data.get('name'),
    #                                        remark=data.get('remark'),
    #                                        )
    #     vendor = Vendor.objects.get(name=data.get('vendor'))
    #     unitType.vendor = vendor
    #     unitType.save()
    #
    #     serializer = self.serializer_class(unitType)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    #
    # def update(self, request, *args, **kwargs):
    #     data = request.data
    #     unitType = UnitType.objects.get(id=kwargs.get('pk'))
    #     unitType.name = data.get('name')
    #     unitType.remark = data.get('remark')
    #
    #     vendor = Vendor.objects.get(name=data.get('vendor'))
    #     unitType.vendor = vendor
    #     unitType.save()
    #     serializer = self.serializer_class(unitType)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class FunctionsTypesView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = Function.objects.all()
    serializer_class = FunctionSerializers


class NeTypesViews(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = NeType.objects.all()
    serializer_class = NeTypeSerializers


class VendorTypesViews(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializers


