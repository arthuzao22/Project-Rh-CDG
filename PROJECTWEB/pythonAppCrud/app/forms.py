from django import forms
from django.forms import ModelForm
from app.models import Funcionarios, Login, PlanSalario

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
            'status',
            'cargo'
        ]
        
        widgets = {
            'data_nascimento': forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy', 'class': 'date-input'}),
            'data_admissao': forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy', 'class': 'date-input'}),
            'ultimo_exame': forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy', 'class': 'date-input'}),
            'proximo_exame': forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy', 'class': 'date-input'}),
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

class PlanSalarioForm(ModelForm):
    class Meta:
        model = PlanSalario
        fields = [
            'funcionario', 
            'mesAno', 
            'qtde_dias_Mes',
            'dias_trabalhados',  
            'arred', 
            'ferias', 
            'decimo_terceiro_ferias',  
            'periculosidade',  
            'salario_familia', 
            'outras_entradas',  
            'ir_ferias', 
            'vales_e_faltas', 
            'vt', 
            'troco', 
            'geral', 
        ]
        
        widgets = {
            'mesAno': forms.TextInput(attrs={'placeholder': 'mm/yyyy', 'class': 'date-input'}),
        }
