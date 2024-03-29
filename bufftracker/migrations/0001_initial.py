# Generated by Django 3.0.6 on 2020-05-19 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CasterLevelFormula",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("displayed_formula", models.CharField(max_length=100)),
                ("function_name", models.CharField(max_length=100)),
            ],
            options={"ordering": ("displayed_formula",),},
        ),
        migrations.CreateModel(
            name="MiscBonus",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.CharField(max_length=200)),
            ],
            options={"ordering": ("description",),},
        ),
        migrations.CreateModel(
            name="ModifierType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
            options={"ordering": ("name",),},
        ),
        migrations.CreateModel(
            name="NumericalBonus",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={"ordering": ("bonus_formula__displayed_formula",),},
        ),
        migrations.CreateModel(
            name="Source",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("short_name", models.CharField(max_length=5)),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="StatisticGroup",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
            options={"ordering": ("name",),},
        ),
        migrations.CreateModel(
            name="TempHPBonus",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("die_size", models.IntegerField(default=0)),
                (
                    "die_number_formula",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="die_number",
                        to="bufftracker.CasterLevelFormula",
                    ),
                ),
                (
                    "other_bonus_formula",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="other_bonus",
                        to="bufftracker.CasterLevelFormula",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Statistic",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="bufftracker.StatisticGroup",
                    ),
                ),
            ],
            options={"ordering": ("group__name", "name"),},
        ),
        migrations.CreateModel(
            name="Spell",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("real_spell", models.BooleanField(default=True)),
                ("varies_by_cl", models.BooleanField(default=False)),
                ("size_modifying", models.BooleanField(default=False)),
                (
                    "additional_note",
                    models.CharField(blank=True, default="", max_length=200),
                ),
                (
                    "misc_bonuses",
                    models.ManyToManyField(blank=True, to="bufftracker.MiscBonus"),
                ),
                (
                    "numerical_bonuses",
                    models.ManyToManyField(blank=True, to="bufftracker.NumericalBonus"),
                ),
                (
                    "source",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="bufftracker.Source",
                    ),
                ),
                (
                    "temp_hp_bonuses",
                    models.ManyToManyField(blank=True, to="bufftracker.TempHPBonus"),
                ),
            ],
            options={"ordering": ("name",),},
        ),
        migrations.AddField(
            model_name="numericalbonus",
            name="applies_to",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="bufftracker.Statistic"
            ),
        ),
        migrations.AddField(
            model_name="numericalbonus",
            name="bonus_formula",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="bufftracker.CasterLevelFormula",
            ),
        ),
        migrations.AddField(
            model_name="numericalbonus",
            name="modifier_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="bufftracker.ModifierType",
            ),
        ),
    ]
