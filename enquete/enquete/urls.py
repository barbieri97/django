# Esse arquivo não vem por padrão no Django, eu quem criei.

# Esse módulo permite lincar o caminho que passamos para a view que desejamos
from django.urls import path

# importa a view que acabamos de criar
from . import views

# Essa variavel atribui nome a todas as urls desse app permitindo acessar
# essas urls com 'enquete:index' por exemplo. 
app_name='enquete'

# Define a variavel onde o django vai procurar os padrões de url que recebe.
# Essa variavel recebe uma lista que contem os padroes das urls a view a que
# se refere e o nome da url tudo isso dentro da função path() 
urlpatterns = [

    # O primeiro argumento é o padrão da url, o segundo a view que deve ser
    # atribuida ao padrão e o name para identificar a url 
    # Como a view é uma classe agora, é necessario chamar a função as_view()
    # para funcionar
    path('', views.ViewIndex.as_view(), name='index'),

    #defini o padrão de url para acessar a view detalhe
    # o primeiro argumento '<int:id_questao>' indica que será recebido um
    # valor pela url e esse valor sera um int e o nome dessa variavel vai ser
    # id_questao, essa variavel que será recebida como parametro nas nossas
    # views 
    path('<int:pk>/', views.ViewDetalhe.as_view(), name='detalhe'),

    # define o padrão de url para acessar a view resultado
    path('<int:pk>/resultado', views.ViewResultado.as_view(), name='resultado'),

    # define o padrão de url para acessar a view vote
    path('<int:id_pergunta>/vote', views.vote, name='vote')
]
