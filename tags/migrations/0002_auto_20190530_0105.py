# Generated by Django 2.2.1 on 2019-05-30 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='products',
            field=models.ManyToManyField(to='products.Product'),
        ),
    ]