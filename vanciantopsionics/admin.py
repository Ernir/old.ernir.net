from django.contrib import admin
from vanciantopsionics.models import VtPFile, CharacterClass
from vanciantopsionics.models import Chapter, Section, Subsection, Subsubsection, Spell


admin.site.register(VtPFile)

admin.site.register(Chapter)
admin.site.register(Section)
admin.site.register(Subsection)
admin.site.register(Subsubsection)

admin.site.register(Spell)
admin.site.register(CharacterClass)
