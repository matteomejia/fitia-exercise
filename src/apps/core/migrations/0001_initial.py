# Generated by Django 4.1 on 2022-08-06 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Food",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "external_id",
                    models.IntegerField(unique=True, verbose_name="external id"),
                ),
                ("name", models.CharField(max_length=255, verbose_name="name")),
                (
                    "macro_type",
                    models.CharField(
                        choices=[
                            ("Proteina", "protein"),
                            ("Carbohidrato", "carbohydrate"),
                            ("Grasa", "fat"),
                        ],
                        max_length=255,
                        verbose_name="macro type",
                    ),
                ),
                ("calories", models.FloatField(verbose_name="calories")),
                ("protein", models.FloatField(verbose_name="protein")),
                ("carbohydrates", models.FloatField(verbose_name="carbohydrates")),
                ("fat", models.FloatField(verbose_name="fat")),
                (
                    "portion_unit",
                    models.CharField(max_length=255, verbose_name="portion unit"),
                ),
                ("portion_weight", models.FloatField(verbose_name="portion weight")),
                ("portion_min", models.IntegerField(verbose_name="minimum portions")),
                ("portion_max", models.IntegerField(verbose_name="maximum portions")),
                (
                    "breakfast",
                    models.BooleanField(default=True, verbose_name="breakfast"),
                ),
                ("lunch", models.BooleanField(default=True, verbose_name="lunch")),
                ("dinner", models.BooleanField(default=True, verbose_name="dinner")),
            ],
            options={
                "verbose_name": "food",
                "verbose_name_plural": "foods",
            },
        ),
    ]