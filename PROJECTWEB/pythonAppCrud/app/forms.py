from django import forms
from django.forms import ModelForm
from app.models import Funcionarios, Login, PlanSalario  # Corrigido

class FuncionariosForm(ModelForm):
    class Meta:
        model = Funcionarios
        fields = [
            'nome', 
            'registro', 
            'funcao', 
            'data_nascimento', 
            'data_admissao', 
            'cpf', 
            'conta_inter', 
            'ultimo_exame', 
            'proximo_exame', 
            'email', 
            'salario',
            'status'
        ]
        
        # Adicionando widgets para personalizar os campos
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'data_admissao': forms.DateInput(attrs={'type': 'date'}),
            'ultimo_exame': forms.DateInput(attrs={'type': 'date'}),
            'proximo_exame': forms.DateInput(attrs={'type': 'date'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@exemplo.com'}),
        }


class LoginForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))

    class Meta:
        model = Login
        fields = ['username', 'password']
        
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nome de Usuário'}),
        }

class PlanSalarioForm(ModelForm):  # Corrigido
    class Meta:
        model = PlanSalario
        fields = [
            'funcionario', 
            'mesAno', 
            'dias_trabalhados',  # Corrigido
            'arred', 
            'ferias', 
            'decimo_terceiro_ferias',  # Corrigido
            'periculosidade',  # Corrigido
            'salario_familia', 
            'outras_entradas',  # Corrigido
            'ir_ferias', 
            'vales_e_faltas', 
            'vt', 
            'troco', 
            'geral', 
        ]
        
        widgets = {
            'mesAno': forms.DateInput(attrs={'type': 'date'}),  # Mudando para campo de texto
            'dias_trabalhados': forms.NumberInput(attrs={'min': 0, 'step': 'any'}),  # Corrigido
            'arred': forms.NumberInput(attrs={'min': 0, 'step': 'any'}),
            'ferias': forms.NumberInput(attrs={'min': 0, 'step': 'any'}),
            'decimo_terceiro_ferias': forms.NumberInput(attrs={'min': 0, 'step': 'any'}),
            'periculosidade': forms.NumberInput(attrs={'min': 0, 'step': 'any'}),
            'salario_familia': forms.NumberInput(attrs={'min': 0, 'step': 'any'}),
            'outras_entradas': forms.NumberInput(attrs={'min': 0, 'step': 'any'}),
            'ir_ferias': forms.NumberInput(attrs={'min': 0, 'step': 'any'}),
            'vales_e_faltas': forms.NumberInput(attrs={'min': 0, 'step': 'any'}),
            'vt': forms.NumberInput(attrs={'min': 0, 'step': 'any'}),
            'troco': forms.NumberInput(attrs={'min': 0, 'step': 'any'}),
            'geral': forms.NumberInput(attrs={'min': 0, 'step': 'any'}),
        }
