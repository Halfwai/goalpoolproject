# Generated by Django 4.0.1 on 2022-11-13 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goalpoolapp', '0035_rename_teamid_country_countryid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixture',
            name='awayteam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='awayfixture', to='goalpoolapp.country'),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='hometeam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homefixture', to='goalpoolapp.country'),
        ),
    ]
