from django.urls import path
from .views import empresa_cadastro, empresas

urlpatterns = [
    path('',empresa_cadastro, name='empresa_cadastro'),
    path('empresas/',empresas, name='empresas'),

]

