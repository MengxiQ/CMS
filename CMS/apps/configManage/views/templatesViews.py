from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import json
from CMS.apps.configManage.models import Templates, Function, UnitType, TempType, Params
from CMS.apps.typesManage.serializers.TypeSerializers import TemplatesSerializers

from django.db import transaction


class TemplateData(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = Templates.objects.all()
    serializer_class = TemplatesSerializers

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        template = Templates.objects.get(id=pk)
        template.templateData = request.data.get('templateData')
        template.save()
        return Response(status.HTTP_200_OK)


class StandardPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 100


class TemplatesViews(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = Templates.objects.all()
    serializer_class = TemplatesSerializers
    pagination_class = StandardPageNumberPagination
    filter_fields = ('name', 'tempType')

    def post(self, request, *args, **kwargs):
        # print(request.data)
        return self.create( request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            # 保存点
            save_point = transaction.savepoint()
            try:
                # 1. 创建模板对象
                templateSerializer = self.get_serializer(data=request.data)
                if(templateSerializer.is_valid()):
                    template = Templates.objects.create(**templateSerializer.validated_data)
                else:
                    raise Exception
                # 2，绑定模板类型
                tempType = TempType.objects.get(name=request.data.get('tempType'))
                template.tempType = tempType
                # 3. 绑定模板支持的型号
                for item in request.data.get('support'):
                    # 'unitTypes': ['CE12800','CE6800'],
                    unitType = UnitType.objects.get(name=item)
                    template.support.add(unitType)
                # 4. 绑定模板的功能
                function = Function.objects.get(name=request.data.get('function'))
                template.function = function
                # 5. 创建并绑定模板的参数
                for item in request.data.get('params'):
                    param = Params.objects.create(**item)
                    param.template = template
                    param.save()
                # 6. 保存
                template.save()
            except Exception as e:
                print(e)
                # 7. 回滚
                transaction.savepoint_rollback(save_point)
                return Response({'message': '创建失败。'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 不能返回序列化器的data的数据，因为返回效验support字段会失败
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        # print(kwargs)
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            save_point = transaction.savepoint()
            try:
                # 0.查询该模板
                pk = kwargs.get('pk')
                template = Templates.objects.get(id=pk)
                # 1.删除功能
                template.function = None
                # 2.删除模板类型
                template.tempType = None
                # 3.删除模板参数
                params = Params.objects.filter(template=template)
                for item in params:
                    item.delete()
                # 4.删除型号支持
                unitTyeps = template.support.all()
                for item in unitTyeps:
                    template.support.remove(item)
                # 5.删除该模板实例
                template.delete()
            except Exception as e:
                print(e)
                # 6.回滚
                transaction.savepoint_rollback(save_point)
                Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        with transaction.atomic():
            # 保存点
            save_point = transaction.savepoint()
            try:
                # 1. 更新模板对象基表
                # print(request.data)
                templateSerializer = self.get_serializer(data=request.data)
                # print(templateSerializer.is_valid())
                template = Templates.objects.get(id=pk)
                if (templateSerializer.is_valid()):
                    validated_data = templateSerializer.validated_data
                    template.name = validated_data.get('name')
                    template.remark = validated_data.get('remark')
                    template.updateDate = validated_data.get('updateDate')
                    template.templateData = validated_data.get('templateData')
                else:
                    raise Exception
                # 2，更新模板类型
                tempType = TempType.objects.get(name=request.data.get('tempType'))
                template.tempType = tempType
                # 3. 更新模板支持的型号
                # 3.1.删除型号支持
                unitTyeps = template.support.all()
                for item in unitTyeps:
                    template.support.remove(item)
                # 3.2 添加
                for item in request.data.get('support'):
                    # 'unitTypes': ['CE12800','CE6800'],
                    unitType = UnitType.objects.get(name=item)
                    template.support.add(unitType)
                # 4. 绑定模板的功能
                function = Function.objects.get(name=request.data.get('function'))
                template.function = function
                # 5. 更新模板的参数
                # 5.1.删除模板参数
                params = Params.objects.filter(template=template)
                for item in params:
                    item.delete()
                # 5.2 更新参数
                for item in request.data.get('params'):
                    item['template'] = template
                    param = Params.objects.create(**item)
                    param.template = template
                    param.save()
                # 6. 保存
                template.save()
            except Exception as e:
                print(e)
                # 7. 回滚
                transaction.savepoint_rollback(save_point)
                return Response({'message': '更新失败。'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)