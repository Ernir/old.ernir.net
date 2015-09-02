from django.db import models
from bufftracker.hardcoded_data import CasterLevelFormula


class Source(models.Model):
    short_name = models.CharField(max_length=5)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class StatisticGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_as_dict(self):
        """
        Returns a dictionary object representing this group.
        """
        return {
            "id": self.id,
            "name": self.name,
            "statistics": [
                stat.get_as_dict() for stat in self.statistic_set.all()
            ]
        }

    class Meta:
        ordering = ("name", )


class Statistic(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(StatisticGroup)

    def __str__(self):
        return self.name

    def get_as_dict(self):
        """
        Returns a dictionary object representing this statistic.
        """
        return {
            "id": self.id,
            "name": self.name
        }

    class Meta:
        ordering = ("group__name", "name")


class ModifierType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name", )


class MiscBonus(models.Model):
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ("description", )


class NumericalBonus(models.Model):
    bonus_formula = models.ForeignKey(CasterLevelFormula, null=True)
    modifier_type = models.ForeignKey(ModifierType)
    applies_to = models.ForeignKey(Statistic)

    def __str__(self):
        if self.bonus_formula:
            bonus_value = self.bonus_formula.displayed_formula
        else:
            bonus_value = ""
        modifier_type = self.modifier_type.name
        applies_to = self.applies_to.name
        return bonus_value + " " + modifier_type + " bonus to " + applies_to

    def save(self, *args, **kwargs):
        super(NumericalBonus, self).save(*args, **kwargs)
        self.formula = str(self)

    class Meta:
        ordering = ("bonus_formula__displayed_formula", )


class TempHPBonus(models.Model):
    die_number_formula = models.ForeignKey(
        CasterLevelFormula,
        related_name="die_number",
        null=True
    )
    die_size = models.IntegerField(default=0)
    other_bonus_formula = models.ForeignKey(
        CasterLevelFormula,
        related_name="other_bonus",
        null=True
    )

    def __str__(self):
        if self.die_number_formula:
            die_number = self.die_number_formula.displayed_formula
        else:
            die_number = ""
        die_size = str(self.die_size)
        if self.other_bonus_formula:
            other_bonus = self.other_bonus_formula.displayed_formula
        else:
            other_bonus = ""
        return die_number + "d" + die_size + " + " + other_bonus


class Spell(models.Model):
    name = models.CharField(max_length=100)
    source = models.ForeignKey(Source)

    numerical_bonuses = models.ManyToManyField(NumericalBonus, blank=True)
    misc_bonuses = models.ManyToManyField(MiscBonus, blank=True)
    temp_hp_bonuses = models.ManyToManyField(TempHPBonus, blank=True)

    real_spell = models.BooleanField(default=True)
    varies_by_cl = models.BooleanField(default=False)
    size_modifying = models.BooleanField(default=False)

    additional_note = models.CharField(max_length=200, blank=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
