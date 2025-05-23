from django.urls import path
from .views import logout_view,deletar_mensalidade,atualizar_mensalidade,mensalidades,cadastra_mensalidade,deletar_assinante, atualizar_assinante,assinantes,cadastro_assinantes, empresa_cadastro, empresa_user, home, login_view,cadastro_user, assinar_servico, listar_servicos, cadastra_servico, dashboard_user,dashboard,editar_infoEmpresa,servicos_empresa,deletar_servico,Editar_servico,politica_de_privacidade, termos_de_uso

urlpatterns = [
    path('',home, name='home'),
    path('empresa_cadastro',empresa_cadastro, name='empresa_cadastro'),
    path('dashboard/',dashboard, name='dashboard'),
    path('editar_infoEmpresa/',editar_infoEmpresa, name='editar_infoEmpresa'),

    path('login/',login_view, name='login'),
    path('logout/',logout_view, name='logout_view'),

    path('cadastro_user/',cadastro_user, name='cadastro_user'),
    path('cadastro_user/<int:id>/',empresa_user, name='empresa_user'),
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
    
    path('assinar_servico/<int:servico_id>',assinar_servico, name='assinar_servico'),
    path('servicos/<int:empresa_id>',listar_servicos, name='servicos'),
    path('cadastra_servico/',cadastra_servico, name='cadastra_servico'),
    path('dashboardUser/',dashboard_user, name='dashboardUser'),
    path('servicos_empresa/',servicos_empresa, name='servicos_empresa'),
    path('Editar_servico/<int:id>',Editar_servico, name='Editar_servico'),
    path('deletar_servico/<int:id>',deletar_servico, name='deletar_servico'),
    
    path('termos-de-uso/', termos_de_uso, name='termos_de_uso'),
    path('politica-de-privacidade/', politica_de_privacidade, name='politica_de_privacidade'),

]

