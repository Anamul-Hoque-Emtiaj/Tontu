# Generated by Django 4.1.5 on 2023-02-08 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0006_product_rating_product_review_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]
