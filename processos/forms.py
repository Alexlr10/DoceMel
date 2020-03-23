from django import forms
from .models import *
from django import forms


from django.utils.translation import gettext as _


class ClienteForm(forms.ModelForm):
    # data_intimacao = forms.DateField(widget=forms.TextInput(attrs={'format': 'dd/mm/yyyy', 'type': 'date'}))

    class Meta:
        model = Cliente
        fields = '__all__'
        # exclude = ['data_cadastro', 'data_atualizacao']

        widgets = {

        }


class ProdutoForm(forms.ModelForm):
    # data_intimacao = forms.DateField(widget=forms.TextInput(attrs={'format': 'dd/mm/yyyy', 'type': 'date'}))

    class Meta:
        model = Produto
        fields = '__all__'
        # exclude = ['data_cadastro', 'data_atualizacao']

        widgets = {

        }


class EstoqueForm(forms.ModelForm):
    # data_intimacao = forms.DateField(widget=forms.TextInput(attrs={'format': 'dd/mm/yyyy', 'type': 'date'}))

    class Meta:
        model = Estoque
        fields = '__all__'
        # exclude = ['data_cadastro', 'data_atualizacao']

        widgets = {

        }


class CompraForm(forms.ModelForm):
    # data_intimacao = forms.DateField(widget=forms.TextInput(attrs={'format': 'dd/mm/yyyy', 'type': 'date'}))

    class Meta:
        model = Compra
        fields = '__all__'
        # exclude = ['data_cadastro', 'data_atualizacao']

        widgets = {

        }


class FuncionarioForm(forms.ModelForm):
    # data_intimacao = forms.DateField(widget=forms.TextInput(attrs={'format': 'dd/mm/yyyy', 'type': 'date'}))

    class Meta:
        model = Funcionario
        fields = '__all__'
        # exclude = ['data_cadastro', 'data_atualizacao']

        widgets = {

        }


class FornecedorForm(forms.ModelForm):
    # data_intimacao = forms.DateField(widget=forms.TextInput(attrs={'format': 'dd/mm/yyyy', 'type': 'date'}))

    class Meta:
        model = Fornecedor
        fields = '__all__'
        exclude = ['sobrenome']

        widgets = {

        }

class TarefasForm(forms.ModelForm):
    # data_intimacao = forms.DateField(widget=forms.TextInput(attrs={'format': 'dd/mm/yyyy', 'type': 'date'}))

    class Meta:
        model = Tarefas
        fields = '__all__'


        widgets = {

        }
