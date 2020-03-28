from django.db.models import Count, Model
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
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

@login_required
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

@login_required
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





@login_required
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
@login_required
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


@login_required
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

@login_required
def cliente_delete(request, pk):
    cliente = Cliente.objects.get(pk=pk)
    cliente.delete()
    messages.error(request, 'Cadastro removido com sucesso')

    return redirect('cliente')

@login_required
def produto(request):
    produto = Produto.objects.all()
    form = ProdutoForm(request.POST)

    print(produto)
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

@login_required
def produto_delete(requestt,pk):
    produto = get_object_or_404(Produto,pk=pk)
    produto.delete()
    return redirect('produto')

@login_required
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



@login_required
def estoque(request):
    #produto = Produto.objects.values('nomeproduto')
    #lote = Lote.objects.select_related('produto').values('produto__nomeproduto').annotate(quantLote = Sum('quantLote'))
    #compra = Compra.objects.select_related('produto').values('Produto__nomeproduto').annotate(quantCompra = Sum('quantCompra'))

  #  estoque = Compra.objects.select_related('Lote')
    #estoque = Produto.objects.raw('SELECT * FROM processos_produto')

    lote = Compra.objects.raw("SELECT DISTINCT id, nomeproduto,Sum(lote) as lote,Sum(compra) as compra, "
                              " (Sum(lote)-Sum(compra)) as total "
                              "from (Select DISTINCT pp.id, pp.nomeproduto ,NULL as Lote, Sum(pc.quantCompra) as compra "
                              "from processos_produto pp join processos_compra pc "
                              "where pp.id = pc.Produto_id GROUP by pp.nomeproduto UNION "
                              "select DISTINCT pp.id, pp.nomeproduto, Sum(pl.quantlote) as lote, NULL from processos_lote pl "
                              "join processos_produto pp where pp.id = pl.produto_id "
                              "group by pp.nomeproduto ) GROUP by nomeproduto")


    estoque = Estoque.objects.all()

    form = EstoqueForm(request.POST)


    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado com sucesso')
            return redirect('estoque')

    context = {

        'form': form,
        'estoque':estoque,
        'lote':lote
    }



    return render(request, 'estoque.html', context)




@login_required
def compra(request):
    compra = Compra.objects.raw("SELECT DISTINCT pcl.id,pcl.nome, pp.nomeproduto,pc.quantcompra,"
                                "(pp.valor*pc.quantCompra)as valor, pc.Data FROM processos_compra pc "
                                "join processos_cliente pcl join processos_produto pp "
                                "where pcl.id = pc.Cliente_id and pp.id = pc.Produto_id")

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


@login_required
def compra_delete(request,pk):
    compra = get_object_or_404(Compra,pk=pk)
    compra.delete()
    return redirect('compra')


@login_required
def compra_edit(request, pk):

    compra = get_object_or_404(Compra, pk=pk)

    form = CompraForm(request.POST or None, instance=compra)

    if form.is_valid():
        form.save()
        return redirect('compra')

    context = {
        'form': form,
        'compra': compra
    }

    return render(request, 'compra_edit.html', context)



@login_required
def lote(request):
    lote = Lote.objects.all()
    form = LoteForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado com sucesso')
            return redirect('lote')

    context = {

        'form': form,
        'lote':lote
    }

    return render(request, 'lote.html', context)

@login_required
def lote_delete(request,pk):
    lote = get_object_or_404(Lote,pk=pk)
    lote.delete()
    return redirect('lote')

@login_required
def lote_edit(request, pk):

    lote = get_object_or_404(Lote, pk=pk)

    form = LoteForm(request.POST or None, instance=lote)

    if form.is_valid():
        form.save()
        return redirect('lote')

    context = {
        'form': form,
        'lote': lote
    }

    return render(request, 'lote_edit.html', context)


