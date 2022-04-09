from django.contrib import admin
from .models import Produto, Caracteristica, Preco

class CaracteristicaEmLinha(admin.TabularInline):
    model = Caracteristica
    extra = 1

class ProdutoAdmin(admin.ModelAdmin):
    fieldsets = [
        ('produto', {'fields':['nome']}),
        ('url', {'fields': ['slug']}),
        ('tipo', {'fields': ['tipo']}),
    ]

    inlines = [CaracteristicaEmLinha]

    prepopulated_fields = {'slug':('nome',)}

    list_filter = ['tipo']

    search_fields = ['nome']

    list_display = ('nome', 'tipo')
admin.site.register(Produto, ProdutoAdmin)

admin.site.register(Preco)
