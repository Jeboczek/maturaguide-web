# Generated by Django 3.2.8 on 2021-10-10 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maturaguideapi', '0008_auto_20211010_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_tags',
            field=models.ManyToManyField(help_text='Tagi pytania.', to='maturaguideapi.QuestionTag'),
        ),
    ]
