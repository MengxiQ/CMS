from django.db import models

# Create your models here.
from CMS.apps.equipment.models import Networkequipment

#
# class Interfaces(models.Model):
#     equipment = models.ForeignKey(Networkequipment, on_delete=models.CASCADE, null=True)
#     ifName = models.CharField(max_length=255, null=True)
#     baseConfig = models.CharField(max_length=1000, null=True)
#     ipv4Config = models.CharField(max_length=1000, null=True)
#     ipv6Config = models.CharField(max_length=1000, null=True)
#
#     class Meta:
#         managed = True
#         db_table = 'interfaces'