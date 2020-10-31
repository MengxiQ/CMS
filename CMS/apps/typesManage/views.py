from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from CMS.apps.configManage.models import TempType, UnitType, Function
from CMS.apps.configManage.serializers import TempTypesSeralizers, UnitTypeSerializers, FunctionSerializers
from CMS.apps.equipment.models import NeType
from CMS.apps.equipment.serializers import NeTypeSerializers


class TempTypesView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = TempType.objects.all()
    serializer_class = TempTypesSeralizers


class UnitTypesView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = UnitType.objects.all()
    serializer_class = UnitTypeSerializers


class FunctionsTypesView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = Function.objects.all()
    serializer_class = FunctionSerializers


class NeTypesViews(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = NeType.objects.all()
    serializer_class = NeTypeSerializers