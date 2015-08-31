from django.contrib import admin
from bufftracker import models
from bufftracker.hardcoded_data import CasterLevelFormula


class SpellAdmin(admin.ModelAdmin):
    save_as = True

admin.site.register(models.Source)
admin.site.register(models.Statistic)
admin.site.register(models.StatisticGroup)
admin.site.register(models.ModifierType)
admin.site.register(models.NumericalBonus)
admin.site.register(models.MiscBonus)
admin.site.register(models.TempHPBonus)
admin.site.register(models.Spell, SpellAdmin)
admin.site.register(CasterLevelFormula)