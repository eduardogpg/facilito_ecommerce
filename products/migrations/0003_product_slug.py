# Generated by Django 2.2.1 on 2019-05-27 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20190524_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
