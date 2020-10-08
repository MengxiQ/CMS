from django.db import models

# Create your models here.

class NeType(models.Model):
    tid = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ne_type'


class Nestatus(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey('NestatusType', models.DO_NOTHING, db_column='type')
    date = models.DateTimeField(blank=True, null=True)
    site = models.CharField(max_length=255, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nestatus'


class NestatusType(models.Model):
    tid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    show_type = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'nestatus_type'


class Networkequipment(models.Model):
    neid = models.AutoField(primary_key=True)
    ip = models.CharField(unique=True, max_length=255, blank=True, null=True)
    mac = models.CharField(unique=True, max_length=255, blank=True, null=True)
    fixed_id = models.CharField(unique=True, max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.ForeignKey(NeType, models.DO_NOTHING, db_column='type', blank=True, null=True)
    status = models.ForeignKey(Nestatus, models.DO_NOTHING, db_column='status', blank=True, null=True)
    unittype = models.CharField(db_column='unitType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    stock_date = models.DateTimeField(blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'networkequipment'


class NetconfUsers(models.Model):
    uid = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(Networkequipment, models.DO_NOTHING, db_column='equipment', null=False)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    port = models.IntegerField(null=False, default=22)
    device_params = models.CharField(max_length=255, null=False, default='huawei')
    hostkey = models.CharField(max_length=255, null=True)

    class Meta:
        managed = False
        db_table = 'netconfusers'