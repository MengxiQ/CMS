# Generated by Django 3.1.1 on 2020-10-28 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configManage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='function',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='params',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='templates',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='temptype',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]