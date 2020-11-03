# Generated by Django 3.1.1 on 2020-10-28 05:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('equipment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interfaces',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ifName', models.CharField(max_length=255, null=True)),
                ('baseConfig', models.CharField(max_length=1000, null=True)),
                ('ipv4Config', models.CharField(max_length=1000, null=True)),
                ('ipv6Config', models.CharField(max_length=1000, null=True)),
                ('equipment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.networkequipment')),
            ],
            options={
                'db_table': 'interfaces',
                'managed': True,
            },
        ),
    ]