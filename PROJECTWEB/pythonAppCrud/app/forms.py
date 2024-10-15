from django import forms
from django.forms import ModelForm
from app.models import Funcionarios, Login

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
            'salario'
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
        
        # Adicionando widgets para personalizar os campos
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nome de Usuário'}),
        }
