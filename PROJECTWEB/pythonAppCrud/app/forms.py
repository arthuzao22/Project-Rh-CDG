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


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Usuário')
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        # Verificar se o usuário existe
        try:
            user = Login.objects.get(username=username)
        except Login.DoesNotExist:
            raise forms.ValidationError("Usuário não encontrado")

        # Verificar a senha
        if not user.check_password(password):
            raise forms.ValidationError("Senha incorreta")

        # Retornar o usuário se o login for bem-sucedido
        cleaned_data['user'] = user
        return cleaned_data

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
