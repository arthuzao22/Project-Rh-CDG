from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
import re

class Funcionarios(models.Model):
    cpf_validator = RegexValidator(
        r'^\d{11}$',
        'O CPF deve ter 11 dígitos numéricos.'
    )

    def validate_date_format(value):
        """Valida se o campo segue o formato de data 'YYYY-MM-DD'."""
        if not re.match(r'\d{4}-\d{2}-\d{2}', value):
            raise ValidationError('A data deve estar no formato YYYY-MM-DD.')

    nome = models.CharField(max_length=150, verbose_name='Nome')
    registro = models.CharField(max_length=50, verbose_name='Registro')
    funcao = models.CharField(max_length=100, verbose_name='Função')
    data_nascimento = models.CharField(
        max_length=100, 
        verbose_name='Data de Nascimento', 
        validators=[validate_date_format]
    )
    data_admissao = models.CharField(
        max_length=100, 
        verbose_name='Data de Admissão', 
        validators=[validate_date_format]
    )
    cpf = models.CharField(max_length=11, validators=[cpf_validator], unique=True, verbose_name='CPF')
    conta_inter = models.CharField(max_length=20, verbose_name='Conta Inter')
    ultimo_exame = models.CharField(
        max_length=100, 
        null=True, 
        blank=True, 
        verbose_name='Último Exame', 
        validators=[validate_date_format]
    )
    proximo_exame = models.CharField(
        max_length=100, 
        null=True, 
        blank=True, 
        verbose_name='Próximo Exame', 
        validators=[validate_date_format]
    )
    email = models.EmailField(max_length=100, validators=[EmailValidator()], unique=True, verbose_name='Email')
    salario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Salário')
    status = models.CharField(max_length=50, verbose_name='Status')
    cargo = models.CharField(max_length=50, verbose_name='Status')


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
    mesAno = models.CharField(max_length=15, verbose_name='Mês e Ano')  # Alterado para CharField, conforme solicitado
    dias_trabalhados = models.IntegerField(verbose_name='Dias Trabalhados')
    qtde_dias_Mes = models.IntegerField(verbose_name='Qtde dias do mes')
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
        return f'Salário de {self.funcionario.nome} - {self.mesAno}'

