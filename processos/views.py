from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from .models import *
from .forms import *
from django.contrib import messages
# from . import models
# import calendar
# import itertools



class usuariosUpdate(UpdateView):
    model = Usuario
    fields = ('Nome',
              'Login',
              'Situacao',
              'CPF',
              'Email',
              'Funcao',
              )
    success_url = reverse_lazy('usuarios')
    template_name = 'legacy/usuarios_edit.html'


class usuariosDelete(DeleteView):
    model = Usuario
    success_url = reverse_lazy('usuarios')
    template_name = 'legacy/usuarios_delete.html'


def usuariosEdit(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    form = UsuarioCreationForm(request.POST or None, instance=usuario)

    if form.is_valid():
        form.save()
        return redirect('usuarios')

    context = {
        'form': form,
        'usuario': usuario
    }

    return render(request, 'usuarios_edit.html', context)



def usuarios(request):
    if request.FILES:
        from .models import Importacao
        arquivo = Importacao()
        arquivo.Usuario = request.user
        arquivo.Arquivo = request.FILES['arquivo']
        arquivo.TipoArquivo = 'USUA'
        arquivo.save()
        arquivo.ProcessaArquivo()
        total = d.TotalRegistros

        messages.success(request, f'{total} usuários importados.')

        return redirect('usuarios')

    if request.POST:

        form = UsuarioCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('usuarios')
        context = {
            'Usuarios': q,
            'formusuario': form
        }

        return render(request, 'usuarios.html', context)

    form = UsuarioCreationForm()

    q = Usuario.objects.all().order_by('-id')[:100]  # ORM do Django

    ultima_imp = Usuario.objects.all().order_by('-id')[:1]

    context = {
        'Usuarios': q,
        'formusuario': form,
        'ultima_imp': ultima_imp
        # 'Filial': i,

    }

    return render(request, 'usuarios.html', context)


def editar_meus_dados(request):
    if request.method == 'POST':
        usuario = get_object_or_404(Usuario, pk=request.user.id)
        email_usuario = request.user.Email.lower()
        if request.FILES.get('usuarioFoto') != None:
            usuario.Foto = request.FILES.get('usuarioFoto')

        usuario.Nome = request.POST.get('nomeUsuario')
        usuario.Email = request.POST.get('emailUsuario')
        usuario.Celular = request.POST.get('celularUsuario')
        usuario.CPF = request.POST.get('cpfUsuario')
        usuario.RG = request.POST.get('rgUsuario')

        if request.POST.get('usuarioSenha') != None:
            usuario.Senha = request.POST.get('usuarioSenha')

        usuario.save()
        send_mail(
            'VivoX - Atualiação',
            'Você atualizou as informações do seu perfil',
            'vivox.nao-responda@gestaovivox.com.br',
            [email_usuario],
            fail_silently=False,
        )
        messages.success(request, 'Dados alterados com sucesso')

        return redirect(reverse('meusdados'))

    usuario = request.user

    context = {
        'usuario': usuario
    }

    return render(request, 'meus_dados.html', context)






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


######## Cliente

def cliente(request):
    cliente = Cliente.objects.all()
    if request.method == 'POST':
        form = ClienteForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso')
            return redirect('cliente')

    form = ClienteForm()

    context = {
        'form': form,
        'cliente': cliente
    }

    return render(request, 'cliente.html', context)



def cliente_edit(request, pk):
    cliente = Cliente.objects.get(pk=pk)

    form = ClienteForm(request.POST or None, instance=cliente)

    if form.is_valid():
        form.save()
        messages.success(request, 'Cadastro alterado com sucesso')
        return redirect('cliente')

    context = {
        'form': form,
        'cliente': cliente
    }

    return render(request, 'cliente_edit.html', context)


def cliente_delete(request, pk):
    cliente = Cliente.objects.get(pk=pk)
    cliente.delete()
    messages.error(request, 'Cadastro removido com sucesso')

    return redirect('cliente')


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