from django.contrib import admin

# O que foi colocado abaixo daqui foi meu código e acima o código gerado
# automaticamente pelo Django.

# importa a app artigos que criei para usar na interface admin 
from .models import Artigo

# forma alternativa para o 'admin.site.register(Artigo, AtigoAdmin)
# como não sei pra que nem como usar o @ preferi deixar da outra forma que
# faz mais sentido para mim. 
# 
# @admin.register(Artigo)

# Essa classe vai ser usado para fazer melhorias na pag de admin
class ArtigoAdmin(admin.ModelAdmin):
    # essa variavel permite escolher quais os parametros do models nós
    # desejamos mostrar(display) na pag de admin na tabela de artigos 
    list_display = ('titulo', 'slug', 'autor', 'criado', 'atualizado')

    # Cria um campo de filtro para encontrar os artigos, dentro da lista
    # é passado os models pelo qual se deja filtrar 
    list_filter = ['titulo', 'autor']

    # Faz com que o campo 'slug', que é identificado na nossa app por
    # 'caminho do link (blog/)', seja preenchido automaticamente ao se ditar
    # o titulo do artigo 
    prepopulated_fields = {'slug':('titulo',)}

# Usa o app padrão do django (admin) para mostrar o meu app na pag de admin
# permite tbm acrecentar novos artigos pela pag de admin. 
# o primeiro parametro é o models, no nosso caso 'Artigo' e o segundo
# é a classe que acabamos de criar para 'melhorar' a pagina de admin
admin.site.register(Artigo, ArtigoAdmin)
