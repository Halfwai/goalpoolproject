# Generated by Django 4.0.1 on 2022-11-13 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goalpoolapp', '0033_rename_realteam_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='goals',
            field=models.IntegerField(null=True),
        ),
    ]
