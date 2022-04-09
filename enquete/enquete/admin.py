from django.contrib import admin

# Register your models here.

# importando o meu model para que apareçao no site de administração
from .models import Pergunta, Resposta

# Essa classe permite editar as respostas das perguntas na mesma pagina das
# perguntas
class EscolhaNaLinha(admin.TabularInline):
    model = Resposta

# Essa classe permite personalizar algumas coisas no painel adiministrativo
# como a apresentação dos meus modelos e suas funcionalidades
class PerguntaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['texto_pergunta']}),
        ('informação da data',{'fields':['data_publi']})
    ]

    inlines = [EscolhaNaLinha]

    list_display = ('texto_pergunta', 'data_publi', 'foi_publicado_recentemente')

    list_filter = ['data_publi']

    search_fields = ['texto_pergunta']

# informando que é para registrar o meu app no site de adiminstração
# e assim poder adicionar novas enquetes por la
admin.site.register(Pergunta, PerguntaAdmin)