from django.shortcuts import render

# O que foi colocado abaixo daqui foi meu código e acima o código gerado
# automaticamente pelo Django.

# Importa algumas views genericas
# as views genericas ja vem por padão algumas funcionalidades comuns
# como listar objetos, exibir detalhes e etc 
from django.views.generic import DetailView, ListView

# importa a nossa app
from .models import Artigo

# Essa classe vai gerar uma view que lista todos os artigos diponiveis.
# Essa classe herda a view generica ListView.
class ArtigoListaView(ListView):
    model = Artigo
    template_name = 'blog/lista_artigos.html'

# Essa classe vai gerar uma view que mostra detalhes de um artigo.
# Essa classe herda a view generica DetailView 
class ArtigoDetalheView(DetailView):
    model = Artigo
    template_name = 'blog/detalhe_artigo.html'