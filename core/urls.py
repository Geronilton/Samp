from django.urls import path
from .views import logout_view, empresa_cadastro, empresa_user, home, login_view,cadastro_user, politica_de_privacidade, termos_de_uso
from .views import pagar_assinatura,assinatura_adm,confirma_assinatura,definir_mensalidade_pago,assinaturas_assinante,mensalidades_assinantes,gerar_mensalidade,atualizar_usuario
from .views import assinar_servico, listar_servicos, cadastra_servico,dashboard,editar_infoEmpresa,servicos_empresa,deletar_servico,Editar_servico,deletar_mensalidade,atualizar_mensalidade,mensalidades,cadastra_mensalidade,deletar_assinante, atualizar_assinante,assinantes,cadastro_assinantes

urlpatterns = [
    path('',home, name='home'),
    path('dashboard/',dashboard, name='dashboard'),
    path('editar_infoEmpresa/',editar_infoEmpresa, name='editar_infoEmpresa'),
    # ------LOGIN----------------------------------
    path('login/',login_view, name='login'),
    path('logout/',logout_view, name='logout_view'),
    # ------URLS DE USUARIO E EMPRESA-------------
    path('cadastro_user/',cadastro_user, name='cadastro_user'),
    path('cadastro_user/<int:id>/',empresa_user, name='empresa_user'),
    path('empresa_cadastro',empresa_cadastro, name='empresa_cadastro'),
    path('atualizar_usuario/',atualizar_usuario, name='atualizar_usuario'),
    # ------ CRUD ASSINANTES-----------------------
    path('cadastro_assinantes/',cadastro_assinantes, name='cadastro_assinantes'),
    path('assinantes/',assinantes, name='assinantes'),
    path('atualizar_assinante/<int:id>/',atualizar_assinante, name='atualizar_assinante'),
    path('deletar_assinante/<int:id>/',deletar_assinante, name='deletar_assinante'),
    # -------URLS MENSALIDADE------------------------
    path('cadastra_mensalidade/<int:id>',cadastra_mensalidade, name='cadastra_mensalidade'),
    path('mensalidades/',mensalidades, name='mensalidades'),
    path('atualizar_mensalidade/<int:id>',atualizar_mensalidade, name='atualizar_mensalidade'),
    path('deletar_mensalidade/<int:id>',deletar_mensalidade, name='deletar_mensalidade'),
    path('definir_mensalidade_pago/<int:id>',definir_mensalidade_pago, name='definir_mensalidade_pago'),
    path('gerar_mensalidade/<int:id>',gerar_mensalidade, name='gerar_mensalidade'),
    #--------URLS USUARIO ASSINANTE-------------
    path('servicos/<int:empresa_id>',listar_servicos, name='servicos'),
    path('assinaturas_assinante/',assinaturas_assinante, name='assinaturas_assinante'),
    path('mensalidades_assinantes/',mensalidades_assinantes, name='mensalidades_assinantes'),
    path('assinar_servico/<int:servico_id>',assinar_servico, name='assinar_servico'),
    # ------CRUD SERVIÇO:USUARIO GESTOR---------
    path('cadastra_servico/',cadastra_servico, name='cadastra_servico'),
    path('servicos_empresa/',servicos_empresa, name='servicos_empresa'),
    path('Editar_servico/<int:id>',Editar_servico, name='Editar_servico'),
    path('deletar_servico/<int:id>',deletar_servico, name='deletar_servico'),
    # ------URLS ASSINATURA---------------------
    path('assinatura/<int:assinatura_id>/pagar/',pagar_assinatura, name='pagar_assinatura'),
    path('assinaturas/',assinatura_adm, name='assinatura_adm'),
    path('confirma_assinatura/<int:id>',confirma_assinatura, name='confirma_assinatura'),
    # -----DOCUMENTOS--------------------------
    path('termos-de-uso/', termos_de_uso, name='termos_de_uso'),
    path('politica-de-privacidade/', politica_de_privacidade, name='politica_de_privacidade'),

]

