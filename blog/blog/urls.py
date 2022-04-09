# Nesse arquivo que foi criado por mim vou definir as urls e direcionalas para
# as views corretas
 
from django.urls import path
from . import views

# marca com o nome blog todos os padroes de urls definida nesse arquivo 
app_name = 'blog'

# link a url com a view e da um nome especifica para url com name=<nome> que pode ser acessada
# depois com blog:<nome url>
# Como as views foram criadas através de classes é necessario chamar a função
# as_view() para que funcione, caso as views sejam feitas por funções não há 
# a necessidade. 
urlpatterns = [
    path('', views.ArtigoListaView.as_view(), name='lista'),
    path('<slug:slug>', views.ArtigoDetalheView.as_view(), name='detalhe')
]
