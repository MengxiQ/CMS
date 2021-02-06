from django.db import models
from CMS.apps.equipment.models import UnitType


# class BaseModel(models.Model):
#     name = models.CharField(max_length=100, blank=True, null=True)
#     remark = models.CharField(max_length=255, blank=True, null=True)


# 模板类型
class TempType(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'temp_type'


# 模板功能
class Function(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'function'


# 模板
class Templates(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    tempType = models.ForeignKey(TempType, blank=True, null=True, on_delete=models.CASCADE)
    # params = models.ForeignKey(Params, blank=True, null=True, on_delete=models.CASCADE)
    function = models.ForeignKey(Function, blank=True, null=True, on_delete=models.CASCADE)
    support = models.ManyToManyField(to=UnitType)
    templateData = models.CharField(max_length=5000, blank=True, null=True)
    updateDate = models.DateTimeField(blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)  # 数据父标签
    class Meta:
        managed = True
        db_table = 'templates'


# 模板参数
class Params(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=100, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    constraint = models.CharField(max_length=255, blank=True, null=True)  # 参数约束
    role = models.CharField(max_length=255, blank=True, null=True)  # 参数角色
    template = models.ForeignKey(Templates, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'params'
