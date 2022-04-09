from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render,  get_object_or_404
from django.urls import reverse

from .models import Preco, Produto

# Create your views here.

def index(request):

    produtos = Produto.objects.order_by('-voto')
    precos = Preco.objects.all()
    return render(request, 'cardapio/index.html', {
        'produtos':produtos,
        'precos':precos,
        })

def detalhe(request, slug):
    detalhes = Produto.objects.get(slug=slug)
    precos = Preco.objects.all()

    contexto = {
        'detalhes':detalhes,
        'precos':precos
    }
    return render(request, 'cardapio/detalhe.html', contexto)

def favorito(request, slug):
    x = request.POST['resposta']
    x = x.split()
    x = x[-1]
    produto = get_object_or_404(Produto, slug=x)
    produto.voto += 1
    produto.save()
    return HttpResponseRedirect(reverse('cardapio:favoritos'))

def favoritos(request):
    favoritos = Produto.objects.order_by('-voto')
    contexto = {
        'favoritos':favoritos
    }
    return render(request, 'cardapio/favoritos.html', contexto)