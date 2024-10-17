from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password
from app.forms import FuncionariosForm, LoginForm, PlanSalarioForm
from app.models import Login, Funcionarios, PlanSalario
import pandas as pd

# Página inicial com todos os funcionários
def home(request):
    data = {'db': Funcionarios.objects.all()}
    return render(request, 'index.html', data)

# Exibe formulário de cadastro de funcionário
def form(request):
    data = {'form': FuncionariosForm()}
    return render(request, 'Funcionarios/form.html', data)

# Criação de funcionário
def create(request):
    form = FuncionariosForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Funcionário criado com sucesso!")
        return redirect('indexFuncionarios')
    return render(request, 'Funcionarios/form.html', {'form': form})

# Visualiza detalhes de um funcionário
def view(request, pk):
    funcionario = get_object_or_404(Funcionarios, pk=pk)
    return render(request, 'Funcionarios/view.html', {'db': funcionario})

# Edição de funcionário
def edit(request, pk):
    funcionario = get_object_or_404(Funcionarios, pk=pk)
    form = FuncionariosForm(instance=funcionario)
    return render(request, 'Funcionarios/form.html', {'form': form, 'db': funcionario})

# Atualização de funcionário
def update(request, pk):
    funcionario = get_object_or_404(Funcionarios, pk=pk)
    form = FuncionariosForm(request.POST, instance=funcionario)
    if form.is_valid():
        form.save()
        messages.success(request, "Funcionário atualizado com sucesso!")
        return redirect('indexFuncionarios')
    return render(request, 'Funcionarios/form.html', {'form': form, 'db': funcionario})

# Listagem de funcionários
def indexFuncionarios(request):
    # Obtém os parâmetros de mês e ano da requisição (GET)
    status = request.GET.get('status')

    if status:
        data = {
            'db': Funcionarios.objects.filter(status=status)
        }
    else:
        data = {'db': Funcionarios.objects.all()}
        
    return render(request, 'Funcionarios/indexFuncionarios.html', data)

# Deletar funcionário
def delete(request, pk):
    funcionario = get_object_or_404(Funcionarios, pk=pk)
    funcionario.delete()
    messages.success(request, "Funcionário deletado com sucesso!")
    return redirect('indexFuncionarios')

# Login de usuário
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "Login realizado com sucesso!")
                return redirect('home')
            else:
                messages.error(request, "Nome de usuário ou senha incorretos.")
    else:
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form})

# Criação de login
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

# Manipulação de dados dos funcionários com Pandas
def manipulate_funcionarios(request):
    funcionarios = Funcionarios.objects.all()
    data = {
        'nome': [f.nome for f in funcionarios],
        'registro': [f.registro for f in funcionarios],
        'funcao': [f.funcao for f in funcionarios],
        'data_admissao': [f.data_admissao for f in funcionarios],
        'salario': [f.salario for f in funcionarios],
    }
    df = pd.DataFrame(data)
    df['salario_com_acrescimo'] = df['salario'].apply(lambda x: x + 100 if x > 3000 else x)
    df['13º'] = (df['salario_com_acrescimo'] / 12) * 12
    df['Total_bruto_mes'] = df['salario_com_acrescimo'] + df['13º']
    
    return render(request, 'Funcionarios/manipulated_data.html', {'data': df.to_html()})

############################################################## PASTA 'SALARIOS' ####################################################

# Criação de salário de funcionário
def create_salario_funcionario(request):
    form = PlanSalarioForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Salário do Funcionário criado com sucesso!")
        return redirect('index_salario')
    return render(request, 'Salarios/form_salario.html', {'form': form})

# Edição de salário de funcionário
def edit_salario(request, pk):
    funcionario_salario = get_object_or_404(PlanSalario, pk=pk)
    form = PlanSalarioForm(instance=funcionario_salario)
    return render(request, 'Salarios/form_salario.html', {'form': form, 'db': funcionario_salario})

# Atualização de salário de funcionário
def update_salario(request, pk):
    funcionario_salario = get_object_or_404(PlanSalario, pk=pk)
    form = PlanSalarioForm(request.POST, instance=funcionario_salario)
    if form.is_valid():
        form.save()
        messages.success(request, "Salário do Funcionário atualizado com sucesso!")
        return redirect('index_salario')
    return render(request, 'Salarios/form_salario.html', {'form': form, 'db': funcionario_salario})

# Listagem de salários dos funcionários
def index_salario(request):
    # Obtém os parâmetros de mês e ano da requisição (GET)
    mes = request.GET.get('mes')
    ano = request.GET.get('ano')

    # Se houver filtros aplicados, faça a filtragem
    if mes and ano:
        data = {
            'db': PlanSalario.objects.filter(mesAno__month=mes, mesAno__year=ano)
        }
    else:
        # Caso contrário, exiba todos os registros
        data = {'db': PlanSalario.objects.all()}

    return render(request, 'Salarios/index_salario.html', data)


# Deletar salário de funcionário
def delete_salario(request, pk):
    funcionario_salario = get_object_or_404(PlanSalario, pk=pk)
    funcionario_salario.delete()
    messages.success(request, "Salário do Funcionário deletado com sucesso!")
    return redirect('index_salario')

# Exibir formulário de salário
def form_salario(request):
    data = {'form': PlanSalarioForm()}
    return render(request, 'Salarios/form_salario.html', data)
