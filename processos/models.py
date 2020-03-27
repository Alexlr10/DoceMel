from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from django.db.models import Sum


FUNCAO_CHOICE = (
    ('PROP','Proprietario'),
    ('ADM', 'Administrador'),
    ('USU', 'Usuario'),
    ('MED', 'Médico'),
    ('FARM','Farmaceutico'),
    ('NUT', 'Nutricionista'),
    ('PSI', 'Psicólogo'),
)

FUNCAO_CHOICE_PROF = (
    ('ADM', 'Administrador'),
    ('MED', 'Médico'),
    ('FARM','Farmaceutico'),
    ('NUT', 'Nutricionista'),
    ('PSI', 'Psicólogo'),
    ('FIS', 'Fisioterapeuta'),
)

GENERO_CHOICE = (
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('N', 'Não Declarado'),
)

UF = (
    ('MG', 'Minas Gerais'),
    ('SP', 'São Paulo'),
    ('RJ', 'Rio de Janeiro'),
    ('ES', 'Espirito Santo'),
    ('BA', 'Bahia'),
)

STATUS = (
    (0, 'Iniciado'),
    (1, 'Em andamento'),
    (2, 'Pendente'),
    (3, 'Resolvido'),
)

MOD = (
    (0, 'ACC'),
    (1, 'SAC'),

)



class UsuarioManager(BaseUserManager):
    def create_user(self, Login, Nome, Situacao, CPF, Email, Funcao, password=None):
        user = self.model(
            Login=Login,
            Nome=Nome,
            Situacao=Situacao,
            CPF=CPF,
            Email=Email,
            Funcao=Funcao
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, Login, Nome, Situacao, CPF, Email, Funcao, password):
        user = self.create_user(
            Login,
            Nome,
            Situacao,
            CPF,
            Email,
            Funcao
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser, PermissionsMixin):
    """Model definition for Usuario."""

    Nome = models.CharField('Nome', max_length=80)
    Foto = models.ImageField('Foto', upload_to='profile', default=None)
    Login = models.CharField('Login', max_length=50, unique=True)
    password = models.CharField('Senha', max_length=128)

    Situacao = models.BooleanField('Ativo', default=True)
    CPF = models.CharField('CPF', max_length=20)
    RG = models.CharField('RG', max_length=20, blank=True, null=True)
    Rua = models.CharField('Rua', max_length=100, blank=True, null=True)
    N = models.CharField('Número', max_length=10, blank=True, null=True)
    CEP = models.CharField('CEP', max_length=50, blank=True, null=True)
    Email = models.EmailField('Email', max_length=254)
    Celular = models.CharField('Celular', max_length=50, blank=True, null=True)
    Data_de_Nascimento = models.DateField(
        'Data de Nascimento', blank=True, null=True)
    Data_de_Admissão = models.DateField(
        'Data de Admissão', blank=True, null=True)
    Data_de_Demissão = models.DateField(
        'Data de Demissão', blank=True, null=True)
    Complemento = models.CharField(
        'Complemento', max_length=50, blank=True, null=True)
    Salario = models.DecimalField(
        'Salário', max_digits=15, decimal_places=2, blank=True, null=True)
    INSS = models.DecimalField(
        'INSS', max_digits=15, decimal_places=2, blank=True, null=True)
    Comissao = models.BooleanField('Recebe comissão', default=True)
    Agencia = models.CharField('Agência', max_length=50, blank=True, null=True)
    Conta_Corrente = models.CharField(
        'Conta', max_length=50, blank=True, null=True)
    Data_cadastro = models.DateTimeField(
        'Data de Cadastro', blank=True, null=True)

    Proximas_ferias = models.CharField(
        'Próximas férias', max_length=50, blank=True, null=True)
    Periodo_de_afastamento = models.CharField(
        'Período de afastamento', max_length=50, blank=True, null=True)
    Funcao = models.CharField('Função', max_length=4, choices=FUNCAO_CHOICE)

    # campos necessários pra o DJango
    last_login = models.DateTimeField(
        'Último login', blank=True, null=True, db_column='last_login')
    is_active = models.BooleanField('Ativo', default=True)
    is_staff = models.BooleanField('Membro da Equipe', default=False)
    is_admin = models.BooleanField('Administrador', default=False)

    USERNAME_FIELD = 'Login'
    EMAIL_FIELD = 'Email'
    REQUIRED_FIELDS = ['Nome', 'Situacao', 'CPF', 'Email', 'Funcao']

    objects = UsuarioManager()

    '''@receiver(post_save, sender=Usuario)
def post_usuario(self, instance, *args, **kwargs):
    if not Usuario.objects.filter(instance.Nome).exist():
        u = instance.Usuario.save()'''

    @property
    def is_superuser(self):
        return self.is_admin

    def get_full_name(self):
        return self.Nome

    class Meta:
        """Meta definition for Usuario."""

        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        """Unicode representation of Usuario."""
        return self.Nome



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



class Produto(models.Model):
    nomeproduto = models.CharField(_('Produto'), max_length=30, null=True, blank=True)
    descricao = models.TextField('Descrição', null=True, blank=True)
    valor = models.DecimalField('Valor', max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = _("Produto")
        verbose_name_plural = _("Produtos")

    def __str__(self):
        return self.nomeproduto


class Lote(models.Model):
    numeroLote = models.IntegerField('Nº do lote', blank=True, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='produto')
    quantidade = models.IntegerField('Quantidade', blank=True, null=True)

    class Meta:
        verbose_name = _("Lote")
        verbose_name_plural = _("Lotes")



class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='Produto')
    quantidade = models.IntegerField('Quantidade', blank=True, null=True)
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='Lote')

    class Meta:
        verbose_name = _("Estoque")
        verbose_name_plural = _("Estoques")

    def __str__(self):
        return self.produto.nomeproduto



class Compra(models.Model):
    Cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='Clientes')
    Produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='Produtos')
    quantidade = models.IntegerField('Unidades', blank=True, null=True)
    Data = models.DateField('Data', blank=True, null=True)

    class Meta:
        verbose_name = _("Compra")
        verbose_name_plural = _("Compras")


    def __str__(self):
        return self.Cliente.nome
    def __str__(self):
        return self.Produto.nomeproduto










