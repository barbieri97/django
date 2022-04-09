from django.http import response
from django.test import TestCase

# O que foi feito abaixo desse ponto foi meu código e acima veio
# automaticamente com o Django

# importando bibliotecas para trablahar com datas
from datetime import timedelta
from django.utils import timezone

# importa o modulo para gerar as urls dinamicamente
from django.urls import reverse

# importando os modelos que criei
from .models import Pergunta

# criando uma classe que tera os testes do modelo Pergunta
# essa classe herda a classe TestCase
class TesteModeloPergunta(TestCase):

    # teste que vai verificar a funcionalidade do método 
    # foi_publicado_recentemente()
    # todas as funções de testes devem começar com 'test'
    def teste_foi_publicado_recentemente_com_pergunta_futura(self):
        """
        Verifica se o método retorna falso para uma pergunta com a data de 
        publicação no futuro
        """

        # define a data para a publicação em 30 dias a frente
        time = timezone.now() + timedelta(days=30)
        
        #cria a pergunta futura
        pergunta_futura = Pergunta(data_publi=time)

        # Algo interessante sobre os teste é que ele cria um database
        # particular para os teste, logo você deve criar os dados do databse
        # para ser testado, como fiz acima.
        # isso é interessante pois preserva os dados reais do banco de dados

        # Aqui o teste ocorre de fato
        # verifica se o retorno do primeiro argumento é igual ao segundo
        # argumento
        self.assertIs(pergunta_futura.foi_publicado_recentemente(), False)

        # Esse teste verifica se passado 1 segundo do dia, a funçao já retorna
        # False
    def teste_foi_publicado_recentemente_com_questao_passada(self):
        """
        Verifica se o método retorna falso para uma pergunta com a data de 
        publicação passado um dia e um segundo
        """
        
        # define a data de publicação para um dia e um segundo atrás
        time = timezone.now() - timedelta(days=1, seconds=1)

        # cria o objeto Pergunta com a data de publicação de 'time'
        pergunta_antiga = Pergunta(data_publi=time)
        
        # Faz o teste
        self.assertIs(pergunta_antiga.foi_publicado_recentemente(), False)


    def teste_foi_publicado_recentemente_com_perguntarecente(self):
        """
        Verifica se o método retorna True para uma pergunta com a data de 
        publicação dentro de um dia
        """
        # define uma data de 23h 59m 59s atrás
        time = timezone.now() - timedelta(hours=23,minutes=59, seconds=59)

        # cria o objeto Pergunta com a data de publicação igual a 'time'
        pergunta_recente =  Pergunta(data_publi=time)

        # faz o teste
        self.assertIs(pergunta_recente.foi_publicado_recentemente(), True)

# cria uma função para facilitar a criação de objetos Pergunta
def criar_pergunta(texto_pergunta, dias):
    """
    essa função cria objetos do tipo pergunta com o texto da publicação
    e data da publicação que forem passadas. a data de publicação difere 
    somente em dias
    """
    time = timezone.now() + timedelta(days=dias)
    return Pergunta.objects.create(texto_pergunta=texto_pergunta, data_publi=time)

# essa classe vai realizar testes da view index
class TesteIndexView(TestCase):

    # vai testar se devolve a mensagem de erro esperado caso não tenha questões
    def teste_sem_questões(self):
        """
        Verifica se a view retorna a mensagemde erro esperado caso não tenha
        questoes
        """
        
        # o client.get() é um modulo de TestCase que permite verificar o 
        # comportamento do site sob a perspectiva de experiencia do usuario
        # essa fuinção recebe como parametro uma url e devolve a resposta da 
        # requisição
        resposta = self.client.get(reverse('enquete:index'))

        #verificar se a requisição teve status code igual a 200
        self.assertEqual(resposta.status_code, 200 )

        # verifica se o conteudo da resposta foi igual a mensagem de erro
        # esperado
        self.assertContains(resposta, 'nenhuma pergunta foi encontrada')

        # Verfica se a variavel de contexto esta vazia
        self.assertQuerysetEqual(resposta.context['ultimas_perguntas'], [])

    # testa se as perguntas passadas vão aparecer na view
    def teste_pergunta_passada(self):

        # cria um objeto Pergunta com data no passado
        pergunta = criar_pergunta('questao passada', -30)

        # faz a requisição para a view
        resposta = self.client.get(reverse('enquete:index'))

        # verifica se a variavel de contexto é igual a perguta que criamos
        self.assertQuerysetEqual(resposta.context['ultimas_perguntas'], [pergunta],)

    # testa se perguntas futuras não aparecem
    def teste_pergunta_futura(self):
        """
        verifica se perguntas futuras com data de publicação futura não
        aparecem
        """
        # cria objeto Perguntas com data de publicação para 30 dias 
        pergunta = criar_pergunta('pergunta futura', 30)

        # faz requisição para a url 'index'
        resposta = self.client.get(reverse('enquete:index'))

        # testa se o conteudo é igua a mensagem de erro esperado
        self.assertContains(resposta, 'nenhuma pergunta foi encontrada')

        # Testa se a variavel de contexto esta vazia
        self.assertQuerysetEqual(resposta.context['ultimas_perguntas'], [])

    # Testa se duas perguntas no passado apareceme
    def teste_duas_passadas(self):

        # cria dois objetos pergunta um com 30 dias passados e outro com
        # 5 dias passados
        pergunta1 = criar_pergunta('pergunta 1', -30)
        pergunta2 = criar_pergunta('pergunta 2', -5)

        # faz a requisição para a url 'index'
        resposta = self.client.get(reverse('enquete:index'))

        # verifica se a variavel de contexto contem as duas questoes
        self.assertQuerysetEqual(resposta.context['ultimas_perguntas'], [
            pergunta2,
            pergunta1
        ])

    def teste_duas_passadas(self):
        # cria varios objetos pergunta um com data de publicação no passado
        # e verifica se só os 5 ultimos aparecem
        pergunta1 = criar_pergunta('pergunta 1', -30)
        pergunta2 = criar_pergunta('pergunta 2', -25)
        pergunta3 = criar_pergunta('pergunta 3', -20)
        pergunta4 = criar_pergunta('pergunta 4', -15)
        pergunta5 = criar_pergunta('pergunta 5', -10)
        pergunta6 = criar_pergunta('pergunta 6', -5)
        
        # faz a requisição para a url 'index'
        resposta = self.client.get(reverse('enquete:index'))
        
        # verifica se a variavel de contexto contem as duas questoes
        self.assertQuerysetEqual(resposta.context['ultimas_perguntas'], [
            pergunta6,
            pergunta5,
            pergunta4,
            pergunta3,
            pergunta2,
        ])

# Testes para a view 'detalhe'
class TesteViewDetalhe(TestCase):

    # Testa se a view detalhe mostra perguntas que não foram publicadas ainda
    def teste_questao_futura(self):
        """
        Verifica se ao ser requisitado detalhes de Perguntas ainda não
        publicadas a view retorna um 404
        """
        
        # cria um objeto pergunta com a data de publicação para 5 dias
        pergunta_futura = criar_pergunta('pergunta futura', 5)

        # faz a requisição para a view 'detalhe'
        resposta = self.client.get(reverse('enquete:detalhe', args=(pergunta_futura.id,)))

        # testa se o status code é 404
        self.assertEqual(resposta.status_code, 404)
 
    # Testa se a view detalhe mostra perguntas ja publicadas
    def teste_questao_passada(self):
        """
        Verifica se ao ser requisitado detalhes de Perguntas já
        publicadas a view o texto da pergunta
        """
        
        # cria um objeto pergunta com a data de publicação para 5 dias
        pergunta_passada = criar_pergunta('pergunta futura', -5)

        # faz a requisição para a view 'detalhe'
        resposta = self.client.get(reverse('enquete:detalhe', args=(pergunta_passada.id,)))

        # testa se o conteudo da resposta é igual ao atributo 'texto_pergunta'
        self.assertContains(resposta, pergunta_passada.texto_pergunta)

# Testes para a view 'resultado'
class TesteViewResultado(TestCase):

    # Testa se a view detalhe mostra perguntas que não foram publicadas ainda
    def teste_questao_futura(self):
        """
        Verifica se ao ser requisitado detalhes de Perguntas ainda não
        publicadas a view retorna um 404
        """
        
        # cria um objeto pergunta com a data de publicação para 5 dias
        pergunta_futura = criar_pergunta('pergunta futura', 5)

        # faz a requisição para a view 'detalhe'
        resposta = self.client.get(reverse('enquete:resultado', args=(pergunta_futura.id,)))

        # testa se o status code é 404
        self.assertEqual(resposta.status_code, 404)
 
    # Testa se a view detalhe mostra perguntas ja publicadas
    def teste_questao_passada(self):
        """
        Verifica se ao ser requisitado detalhes de Perguntas já
        publicadas a view o texto da pergunta
        """
        
        # cria um objeto pergunta com a data de publicação para 5 dias
        pergunta_passada = criar_pergunta('pergunta passada', -5)

        # cria um objeto resposta para o objeto pergunta e o salva
        r = pergunta_passada.resposta_set.create(texto_resposta='resposta')
        r.save()

        # faz a requisição para a view 'resultado'
        resposta = self.client.get(reverse('enquete:resultado', args=(pergunta_passada.id,)))

        # testa se o conteudo da resposta é igual ao atributo 'texto_pergunta'
        self.assertContains(resposta, r)
    




