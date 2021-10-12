from django.db import models


class Topology(models.Model):
    name = models.CharField(max_length=100)
    connectors = models.TextField()
    nodes = models.TextField()

    class Meta:
        managed = True
        db_table = 'topology'
