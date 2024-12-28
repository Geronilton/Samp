from django.shortcuts import render, redirect
from .models import Empresas
from .forms import EmpresasForm

# Create your views here.

def empresa_cadastro (request):
    form = EmpresasForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('empresas')
    context = {
        'form': form
    }
    return render(request, 'empresa_cadastro.html',context)

def empresas (request):
    empresas = Empresas.objects.all()
    context = {
        'empresas': empresas
    }

    return render(request, 'empresas.html', context)
