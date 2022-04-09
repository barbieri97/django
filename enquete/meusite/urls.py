"""meusite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # importa o include para poder referenciar as urls do nosso app

urlpatterns = [
    path('admin/', admin.site.urls),

    # adiciona um padrão de url que vai levar para a nosso app.
    # usa-se o include('enquete.urls') para indicar que sempre que receber
    # uma requisição com o padrão definido ele vá buscar as urls e as views
    # em enquete/urls.py que criamos a pouco
    # para isso ele corta a url até o padrão que definimos no primeiro
    # argumento e envia o restante para enquete/urls.py 
    # inclui o parametro namespace='enquete' para me referir a essa url com
    # maior facilidade
    path('enquete/', include('enquete.urls', namespace='enquete')), 
]
