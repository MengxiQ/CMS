# Generated by Django 3.1.1 on 2020-12-21 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0003_auto_20201221_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkequipment',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='equipment.netconfusers'),
        ),
    ]
