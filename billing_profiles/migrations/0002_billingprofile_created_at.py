# Generated by Django 2.2.1 on 2019-06-17 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing_profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingprofile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
    ]