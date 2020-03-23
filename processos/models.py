from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete



class Cliente(models.Model):

    nome = models.CharField(_('Nome'), max_length=30, null=True, blank=True)
    sobrenome = models.CharField(_('Sobrenome'), max_length=30, null=True, blank=True)
    cidade = models.CharField(_('Cidade'), max_length=80, null=True, blank=True)
    bairro = models.CharField(_('Bairro'), max_length=20, null=True, blank=True)
    rua = models.CharField(_('Rua'), max_length=80, null=True, blank=True)
    numero = models.CharField(_('Numero'), max_length=20, null=True, blank=True)
    cep = models.CharField(_('CEP'), max_length=15, null=True, blank=True)
    cpf = models.CharField(_('CPF'), max_length=15, null=True, blank=True)
    contato = models.CharField(_('Contato'), max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = _("Cliente")
        verbose_name_plural = _("processos")

    def __str__(self):
        return self.nome

class Fornecedor(models.Model):

    nome = models.CharField(_('Nome:'), max_length=30, null=True, blank=True)
    cidade = models.CharField(_('Cidade'), max_length=80, null=True, blank=True)
    bairro = models.CharField(_('Bairro'), max_length=20, null=True, blank=True)
    rua = models.CharField(_('Rua'), max_length=80, null=True, blank=True)
    numero = models.CharField(_('Numero'), max_length=20, null=True, blank=True)
    cep = models.CharField(_('CEP'), max_length=15, null=True, blank=True)
    cnpj = models.CharField(_('CNPJ'), max_length=15, null=True, blank=True)
    contato = models.CharField(_('Contato'), max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = _("Fornecedor")
        verbose_name_plural = _("Fornecedor")

    def __str__(self):
        return self.nome

class Funcionario(models.Model):

    nome = models.CharField(_('Nome:'), max_length=30, null=True, blank=True)
    sobrenome = models.CharField(_('Sobrenome'), max_length=30, null=True, blank=True)
    cidade = models.CharField(_('Cidade'), max_length=80, null=True, blank=True)
    bairro = models.CharField(_('Bairro'), max_length=20, null=True, blank=True)
    rua = models.CharField(_('Rua'), max_length=80, null=True, blank=True)
    numero = models.CharField(_('Numero'), max_length=20, null=True, blank=True)
    cep = models.CharField(_('CEP'), max_length=15, null=True, blank=True)
    ssn = models.CharField(_('Ssn'),max_length=30,null=True,blank=True)
    salario = models.DecimalField('Salario', max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = _("Funcionario")
        verbose_name_plural = _("Funcionario")

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nomeproduto = models.CharField(_('Produto'), max_length=30, null=True, blank=True)
    descricao = models.TextField('Descrição', null=True, blank=True)
    quantidade = models.IntegerField('Quantidade', blank=True, null=True)
    valor = models.DecimalField('Valor', max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = _("Produto")
        verbose_name_plural = _("Produtos")

    def __str__(self):
        return self.nomeproduto

class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='Produto')
    qtd = models.IntegerField('Quantidade', blank=True, null=True)
    limite = 50
    data= models.DateTimeField('Data', blank=True, null=True)

    class Meta:
        verbose_name = _("Estoque")
        verbose_name_plural = _("Estoques")

    def __str__(self):
        return self.produto.nomeproduto


class Compra(models.Model):
    Cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='Clientes')
    Produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='Produtos')
    quantidade = models.IntegerField('Unidades', blank=True, null=True)
    Funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='Funcionarios')
    valor = models.DecimalField('Preco', max_digits=6, decimal_places=2)
    Data = models.DateTimeField('Data', blank=True, null=True)

    class Meta:
        verbose_name = _("Compra")
        verbose_name_plural = _("Compras")


    def __str__(self):
        return self.Cliente.nome
    def __str__(self):
        return self.Produto.nomeproduto
    def __str__(self):
        return self.Funcionario.nome


class Tarefas(models.Model):

    nome = models.CharField(_('nome'), max_length=30, null=True, blank=True)
    descricao = models.TextField('descrição', null=True, blank=True)

    class Meta:
        verbose_name = _("Tarefa")
        verbose_name_plural = _("tarefas")



