from django.db import models
from django.db.models.fields import CharField

# Create your models here.

class Produto(models.Model):
    escolha_tipo=[
        ('D', 'Doce'),
        ('S', 'salgado')
    ]    
    nome = models.CharField('Nome do Produto', max_length=200)
    tipo = models.CharField('Tipo do produto', max_length=1, choices=escolha_tipo)
    slug = models.SlugField(max_length=200, unique=True)
    voto = models.IntegerField('numero de favritos', default=0)

    def __str__(self):
        return self.nome

class Caracteristica(models.Model):
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE)
    ingredientes = models.TextField('Ingredientes', unique=True)
    descricao = models.TextField('Descrição', blank=True)
    

    def __str__(self):
        return f'{self.produto.nome}'

class Preco(models.Model):
    escolha_tipo = [
        ('C', 'Congelado'),
        ('F', 'Frito'),
    ]
    unidades = models.IntegerField('Quantidade')
    valor = models.FloatField('Valor')
    tipo = CharField(max_length=1, choices=escolha_tipo, blank=True)

    def __str__(self) -> str:
        return f'quant: {self.unidades}, tipo: {self.tipo}'


