# Generated by Django 4.1 on 2022-08-06 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="food",
            name="external_id",
            field=models.IntegerField(
                db_index=True, unique=True, verbose_name="external id"
            ),
        ),
    ]
