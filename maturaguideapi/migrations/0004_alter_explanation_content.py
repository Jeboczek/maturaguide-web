# Generated by Django 3.2.8 on 2021-10-10 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maturaguideapi', '0003_auto_20211010_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='explanation',
            name='content',
            field=models.JSONField(default=list),
        ),
    ]
