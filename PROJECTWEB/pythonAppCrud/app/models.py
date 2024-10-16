from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

class Funcionarios(models.Model):
    cpf_validator = RegexValidator(
        r'^\d{11}$',
        'O CPF deve ter 11 dígitos numéricos.'
    )

    nome = models.CharField(max_length=150, verbose_name='Nome')
    registro = models.CharField(max_length=50, verbose_name='Registro')
    funcao = models.CharField(max_length=100, verbose_name='Função')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    data_admissao = models.DateField(verbose_name='Data de Admissão')
    cpf = models.CharField(max_length=11, validators=[cpf_validator], unique=True, verbose_name='CPF')
    conta_inter = models.CharField(max_length=20, verbose_name='Conta Inter')
    ultimo_exame = models.DateField(null=True, blank=True, verbose_name='Último Exame')
    proximo_exame = models.DateField(null=True, blank=True, verbose_name='Próximo Exame')
    email = models.EmailField(max_length=100, validators=[EmailValidator()], unique=True, verbose_name='Email')
    salario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Salário')
    status = models.CharField(max_length=50, verbose_name='status')


    def __str__(self):
        return self.nome


class Login(models.Model):
    username = models.CharField(max_length=150, unique=True, verbose_name='Nome de Usuário')
    password = models.CharField(max_length=128, verbose_name='Senha')
    funcionario = models.ForeignKey(Funcionarios, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Funcionário')

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class PlanSalario(models.Model):
    funcionario = models.ForeignKey(Funcionarios, on_delete=models.CASCADE, verbose_name='Funcionário')
    mesAno = models.DateField(verbose_name='Mês e Ano')
    dias_trabalhados = models.IntegerField(verbose_name='Dias Trabalhados')
    arred = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Arredondamento')
    ferias = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Férias')
    decimo_terceiro_ferias = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='13º de Férias')
    periculosidade = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Periculosidade')
    salario_familia = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Salário Família')
    outras_entradas = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Outras Entradas')
    ir_ferias = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='IR Férias')
    vales_e_faltas = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Vales e Faltas')
    vt = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Vale Transporte')
    troco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Troco')
    geral = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Geral')

    def __str__(self):
        return f'Salário de {self.funcionario.nome} - {self.mesAno.strftime("%Y-%m")}'
