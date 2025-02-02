import datetime
import decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from .forms import *
from .models import *
from . import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json




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
    template_name = 'usuarios_edit.html'


class usuariosDelete(DeleteView):
    model = Usuario
    success_url = reverse_lazy('usuarios')
    template_name = 'usuarios_delete.html'

@login_required
def usuariosEdit(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    form = UsuarioCreationForm(request.POST or None, instance=usuario)

    if form.is_valid():
        form.save()
        return redirect('usuarios')

    context = {
        'form': form,
        'usuario': usuario.id
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
    if request.method == 'POST' and request.POST.get('usuarioSenha') != None:
        usuario = get_object_or_404(Usuario, pk=request.user.id)
       # email_usuario = request.user.Email.lower()

        if request.FILES.get('usuarioFoto') != None:
            usuario.Foto = request.FILES.get('usuarioFoto')

        usuario.Nome = request.POST.get('nomeUsuario')
        usuario.Email = request.POST.get('emailUsuario')
        usuario.Celular = request.POST.get('celularUsuario')
        usuario.CPF = request.POST.get('cpfUsuario')
        usuario.RG = request.POST.get('rgUsuario')
        usuario.Senha = request.POST.get('usuarioSenha')
        usuario.save()
        print(usuario.Nome)
        print(usuario.Email)
        messages.success(request, 'Dados alterados com sucesso')

        return redirect(reverse('meusdados'))

    usuario = request.user
    context = {
        'usuario': usuario
    }

    return render(request, 'meus_dados.html', context)




def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError



@login_required
def home(request):

    estoque = Compra.objects.raw('''select distinct processos_produto.id,nomeproduto,
                                   (select sum(processos_compra."quantCompra")from processos_compra 
                                   where processos_compra."Produto_id" = processos_produto.id) 
                                   as SomaCompras, (select sum(processos_lote."quantLote")
                                   from processos_lote where processos_produto.id = processos_lote.Produto_id)
                                   as SomaLote ,((select sum(processos_lote."quantLote") from processos_lote
                                   where processos_produto.id = processos_lote.Produto_id) - (select sum(processos_compra."quantCompra")
                                   from processos_compra where processos_compra."Produto_id" = processos_produto.id )  )
                                   as total from processos_produto''')

    balanco = Balanco.objects.raw('''SELECT 1 as id,to_char(processos_balanco."datas", 'MM-YYYY') as periodo, 
                                       sum(compra) as rendimento, sum(despesa) as despesa, (sum(compra) - sum(despesa)) as total
                                         FROM public.processos_balanco GROUP BY to_char(processos_balanco."datas", 'MM-YYYY')
                                          ORDER BY to_char(processos_balanco."datas", 'MM-YYYY')''')



    nomes = [obj.nomeproduto for obj in estoque]
    total = [obj.total for obj in estoque]

    datas = [obj.periodo for obj in balanco]
    balancos = [obj.total for obj in balanco]

    rendimentos = [obj.rendimento for obj in balanco]



    context = {
        'nomes': json.dumps(nomes),
        'total': json.dumps(total),

        'datas': json.dumps(datas),
        'balancos': json.dumps(balancos, default=decimal_default),

        'rendimentos': json.dumps(rendimentos, default=decimal_default),

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

    estoque = Compra.objects.raw('''select distinct processos_produto.id,nomeproduto,
                                (select sum(processos_compra."quantCompra")from processos_compra 
                                where processos_compra."Produto_id" = processos_produto.id) 
                                as SomaCompras, (select sum(processos_lote."quantLote")
                                from processos_lote where processos_produto.id = processos_lote.Produto_id)
                                as SomaLote ,((select sum(processos_lote."quantLote") from processos_lote
                                where processos_produto.id = processos_lote.Produto_id) - (select sum(processos_compra."quantCompra")
                                from processos_compra where processos_compra."Produto_id" = processos_produto.id )  )
                                as total from processos_produto''')

    form = EstoqueForm(request.POST)

    context = {

        'form': form,
        'estoque':estoque,

    }

    return render(request, 'estoque.html', context)




@login_required
def compra(request):
    compra = Compra.objects.raw('''SELECT processos_compra.id, processos_cliente.nome, 
                                    processos_compra."Data", processos_produto.nomeproduto, 
                                    processos_produto.valor, processos_compra."quantCompra",processos_compra."Desconto",
                                   ((valor*"quantCompra") - processos_compra."Desconto" )as total FROM  public.processos_compra, 
                                    public.processos_cliente, public.processos_produto WHERE 
                                    processos_compra."Produto_id" = processos_produto.id AND
                                    processos_cliente.id = processos_compra."Cliente_id" 
                                    ORDER BY processos_compra."Data" desc;''')

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

    balanco = Balanco.objects.get(compras_id = pk)

    form = CompraForm(request.POST or None, instance=compra)

    if form.is_valid():
        balanco.delete()
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


@login_required
def despesa(request):
    despesa = Despesas.objects.all()
    form = DespesasForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado com sucesso')
            return redirect('despesa')

    context = {

        'form': form,
        'despesa':despesa
    }

    return render(request, 'despesa.html', context)

@login_required
def despesa_delete(request,pk):
    despesa = get_object_or_404(Despesas,pk=pk)
    despesa.delete()
    return redirect('despesa')

@login_required
def despesa_edit(request, pk):

    despesa = get_object_or_404(Despesas, pk=pk)

    balanco = Balanco.objects.get(despesa_id=pk)
    form = DespesasForm(request.POST or None, instance=despesa)

    if form.is_valid():
        balanco.delete()
        form.save()
        return redirect('despesa')

    context = {
        'form': form,
        'despesa': despesa
    }

    return render(request, 'despesa_edit.html', context)

@login_required
def balanco(request):

    balanco = Balanco.objects.raw('''SELECT 1 as id,to_char(processos_balanco."datas", 'MM-YYYY') as periodo, 
                                    sum(compra) as rendimento, sum(despesa) as despesa, (sum(compra) - sum(despesa)) as total
                                      FROM public.processos_balanco GROUP BY to_char(processos_balanco."datas", 'MM-YYYY') ''')

    balancoCompleto = Balanco.objects.all().order_by('-datas')



    form = BalancoForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado com sucesso')
            return redirect('balanco')

    context = {

        'form': form,
        'balanco':balanco,
        'balancoCompleto':balancoCompleto,

    }

    return render(request, 'balanco.html', context)

@login_required
def balanco_delete(request,pk):
    balanco = get_object_or_404(Balanco,pk=pk)
    balanco.delete()
    return redirect('balanco')

@login_required
def balanco_edit(request, pk):

    balanco = get_object_or_404(Balanco, pk=pk)

    form = BalancoForm(request.POST or None, instance=balanco)

    if form.is_valid():
        form.save()
        return redirect('balanco')

    context = {
        'form': form,
        'balanco': balanco
    }

    return render(request, 'balanco_edit.html', context)

