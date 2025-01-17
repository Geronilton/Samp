from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .models import Empresas, Assinantes, Mensalidades
from .forms import EmpresasForm, EmpresaUserForm,AssinantesForm,MensalidadesForm

# Create your views here.
@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def deletar_mensalidade(request, id):
    mensalidade = Mensalidades.objects.get( pk=id)
    mensalidade.delete()
    return redirect('mensalidades')

@login_required
def atualizar_mensalidade(request, id):
    mensalidade = Mensalidades.objects.get(pk=id)
    form = MensalidadesForm(request.POST or None, instance=mensalidade)
    if form.is_valid():
        mensalidade.save()
        return redirect('mensalidades')
    contexto = {
        'form': form
    }
    return render(request, 'cadastro_mensalidade.html',contexto)

@login_required
def mensalidades(request):
    empresa = request.user.empresa 
    mensalidades = Mensalidades.objects.filter(assinantes__empresa=empresa)
    contexto = {
        'mensalidades':mensalidades
    }
    return render(request, 'mensalidades.html', contexto)

@login_required
def cadastra_mensalidade(request, id):
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

@login_required
def deletar_assinante(request, id):
    assinante = Assinantes.objects.get(pk=id)
    assinante.delete()
    return redirect('assinantes')

@login_required
def atualizar_assinante(request, id):
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
    empresa = request.user.empresa 
    assinantes = Assinantes.objects.filter(empresa=empresa)
    contexto = {
        'assinantes': assinantes
    }
    return render(request, 'assinantes.html', contexto)

@login_required
def cadastro_assinantes(request):
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
        form = EmpresaUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.empresa = empresa
            user.save()
            return redirect('login') 
    else:
        form = EmpresaUserForm()
    context = {
        'form': form,
        'empresa': empresa,
    }
    return render(request, 'empresa_user.html', context)

def empresas (request):
    empresas = Empresas.objects.all()
    context = {
        'empresas': empresas
    }

    return render(request, 'empresas.html', context)
