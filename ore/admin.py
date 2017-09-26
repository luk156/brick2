from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from ore.models import Cliente, Cantiere, Dipendente, Attivita, SchedaLavoro, CategoriaAttivita, SchedaAttivita


class SchedaAttivitaInline(admin.TabularInline):
    model = SchedaAttivita


@admin.register(SchedaLavoro)
class SchedaLavoroAdmin(admin.ModelAdmin):
    list_filter = ('dipendente', 'cantiere',)
    inlines = [
        SchedaAttivitaInline,
    ]


admin.site.register(Cliente)
admin.site.register(Cantiere)
admin.site.register(Dipendente)
admin.site.register(Attivita)
admin.site.register(CategoriaAttivita,MPTTModelAdmin)





