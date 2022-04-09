from django.db import models

# O que foi colocado abaixo daqui foi meu código e acima o código gerado
# automaticamente pelo Django.

# importando essa biblioteca para pegar o autor do artigo.
from django.contrib.auth.models import User

#importando esse modulo para gerar as urls para o artigo
from django.urls import reverse


class Artigo(models.Model):
    # Cria a coluna titulo na tablea Artigos, que será responsável por
    # armazenar os titulos dos artigos.
    # O primeiro parametro é uma string que será o nome 'humanreadable', ou
    # seja, um nome mais amigavel para humanos para a coluna titulo e o 
    # parametro max_length=255 indica que o maximo de caracteres que a coluna
    # vai aceitar é 255.
    titulo = models.CharField('titulo do artigo', max_length=255, )
    
    # criando o coluna slug na tabela Artigos, que vai receber o parametro de 
    # url que leva para o post
    # ex www.site.com/blog/meu-post O 'meu-post' é o parametro que vai ser
    # guardado no slug.
    # essa campo só aceita letras, numeros, underlines e hifens.
    # O parametro unique=True indica que o valor que for passado ali deve ser
    # unico na tabela .
    slug = models.SlugField('caminho do link (blog/)', max_length=255, unique=True)

    # Essa coluna da tabela Artigos vai fazer referencia a uma outra tabela
    # que contem os dados do usuarios do programa.
    # O models.ForeignKey nos permite a cria colunas que referenciam a outras
    # tabelas.
    # Nesse caso, a coluna vai ser mapeado como autor_id e vai guardar o id do
    # autor do artigo.
    # O primeiro argumento passado foi o user que é utilizado para indicar a
    # tabela estrangeira que será referenciada e o argumento on_delete indica
    # o que vai acontecer se a chave estrangeira for deletada, com o 
    # model.CASCADE indica que o artigo, nesse caso, também sera deletado.
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Cria o campo que será armazenado o conteudo do artigo, o TextField é
    # ideal para isso por não necessitar de um numero maximo de caracters
    # como é o caso do CharField 
    corpo = models.TextField()

    # Cria o campo do tipo datetime que armazena o dia e hora da publicação
    # o parametro auto_now_add=True indica que o dia e hora sera adicionado
    # automaticamente quando o artigo for criado.
    criado = models.DateTimeField(auto_now_add=True)

    # Cria o campo que vai armazenar o dia e hora das atualizações dos 
    # artigos.
    # o auto_now=True indica que a cada modificação será setado um novo dia
    # e horario, mas mantem o valor da coluna criado inalterado. 
    atualizado = models.DateTimeField(auto_now=True)

    # Essa classe faz com que os dados sejam apresentado na ordem inversa do
    # atrbuto 'criado' devido o sinal de negativo na frente do criado
    class Meta:
        ordering = ('-criado',)

    def __str__(self):
        return self.titulo

    def url_absoluta(self):
        """
        Essa função gera as urls para o artigo usando o atributo slug
        """
        return reverse('blog:detalhe', kwargs={'slug':self.slug})


