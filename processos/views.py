from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
# from . import models
# import calendar
# import itertools


# Create your views here.

def home(request):
    cliente = Cliente.objects.all()
    form = ClienteForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado com sucesso')
            return redirect('home')

    context = {

        'form': form,
        'cliente': cliente
    }
    return render(request,'home.html',context)

def cliente(request):
    cliente = Cliente.objects.all()
    form = ClienteForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado com sucesso')
            return redirect('cliente')

    context = {

        'form': form,
        'cliente':cliente
    }

    return render(request, 'cliente.html', context)

def cliente_delete(requestt,pk):
    cliente = get_object_or_404(Cliente,pk=pk)
    cliente.delete()
    return redirect('cliente')

def cliente_edit(request, pk):

    q = get_object_or_404(Cliente, pk=pk)

    form = ClienteForm(request.POST or None, instance=q)

    if form.is_valid():
        form.save()
        return redirect('cliente')

    context = {
        'form': form,
        'id': pk
    }

    return render(request, 'cliente_edit.html', context)

def fornecedor(request):
    fornecedor = Fornecedor.objects.all()
    form = FornecedorForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado com sucesso')
            return redirect('fornecedor')

    context = {

        'form': form,
        'fornecedor':fornecedor
    }

    return render(request, 'fornecedor.html', context)

def fornecedor_delete(requestt,pk):
    fornecedor = get_object_or_404(Fornecedor,pk=pk)
    fornecedor.delete()
    return redirect('fornecedor')

def fornecedor_edit(request, pk):

    q = get_object_or_404(Funcionario, pk=pk)

    form = FornecedorForm(request.POST or None, instance=q)

    if form.is_valid():
        form.save()
        return redirect('fornecedor')

    context = {
        'form': form,
        'id': pk
    }

    return render(request, 'fornecedor_edit.html', context)

def funcionario(request):
    funcionario = Funcionario.objects.all()
    form = FuncionarioForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado com sucesso')
            return redirect('funcionario')

    context = {

        'form': form,
        'funcionario':funcionario
    }

    return render(request, 'funcionario.html', context)

def funcionario_delete(requestt,pk):
    funcionario = get_object_or_404(Funcionario,pk=pk)
    funcionario.delete()
    return redirect('funcionario')

def funcionario_edit(request, pk):

    q = get_object_or_404(Funcionario, pk=pk)

    form = FuncionarioForm(request.POST or None, instance=q)

    if form.is_valid():
        form.save()
        return redirect('funcionario')

    context = {
        'form': form,
        'id': pk
    }

    return render(request, 'funcionario_edit.html', context)


def produto(request):
    produto = Produto.objects.all()
    form = ProdutoForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado com sucesso')
            return redirect('produto')

    context = {

        'form': form,
        'produto':produto
    }

    return render(request, 'produto.html', context)

def produto_delete(requestt,pk):
    produto = get_object_or_404(Produto,pk=pk)
    produto.delete()
    return redirect('produto')

def produto_edit(request, pk):

    q = get_object_or_404(Produto, pk=pk)

    form = ProdutoForm(request.POST or None, instance=q)

    if form.is_valid():
        form.save()
        return redirect('produto')

    context = {
        'form': form,
        'id': pk
    }

    return render(request, 'produto_edit.html', context)


def estoque(request):
    estoque = Estoque.objects.all()
    form = EstoqueForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado com sucesso')
            return redirect('estoque')

    context = {

        'form': form,
        'estoque':estoque
    }

    return render(request, 'estoque.html', context)

def estoque_delete(requestt,pk):
    estoque = get_object_or_404(Estoque,pk=pk)
    estoque.delete()
    return redirect('estoque')

def estoque_edit(request, pk):

    q = get_object_or_404(Estoque, pk=pk)

    form = EstoqueForm(request.POST or None, instance=q)

    if form.is_valid():
        form.save()
        return redirect('estoque')

    context = {
        'form': form,
        'id': pk
    }

    return render(request, 'estoque_edit.html', context)

def compra(request):
    compra = Compra.objects.all()
    form = CompraForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado com sucesso')
            return redirect('compra')

    context = {

        'form': form,
        'compra':compra
    }

    return render(request, 'compra.html', context)

def compra_delete(requestt,pk):
    compra = get_object_or_404(Compra,pk=pk)
    compra.delete()
    return redirect('compra')

def compra_edit(request, pk):

    q = get_object_or_404(Compra, pk=pk)

    form = CompraForm(request.POST or None, instance=q)

    if form.is_valid():
        form.save()
        return redirect('compra')

    context = {
        'form': form,
        'id': pk
    }

    return render(request, 'compra_edit.html', context)

def tarefas(request):
    tarefas = Tarefas.objects.all()
    form = TarefasForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado com sucesso')
            return redirect('tarefas')

    context = {

        'form': form,
        'tarefas':tarefas
    }

    return render(request, 'tarefas.html', context)

def tarefas_delete(requestt,pk):
    tarefas = get_object_or_404(Tarefas,pk=pk)
    tarefas.delete()
    return redirect('tarefas')

def tarefas_edit(request, pk):

    tarefas = get_object_or_404(Tarefas, pk=pk)

    form = TarefasForm(request.POST or None, instance=tarefas)

    if form.is_valid():
        form.save()
        return redirect('tarefas')

    context = {
        'form': form,
        'id': pk
    }

    return render(request, 'tarefas_edit.html', context)