from django.db import models
# Create your models here.


# 厂商
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    device_param = models.CharField(max_length=255)
    remark = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'vendor'


# 设备型号
class UnitType(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    remark = models.CharField(max_length=255, blank=False, null=False)
    vendor = models.ForeignKey(Vendor, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        managed = True,
        db_table = 'unittype'


# 设备类型
class NeType(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ne_type'


class NestatusType(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    remark = models.CharField(max_length=255, blank=True, null=True)
    show_type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'nestatus_type'


class Nestatus(models.Model):
    type = models.ForeignKey(NestatusType, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(blank=True, null=True)
    site = models.CharField(max_length=255, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'nestatus'


class NetconfUsers(models.Model):
    # equipment = models.OneToOneField(Networkequipment, on_delete=models.CASCADE, null=True, unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    port = models.IntegerField(null=False, default=22)
    device_params = models.CharField(max_length=255, null=False, default='huawei')
    # hostkey = models.CharField(max_length=255, null=True)

    class Meta:
        managed = True
        db_table = 'netconfusers'


class Networkequipment(models.Model):
    ip = models.CharField(unique=True, max_length=255)
    # mac = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.ForeignKey(NeType, blank=True, null=True, on_delete=models.CASCADE)
    status = models.ForeignKey(Nestatus, blank=True, null=True, on_delete=models.CASCADE)
    unittype = models.ForeignKey(UnitType, blank=True, null=True, on_delete=models.CASCADE)
    stock_date = models.DateTimeField(blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    user = models.OneToOneField(NetconfUsers, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.ip

    class Meta:
        managed = True
        db_table = 'networkequipment'



