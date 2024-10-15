from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password
from app.forms import FuncionariosForm, LoginForm
from app.models import Login, Funcionarios
import pandas as pd

# Create your views here.
def home(request):
    data = {'db': Funcionarios.objects.all()}
    return render(request, 'index.html', data)

def form(request):
    data = {'form': FuncionariosForm()}
    return render(request, 'Funcionarios/form.html', data)

# Create
def create(request):
    form = FuncionariosForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Funcionário criado com sucesso!")
        return redirect('indexFuncionarios')
    data = {'form': form}
    return render(request, 'Funcionarios/form.html', data)

# View
def view(request, pk):
    funcionario = get_object_or_404(Funcionarios, pk=pk)
    return render(request, 'Funcionarios/view.html', {'db': funcionario})

# Edit
def edit(request, pk):
    funcionario = get_object_or_404(Funcionarios, pk=pk)
    form = FuncionariosForm(instance=funcionario)
    return render(request, 'Funcionarios/form.html', {'form': form, 'db': funcionario})

# Update
def update(request, pk):
    funcionario = get_object_or_404(Funcionarios, pk=pk)
    form = FuncionariosForm(request.POST, instance=funcionario)
    if form.is_valid():
        form.save()
        messages.success(request, "Funcionário atualizado com sucesso!")
        return redirect('indexFuncionarios')
    return render(request, 'Funcionarios/form.html', {'form': form, 'db': funcionario})

# Index Funcionarios
def indexFuncionarios(request):
    data = {'db': Funcionarios.objects.all()}
    return render(request, 'Funcionarios/indexFuncionarios.html', data)

# Delete
def delete(request, pk):
    funcionario = get_object_or_404(Funcionarios, pk=pk)
    funcionario.delete()
    messages.success(request, "Funcionário deletado com sucesso!")
    return redirect('indexFuncionarios')

# Login
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

# Login
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Autenticar o usuário
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "Login realizado com sucesso!")
                return redirect('home')  # Redirecione para a página inicial ou outra página
            else:
                messages.error(request, "Nome de usuário ou senha incorretos.")
    else:
        form = LoginForm()

    return render(request, 'login/login.html', {'form': form})


def createlogin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = Login(username=username, password=make_password(password))
            user.save()
            messages.success(request, "Usuário criado com sucesso!")
            return redirect('user_login')
    else:
        form = LoginForm()

    return render(request, 'login/loginform.html', {'form': form})


# Manipular dados dos funcionários com Pandas
def manipulate_funcionarios(request):
    # Obtenha todos os funcionários do banco de dados
    funcionarios = Funcionarios.objects.all()
    
    # Crie um DataFrame a partir dos dados
    data = {
        'nome': [f.nome for f in funcionarios],
        'registro': [f.registro for f in funcionarios],
        'funcao': [f.funcao for f in funcionarios],
        #'data_nascimento': [f.data_nascimento for f in funcionarios],
        'data_admissao': [f.data_admissao for f in funcionarios],
        #'cpf': [f.cpf for f in funcionarios],
        #'conta_inter': [f.conta_inter for f in funcionarios],
        #'ultimo_exame': [f.ultimo_exame for f in funcionarios],
        #'proximo_exame': [f.proximo_exame for f in funcionarios],
        #'email': [f.email for f in funcionarios],
        'salario': [f.salario for f in funcionarios],
    }
    df = pd.DataFrame(data)
    
    # Adicione uma nova coluna para o salário ajustado
    df['salario_com_acrescimo'] = df['salario'].apply(lambda x: x + 100 if x > 3000 else x)
    
    df['13º'] = (df['salario_com_acrescimo']/12) * 12
    
    df['Total_bruto_mes'] = df['salario_com_acrescimo'] + df['13º']

    # Para visualizar o DataFrame manipulado (opcional)
    print(df)

    # Retornar uma resposta ou renderizar um template
    return render(request, 'Funcionarios/manipulated_data.html', {'data': df.to_html()})
