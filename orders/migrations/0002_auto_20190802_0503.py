# Generated by Django 2.2.4 on 2019-08-02 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sicilianpizza',
            old_name='topping_size',
            new_name='item_size',
        ),
    ]