# Generated by Django 4.1.5 on 2023-02-05 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productreview',
            options={'verbose_name_plural': '10. ProductReview'},
        ),
        migrations.AlterModelOptions(
            name='useraddressbook',
            options={'verbose_name_plural': '12. AddressBook'},
        ),
        migrations.AlterModelOptions(
            name='wishlist',
            options={'verbose_name_plural': '11. Wishlist'},
        ),
        migrations.RemoveField(
            model_name='productattribute',
            name='size',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
    ]
