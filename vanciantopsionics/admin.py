from django.contrib import admin
from vanciantopsionics.models import VtPFile
from vanciantopsionics.models import Chapter, Section, Subsection, Subsubsection


admin.site.register(VtPFile)

admin.site.register(Chapter)
admin.site.register(Section)
admin.site.register(Subsection)
admin.site.register(Subsubsection)