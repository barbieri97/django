from django.db import models

# O que foi feito abaixo desse ponto foi meu código e acima veio
# automaticamente com o Django

# Esses modulos nos permite a trabalhar com as horas atuais 
from django.utils import timezone
from datetime import timedelta

#importa modulo para usar o decorator
from django.contrib import admin 


# Os nomes das tabelas são geradas automaticamente combinando o nome do app
# com o nome das classes.
# abaixo coloquei só os nomes das classes para facilitar.

# O Django gera de forma automatica uma coluna id, que será unica para cada
# item adicionado, as foreign Keys iram se referenciar a esses ids, 
# automaticamente

# Essa classe vai cria uma tablela chamada Pergunta no banco de dados, a qual
# sera a fonte onde sera buscado as informações relacionadas as 'perguntas' da
# nossa enquete.
# Essa classe herda, necessariamente, a classe models.Model
class Pergunta(models.Model):

    # Os atributos da classe indica que será criado uma coluna na tabela
    # Pergunta com o nome do atributo e esse atributo vai receber as
    # caracteristicas dos dados, se ele vai ser um int, varchar, primarykey
    # e etc, caracteristicas de um dado em um banco de dados.

    # Esse atributo indica que será criado uma coluna na tabela Pergunta 
    # chamada 'texto_pergunta' que será um 'char'(caracteres), com o maximo
    # de 200 caracteres.
    # a string passada como primeiro argumento indica o nome 'amigavel' dessa
    # coluna, esse nome irá aparecer no site administrativo, por exemplo
    # Essa coluna vai armazenar o texto das perguntas 
    texto_pergunta = models.CharField('Texto da pergunta', max_length=200)

    # Esse atributo indica que será criado uma coluna na tabela Pergunta com
    # o nome 'data_publi' e será um 'datetime'(um campo para datas), e recebe
    # um nome amigavel de 'data de publicação'
    # Essa coluna vai armazenar a data das publicações
    data_publi = models.DateTimeField('data de publicação')

    # essa função é chamada quando for ser usado o nome do objeto que criamos
    # ao invés de aparacer algo como 'objeto1' vao aparecer o nome que 
    # retornamos  dessa função
    def __str__(self):
        return self.texto_pergunta


    # Esse função nos permite verificar se pergunta foi publicada a no maximo
    # um dia.
    # retorna True se tiver sido feita a no maximo um dia e False se for mais
    # antiga
    @admin.display( #decorator para o painel admintrativo
        boolean = True,
        ordering = 'data_publi',
        description = 'publicado recentemente?' 
    ) 
    def foi_publicado_recentemente(self):
        return timezone.now() >= self.data_publi >= timezone.now() - timedelta(days=1)


# Essa classe vai cirar uma tabela chamada Resposta no banco de dados que será
# a fonte para as informações sobre as perguntas na nossa enquete
# Essa classe herda, necessariamente, a classe models.Model
class Resposta(models.Model):

    # Esse atributo irá criar uma coluna na tabela Respostas.
    # essa coluna irá se referenciar a tabela Perguntas por ser uma forerignKey
    # logo irá armazenar o id de uma pergunta ao qual ela será uma das possiveis 
    # resposta.
    # Uma pergunta tem varias respostas e varias respostas podem pertencer a uma
    # unica pergunta.
    # O primeiro parametro é a tabela a qual a coluna vai se referir e o
    # 'on_delete=models.CASCADE' indica que se a pergunta dessa resposta for
    # apagada a pergunta também o será
    # Essa coluna vai armazenar o id da pergunta ao qual ela se refere
    # O django vai adicionar um '_id' no final de 'pergunta' por ser uma 
    # chave estrangeira.
    pergunta =  models.ForeignKey(Pergunta, on_delete=models.CASCADE)

    # Esse atributo vai criar uma coluna na tabela respostas com o nome 
    # texto_resposta e sera um 'char' com o maximo de caracteres em 200
    # e o nome amigavel 'texto da pergunta'
    # Essa coluna vai armazenar o texto da pergunta
    texto_resposta = models.CharField('texto da pergunta', max_length=200)
    
    # Esse attibuto vai criar uma coluna na tabela respostas.
    # essa coluna vai ser uma integer(numeros inteiros) e com 
    # default = 0 indica que sempre será iniciada com o valor 0 e recebe
    # o nome amigavel 'numero de votos para essa resposta'
    # Essa coluna vai armazenar o numero de votos que essa resposta teve
    votes = models.IntegerField('numero de votos para essa resposta', default=0)
    
    # essa função é chamada quando for ser usado o nome do objeto que criamos
    # ao invés de aparacer algo como 'objeto1' vao aparecer o nome que 
    # retornamos  dessa função
    def __str__(self):
        return self.texto_resposta
