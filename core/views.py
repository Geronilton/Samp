from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .models import Empresas, Assinantes, Mensalidades, Servico, Assinatura,Usuario
from .forms import EmpresasForm,AssinantesForm,MensalidadesForm,UserForm, ServicoForm, PesquisaEmpresaForm,PesquisaForm
from .utils.criar_mensalidade_para_assinatura import criar_mensalidade_para_assinatura,primeira_mensalidade_para_assinatura
from django.db.models import Q
from .utils.pix_qrcode import Payload
from django.utils.timezone import now
from datetime import date
import base64


@login_required
def dashboard(request):
    empresa = request.user.empresa
    context = {
        'empresa':empresa
    }   
    return render(request, 'dashboard.html', context)

def home(request):
    form = PesquisaEmpresaForm(request.GET or None)
    empresas = Empresas.objects.all()
    if form.is_valid():
        termo = form.cleaned_data.get('busca')
        if termo:
            empresas = empresas.filter(
                Q(nome__icontains=termo) |
                Q(categoria__icontains=termo) |
                Q(endereco__icontains=termo)
            )
    context = {
        'empresas': empresas,
        'form': form,
    }
    return render(request, 'empresas.html', context)

@login_required
def editar_infoEmpresa(request):
    empresa = request.user.empresa
    if request.user.tipo_usuario != 'admin':
        return redirect('home')
    form = EmpresasForm(request.POST or None, instance=empresa)
    if form.is_valid():
        form.save()
        return redirect('dashboard')  
    context = {
        'form': form,
        'empresa': empresa
    }

    return render(request, 'form_empresa.html', context)

def pagar_assinatura(request, assinatura_id):
    assinatura = Assinatura.objects.get(id=assinatura_id)
    servico = assinatura.servico
    empresa = servico.empresa
#Nome do usuario da empresa.
    # gestor = Usuario.objects.filter(empresa=empresa, tipo_usuario='admin').first()
    # nome_gestor = gestor.get_full_name() if gestor else 'Gestor'
    # print(f"Gestor: {nome_gestor}")
    # print(empresa.nome, servico.valor, empresa.chave_pix)
    chave_copia_e_cola, qr_image = Payload(
        nome=empresa.nome,
        chavepix=empresa.chave_pix,
        valor=str(assinatura.valor),
        cidade=empresa.cidade,
        txtId=f"Assinatura{assinatura.id}"
    )
    img_base64 = base64.b64encode(qr_image.getvalue()).decode('utf-8')
    img_data = f"data:image/png;base64,{img_base64}"
    contexto = {
        "qrcode_base64": img_data,
        "chave_copia_e_cola": chave_copia_e_cola,
        "assinatura": assinatura
    }
    return render(request, "pagamento.html",contexto)

# ----------VIEWS MENSALIDADES---------
@login_required
def deletar_mensalidade(request, id):
    if request.user.tipo_usuario != 'admin':
        return redirect('home')
    mensalidade = Mensalidades.objects.get( pk=id)
    mensalidade.delete()
    return redirect('mensalidades')

@login_required
def atualizar_mensalidade(request, id):
    if request.user.tipo_usuario != 'admin':
        return redirect('home')
    mensalidade = Mensalidades.objects.get(pk=id)
    form = MensalidadesForm(request.POST or None, instance=mensalidade)
    if form.is_valid():
        form.save()
        return redirect('mensalidades')
    contexto = {
        'form': form
    }
    return render(request, 'cadastro_mensalidade.html',contexto)

@login_required
def mensalidades(request):
    empresa = request.user.empresa
    if request.user.tipo_usuario != 'admin':
        return redirect('home')
    form = PesquisaForm(request.GET or None)
    if not empresa:
        return render(request, 'mensalidades.html', {
            'mensalidades': [],
            'erro': 'Usuário sem empresa vinculada.',
            'form': form
        })
    mensalidades = Mensalidades.objects.filter(
        assinatura__servico__empresa=empresa
    ).select_related('assinatura', 'assinatura__servico', 'assinatura__assinante')
    if form.is_valid():
        termo = form.cleaned_data.get('busca')
        if termo:
            mensalidades = mensalidades.filter(
                Q(assinatura__assinante__nome__icontains=termo) |
                Q(assinatura__servico__nome__icontains=termo) |
                Q(status__icontains=termo)
            )
    contexto = {
        'mensalidades': mensalidades,
        'form': form
    }
    return render(request, 'mensalidades.html', contexto)

@login_required
def cadastra_mensalidade(request, id):
    if request.user.tipo_usuario != 'admin':
        return redirect('home')
    assinante = Assinantes.objects.get(pk=id)
    form = MensalidadesForm(request.POST or None)
    if form.is_valid():
        mensalidade = form.save(commit=False)
        mensalidade.assinantes = assinante
        mensalidade.save()
        return redirect('mensalidades')
    contexto = {
        'form': form
    }
    return render(request, 'cadastro_mensalidade.html',contexto)

# ---------VIEWS ASSINANTE------------
@login_required
def deletar_assinante(request, id):
    if request.user.tipo_usuario != 'admin':
        return redirect('home')
    assinante = Assinantes.objects.get(pk=id)
    assinante.delete()
    return redirect('assinantes')

@login_required
def atualizar_assinante(request, id):
    if request.user.tipo_usuario != 'admin':
        return redirect('home')
    empresa = request.user.empresa
    assinante = Assinantes.objects.get(pk=id)
    form = AssinantesForm(request.POST or None, instance=assinante)
    if form.is_valid():
        assinante = form.save(commit=False)
        assinante.empresa = empresa
        assinante.save()
        return redirect('assinantes')
    context = {
        'form': form,
    }

    return render(request, 'assinantes_cadastro.html', context)

@login_required
def assinantes(request):
    if request.user.tipo_usuario != 'admin':
        return redirect('home')
    empresa = request.user.empresa
    form = PesquisaForm(request.GET or None)
    assinantes = Assinantes.objects.filter(empresa=empresa)
    if form.is_valid():
        termo = form.cleaned_data.get('busca')
        if termo:
            assinantes = assinantes.filter(nome__icontains=termo)
    contexto = {
        'assinantes': assinantes,
        'form': form
    }
    return render(request, 'assinantes.html', contexto)

@login_required
def cadastro_assinantes(request):
    if request.user.tipo_usuario != 'admin':
        return redirect('home')
    empresa = request.user.empresa
    form = AssinantesForm(request.POST or None)
    if form.is_valid():
        assinante = form.save(commit=False)
        assinante.empresa = empresa
        assinante.save()
        return redirect('assinantes')
    context = {
        'form': form,
    }

    return render(request, 'assinantes_cadastro.html', context)

# --------VIEWS SERVIÇO GESTOR----------
@login_required
def servicos_empresa(request):
    if request.user.tipo_usuario != 'admin':
        return redirect('home')
    empresa = request.user.empresa
    servicos = Servico.objects.filter(empresa=empresa)
    context = {
        'servicos':servicos
    }
    return render(request, 'servico_list.html', context)

@login_required
def Editar_servico(request, id):
    if request.user.tipo_usuario != 'admin':
        return redirect('home')
    empresa = request.user.empresa
    servico = get_object_or_404(Servico, pk=id, empresa=empresa)  
    form = ServicoForm(request.POST or None, instance=servico)
    if form.is_valid():
        form.save()
        return redirect('servicos_empresa')
    context = {'form': form}
    return render(request, 'servico_cadastro.html',context )

@login_required
def deletar_servico(request, id):
    if request.user.tipo_usuario != 'admin':
        return redirect('home')
    empresa = request.user.empresa
    servico = get_object_or_404(Servico, pk=id, empresa=empresa) 
    servico.delete()
    return redirect('servicos_empresa')

@login_required
def cadastra_servico(request):
    if request.user.tipo_usuario != 'admin':
        return redirect('home')
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            servico = form.save(commit=False)
            servico.empresa = request.user.empresa
            servico.save()
            return redirect('servicos', empresa_id=request.user.empresa.id)
    else:
        form = ServicoForm()
    context ={
        'form':form
    }
    return render(request, 'servico_cadastro.html', context)

# -------VIEWS ASSINATURA GESTOR-----------
@login_required
def assinatura_adm(request):
    if request.user.tipo_usuario != 'admin':
        return redirect('home')
    empresa = request.user.empresa
    form = PesquisaForm(request.GET or None)
    assinaturas = Assinatura.objects.filter(servico__empresa=empresa)
    if form.is_valid():
        termo = form.cleaned_data.get('busca')
        if termo:
            assinaturas = assinaturas.filter(
                Q(assinante__nome__icontains=termo) |
                Q(servico__nome__icontains=termo) |
                Q(status__icontains=termo)
            )
    contexto={
        'assinaturas':assinaturas,
        'form':form
    }
    return render(request,'assinaturas.html', contexto)

@login_required
def confirma_assinatura(request, id):
    if request.user.tipo_usuario != 'admin' or not request.user.empresa:
        messages.error(request, "Você não tem permissão para realizar esta ação.")
        return redirect('assinatura_adm')
    assinatura = get_object_or_404(Assinatura, id=id)
    if assinatura.servico.empresa != request.user.empresa:
        messages.error(request, "Você só pode confirmar assinaturas da sua empresa.")
        return redirect('assinatura_adm')
    assinatura.status = "Ativa"
    assinatura.save()
    primeira_mensalidade_para_assinatura(assinatura)
    messages.success(request, f"Assinatura #{assinatura.id} ativada com sucesso!")
    return redirect('assinatura_adm')

@login_required
def definir_mensalidade_pago(request,id):
    if request.user.tipo_usuario != 'admin' or not request.user.empresa:
        messages.error(request, "Você não tem permissão para realizar esta ação.")
        return redirect('mensalidades')
    mensalidade = get_object_or_404(Mensalidades, id=id)
    if mensalidade.assinatura.servico.empresa != request.user.empresa:
        messages.error(request, "Você só pode altera mensalidades da sua empresa.")
        return redirect('mensalidades')
    mensalidade.status = 'pago'
    mensalidade.data_pagamento = now()
    mensalidade.save()
    messages.success(request, f"Mensalidade de {mensalidade.assinatura.assinante.nome} paga com sucesso.")
    return redirect('mensalidades')

def gerar_mensalidade(request, id):
    if request.user.tipo_usuario != 'admin' or not request.user.empresa:
        messages.error(request, "Você não tem permissão para realizar esta ação.")
        return redirect('assinatura_adm')
    assinatura = get_object_or_404(Assinatura, id=id)
    if assinatura.servico.empresa != request.user.empresa:
        messages.error(request, "Você só pode gerar mensalidades dos seus serviços.")
        return redirect('assinatura_adm')
    ultima_mensalidade = Mensalidades.objects.filter(assinatura=assinatura).order_by('-vencimento').first()
    if ultima_mensalidade and ultima_mensalidade.vencimento >= date.today():
        messages.warning(request, "Ainda não é possível gerar uma nova mensalidade. A última ainda não venceu.")
        return redirect('mensalidades')

    criar_mensalidade_para_assinatura(assinatura)
    messages.success(request, f"Mensalidade gerada com sucesso para a assinatura #{assinatura.id}.")
    return redirect('mensalidades')

#---------- Usuario assinante----------------
def listar_servicos(request, empresa_id):
    empresa = get_object_or_404(Empresas, id=empresa_id)
    servicos = Servico.objects.filter(empresa=empresa)
    context = {
        'servicos':servicos
    }
    return render(request, 'servico.html', context)

def assinar_servico(request, servico_id):
    if not request.user.is_authenticated:
        return redirect('cadastro_user')
    servico = get_object_or_404(Servico, id=servico_id)
    empresa = servico.empresa

    assinante, created = Assinantes.objects.get_or_create(
        email=request.user.email,
        defaults={
            'nome': request.user.username or 'Sem nome',
            'telefone': request.user.telefone,
            'empresa': empresa
        }
    )
    assinatura_existente = Assinatura.objects.filter(
        assinante=assinante,
        servico=servico,
        status__in=['pendente', 'ativa']
    ).first()
    if assinatura_existente:
        messages.info(request, 'Você já possui uma assinatura para esse serviço.')
        return redirect('servicos', empresa_id=empresa.id)

    nova_assinatura = Assinatura.objects.create(
        assinante=assinante,
        servico=servico,
        status='pendente',
        valor=servico.valor
    )
    messages.success(request, 'Assinatura realizada com sucesso! Aguardando o pagamento.')
    return redirect('pagar_assinatura', assinatura_id=nova_assinatura.id)

def buscar_empresa(request):
    form = PesquisaEmpresaForm(request.GET or None)
    empresas = Empresas.objects.all()

    if form.is_valid():
        nome = form.cleaned_data.get('nome')
        categoria = form.cleaned_data.get('categoria')
        endereco = form.cleaned_data.get('endereco')

        if nome:
            empresas = empresas.filter(nome__icontains=nome)
        if categoria:
            empresas = empresas.filter(categoria__icontains=categoria)
        if endereco:
            empresas = empresas.filter(endereco__icontains=endereco)

    contexto = {
        'form': form,
        'empresas': empresas
    }
    return render(request, 'empresas.html', contexto)

@login_required
def atualizar_usuario(request):
    user = request.user
    if request.user.tipo_usuario != 'assinante':
        return redirect('home')
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('dashboard')  
    context = {
        'form': form,
    }

    return render(request, 'form_user_dash.html', context)

@login_required
def assinaturas_assinante(request):
    if request.user.tipo_usuario != 'assinante':
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect('home')
    try:
        assinante = Assinantes.objects.get(email=request.user.email)
    except Assinantes.DoesNotExist:
        messages.error(request, "Perfil de assinante não encontrado.")
        return redirect('home')
    form = PesquisaForm(request.GET or None)
    assinaturas = Assinatura.objects.filter(assinante=assinante)
    if form.is_valid():
        termo = form.cleaned_data.get('busca')
        if termo:
            assinaturas = assinaturas.filter(
                Q(assinante__nome__icontains=termo) |
                Q(servico__nome__icontains=termo) |
                Q(status__icontains=termo)
            )
    contexto={
        'assinaturas':assinaturas,
        'form':form
    }
    return render(request,'assinaturas.html', contexto)

@login_required
def mensalidades_assinantes(request):
    if request.user.tipo_usuario != 'assinante':
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect('home')
    try:
        assinante = Assinantes.objects.get(email=request.user.email)
    except Assinantes.DoesNotExist:
        messages.error(request, "Perfil de assinante não encontrado.")
        return redirect('home')
    
    form = PesquisaForm(request.GET or None)
    mensalidades = Mensalidades.objects.filter(assinatura__assinante=assinante)
    if form.is_valid():
        termo = form.cleaned_data.get('busca')
        if termo:
            mensalidades = mensalidades.filter(
                Q(assinatura__servico__nome__icontains=termo) |
                Q(status__icontains=termo)
            )
    contexto = {
        'mensalidades': mensalidades,
        'form': form
    }
    return render(request, 'mensalidades.html', contexto)

def termos_de_uso(request):
    return render(request, 'termos_de_uso.html')

def politica_de_privacidade(request):
    return render(request, 'politica_de_privacidade.html')

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('email')
        senha = request.POST.get('senha')
        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            contexto = {
                'erro': 'Por favor, entre com um email e senha corretos. Note que ambos os campos diferenciam maiúsculas e minúsculas.'
            }
            return render(request, 'login.html', contexto)
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def empresa_cadastro(request):
    form = EmpresasForm(request.POST or None)
    if form.is_valid():
        empresa = form.save() 
        return redirect('empresa_user', id=empresa.id)  
    context = {
        'form': form,
    }
    return render(request, 'empresa_cadastro.html', context)

def empresa_user(request, id):
    empresa = get_object_or_404(Empresas, pk=id)
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.empresa = empresa
            user.tipo_usuario = 'admin'
            user.save()
            return redirect('login') 
    else:
        form = UserForm()
        form.instance.tipo_usuario = 'admin'
    context = {
        'form': form,
        'empresa': empresa,
        'tipo_usuario': 'admin',
    }
    return render(request, 'cadastro_user.html', context)

def cadastro_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserForm()
    context = {
        'form' : form
    }
    return render(request, 'cadastro_user.html', context )
