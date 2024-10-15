from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.contrib.auth.hashers import make_password

# Create your models here.
class Funcionarios(models.Model):
    # Validador de CPF (apenas números)
    cpf_validator = RegexValidator(
        r'^\d{11}$',  # Permite apenas 11 dígitos
        'O CPF deve ter 11 dígitos numéricos.'
    )

    nome = models.CharField(max_length=150)
    registro = models.CharField(max_length=50)
    funcao = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    data_admissao = models.DateField()
    cpf = models.CharField(max_length=11, validators=[cpf_validator])
    conta_inter = models.CharField(max_length=20)
    ultimo_exame = models.DateField(null=True, blank=True)
    proximo_exame = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=100, validators=[EmailValidator()])
    salario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome


class Login(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Considerando o uso de hashing
    funcionario = models.ForeignKey(Funcionarios, on_delete=models.SET_NULL, null=True)  # Permitir valores nulos

    def save(self, *args, **kwargs):
        # Hash a senha antes de salvar
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
