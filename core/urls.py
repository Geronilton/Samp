from django.urls import path
from .views import deletar_mensalidade,atualizar_mensalidade,mensalidades,cadastra_mensalidade,deletar_assinante, atualizar_assinante,assinantes,cadastro_assinantes, empresa_cadastro, empresas, empresa_user, home, login_view

urlpatterns = [
    path('',empresa_cadastro, name='empresa_cadastro'),
    path('home/',home, name='home'),
    path('login/',login_view, name='login'),
    path('empresas/',empresas, name='empresas'),
    path('empresa_user/<int:id>/',empresa_user, name='empresa_user'),
    # ------ CRUD ASSINANTES---------
    path('cadastro_assinantes/',cadastro_assinantes, name='cadastro_assinantes'),
    path('assinantes/',assinantes, name='assinantes'),
    path('atualizar_assinante/<int:id>/',atualizar_assinante, name='atualizar_assinante'),
    path('deletar_assinante/<int:id>/',deletar_assinante, name='deletar_assinante'),
    # -------------------------------
    path('cadastra_mensalidade/<int:id>',cadastra_mensalidade, name='cadastra_mensalidade'),
    path('mensalidades/',mensalidades, name='mensalidades'),
    path('atualizar_mensalidade/<int:id>',atualizar_mensalidade, name='atualizar_mensalidade'),
    path('deletar_mensalidade/<int:id>',deletar_mensalidade, name='deletar_mensalidade'),

]

