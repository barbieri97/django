from django.shortcuts import render

# O que foi feito abaixo desse ponto foi meu código e acima veio
# automaticamente com o Django

# importa uma função que consulta o os dados em urls.py e gera as urls
# completas

from django.urls import reverse

# importando o modulo que permite fazer redirecionamentos 
from django.http import HttpResponseRedirect 

# importa o modulo que permite fazer uma consulta no banco de dados e caso
# não ache levanta uma excessão 404
# esse modulo é um shortcut, um atalho, na branch view_em_funcoes tem a forma
# extensa de se fazer isso
from django.shortcuts import get_object_or_404

# importa o modulo que permite renderizar os um template e devolver um objeto
# HttpRespose
# esse modulo é um shortcut, um atalho, na branch view_em_funcoes tem a forma
# extensa de se fazer isso
from django.shortcuts import render

# importa o modulo que permite usar as views genericas
from django.views import generic

# importa os modelos que criamos
from .models import Pergunta, Resposta

# importa o modulo para trabalhar com datas
from django.utils import timezone

# essa classe vai ser a view index que tera a função de exibir todas as
# perguntas
# Essa classe herda a view generica ListView(generic.ListView)
class ViewIndex(generic.ListView):
    # Esse atributo é responsavel por definir qual template será usado
    # caso não seja passado ela vai procurar um template com 
    # <nome do app>/<nome do modelo>_detail.html
    template_name = 'enquete/index.html'

    # esse atributo define qual é o nome da variavel que definimos no template
    # se não for alterado a view generica vai gerar automaticamente uma
    # variavel de contexto com o padrão '<nome do model>_list' 
    context_object_name = 'ultimas_perguntas'

    # esse atibuto sdefine a busca que sera feita no banco de dados
    # nesse caso será feita uma busca pelas Perguntas e será ordenada por
    # 'data_publi'(data da publicação), mas na ordem inversa devido o 
    # '-' na frente de data_publi
    # adicionado o filter() para não pegar questões com data de publicação
    # no futuro
    queryset = Pergunta.objects.filter(data_publi__lte=timezone.now()).order_by('-data_publi')[:5]

# essa classe vai ser a view detalhes e vai exibir detalhes de perguntas,
# ou seja, para cada pergunta que for requisitado ela vai mostrar as suas
# possiveis respostas
class ViewDetalhe(generic.DetailView):
    
    # define em qual model sera feito as consultas
    model = Pergunta  

    # Esse atributo é responsavel por definir qual template será usado
    # caso não seja passado ela vai procurar um template com 
    # <nome do app>/<nome do modelo>_detail.html
    template_name = 'enquete/detalhe.html'

    # Exclui qualquer resposta que não tenha sido publicado ainda
    queryset = Pergunta.objects.filter(data_publi__lte=timezone.now())

    

class ViewResultado(generic.DetailView):
    
    # define em qual model sera feito as consultas
    model = Pergunta

    # Esse atributo é responsavel por definir qual template será usado
    # caso não seja passado ela vai procurar um template com 
    # <nome do app>/<nome do modelo>_detail.html
    template_name = 'enquete/resultado.html'

    # Exclui qualquer resposta que não tenha sido publicado ainda
    queryset = Pergunta.objects.filter(data_publi__lte=timezone.now())

# essa view tera a função de gerenciar os votos
def vote(request, id_pergunta):
    # faz uma consulta no banco de dados para pegar a pergunta com o
    # id = <id da pergunta>
    pergunta = get_object_or_404(Pergunta, pk=id_pergunta)
    try:
        # tenta fazer uma consulta no banco de dados para pegar a resposta 
        # escolhida na pagina detalhes
        # se acessa a pergunta escolhida através de 'request.POST['resposta']'
        # onde 'resposta' é o nome do input que usei para selecionar a pergunta
        # no fomulario 'detalhe.html' 
        resposta_selecionada = pergunta.resposta_set.get(pk=request.POST['resposta'])
    except(KeyError, Resposta.DoesNotExist):
        # Caso não ache a resposta retorna o template de detalhes.html com
        # a mensagem de erro 'você não escolheu uma resposta
        contexto = {
            'pergunta':pergunta,
            'mensagem_de_erro':'Você não escolheu uma resposta'
        }
        resposta = render(request, 'enquete/detalhe.html', contexto)
        return resposta
    else:
        # Se a tentativa der certo acrescenta um voto para a resposta 
        # escolhida e salva 
        resposta_selecionada.votes += 1
        resposta_selecionada.save()
        # Então depois de ser efetuado o voto a view redireciona para a view
        # resultado para isso usamos o HttpResponseRedirect que recebe com 
        # argumento o link para o qual ele vai redirecionar
        # ao invés de se colocar o link de forma literal é usado a função reverse
        # que recebe com argumento o nome da url e seu argumento, se tiver, e
        # devolve o a url completa
        # isso é bom para caso a url seja modificada no urls.py, não há a
        # necessidade de se mudar a url aqui, pois o reverse faz isso 
        # automaticamente
        return HttpResponseRedirect(reverse('enquete:resultado', args=(pergunta.id,)))

