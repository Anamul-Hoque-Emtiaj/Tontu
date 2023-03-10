# Generated by Django 4.1.5 on 2023-02-05 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0002_alter_productreview_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraddressbook',
            name='status',
        ),
        migrations.AddField(
            model_name='useraddressbook',
            name='city',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='useraddressbook',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.cartorder'),
        ),
        migrations.AddField(
            model_name='useraddressbook',
            name='street_address',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='useraddressbook',
            name='zipcode',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
