from django.urls import path
from . import views

app_name = 'cardapio'

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>/', views.detalhe, name='detalhe'),
    path('<slug:slug>/favorito', views.favorito, name='favorito'),
    path('favoritos', views.favoritos, name='favoritos'),
]