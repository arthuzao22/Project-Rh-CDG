from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password
from app.forms import FuncionariosForm, LoginForm, PlanSalarioForm
from app.models import Login, Funcionarios, PlanSalario
import pandas as pd
import calendar
from decimal import Decimal

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

def index_salario(request):
    # Obtém os parâmetros de mês, ano e status (ativo/inativo) da requisição (GET)
    mesAno = request.GET.get('mesAno')
    status = request.GET.get('status') 
    nome = request.GET.get('nome') 


    # Inicia a query com todos os registros de salários
    salarios = PlanSalario.objects.all().select_related('funcionario')

    # Aplica o filtro de mês e ano, se fornecido
    if mesAno:
        salarios = salarios.filter(mesAno=mesAno)
    
    # Aplica o filtro de status de funcionários, se fornecido
    if status:
        salarios = salarios.filter(funcionario__status=status)

    if nome:
        salarios = salarios.filter(funcionario__nome__icontains=nome)
    # Prepara os dados para renderização
    data = {'db': salarios}

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


############################################################## RELATORIO SALARIO MENSAL ####################################################

# Manipulação de dados dos funcionários com Pandas
# Manipulação de dados dos funcionários com Pandas
def manipulate_funcionarios(request):
    # Obtém dados dos funcionários
    funcionarios = Funcionarios.objects.all()
    data = {
        'nome': [f.nome for f in funcionarios],
        'registro': [f.registro for f in funcionarios],
        'funcao': [f.funcao for f in funcionarios],
        'data_admissao': [f.data_admissao for f in funcionarios],
        'salario': [f.salario for f in funcionarios],
    }
    
    # Obtém dados de salários
    salarios = PlanSalario.objects.all()  # Filtra pelo mês e ano
    data_salario = {
        'mesAno': [s.mesAno for s in salarios],
        'dias_trabalhados': [s.dias_trabalhados for s in salarios],
        'qtde_dias_Mes': [s.qtde_dias_Mes for s in salarios],
        'arred': [s.arred for s in salarios],
        'ferias': [s.ferias for s in salarios],
        'decimo_terceiro_ferias': [s.decimo_terceiro_ferias for s in salarios],
        'periculosidade': [s.periculosidade for s in salarios],
        'salario_familia': [s.salario_familia for s in salarios],
        'outras_entradas': [s.outras_entradas for s in salarios],
    }
    
    df = pd.DataFrame(data_salario)
    df2 = pd.DataFrame(data)

    # Converte colunas para Decimal
    df2['salario'] = df2['salario'].apply(Decimal)
    df['qtde_dias_Mes'] = df['qtde_dias_Mes'].apply(Decimal)
    df['dias_trabalhados'] = df['dias_trabalhados'].apply(Decimal)
    df['arred'] = df['arred'].apply(Decimal)
    df['ferias'] = df['ferias'].apply(Decimal)
    df['decimo_terceiro_ferias'] = df['decimo_terceiro_ferias'].apply(Decimal)
    df['periculosidade'] = df['periculosidade'].apply(Decimal)
    df['salario_familia'] = df['salario_familia'].apply(Decimal)
    df['outras_entradas'] = df['outras_entradas'].apply(Decimal)

    # Função para realizar o cálculo somente se os valores não forem zero
    def calcular_salario_mes(salario, qtde_dias_Mes, dias_trabalhados):
        if salario == 0 or qtde_dias_Mes == 0 or dias_trabalhados == 0:
            return None 
        return (salario / qtde_dias_Mes) * dias_trabalhados

    # Aplica a função com a condição
    df['salario_Mes'] = df.apply(lambda row: calcular_salario_mes(
        df2['salario'][row.name], row['qtde_dias_Mes'], row['dias_trabalhados']), axis=1)
    
    # Função para calcular o valor bruto da folha final
    def calcular_bruto_folha_final(salario_mes, arred, ferias, decimo_terceiro_ferias, periculosidade, salario_familia, outras_entradas):
        # Substitui None por Decimal(0)
        salario_mes = salario_mes if salario_mes is not None else Decimal(0)
        arred = arred if arred is not None else Decimal(0)
        ferias = ferias if ferias is not None else Decimal(0)
        decimo_terceiro_ferias = decimo_terceiro_ferias if decimo_terceiro_ferias is not None else Decimal(0)
        periculosidade = periculosidade if periculosidade is not None else Decimal(0)
        salario_familia = salario_familia if salario_familia is not None else Decimal(0)
        outras_entradas = outras_entradas if outras_entradas is not None else Decimal(0)

        return (salario_mes + arred + ferias + decimo_terceiro_ferias +
                periculosidade + salario_familia + outras_entradas)

    # Arredondando os valores de salario_Mes para 2 casas decimais, ignorando None
    df['salario_Mes'] = df['salario_Mes'].apply(lambda x: round(x, 2) if x is not None else x)

    # Calcula o bruto_Mes
    df['bruto_Mes'] = df.apply(lambda row: calcular_bruto_folha_final(
        row['salario_Mes'], row['arred'], row['ferias'], row['decimo_terceiro_ferias'],
        row['periculosidade'], row['salario_familia'], row['outras_entradas']), axis=1)

    # Arredondando bruto_Mes para 2 casas decimais, ignorando None
    df['bruto_Mes'] = df['bruto_Mes'].apply(lambda x: round(x, 2) if x is not None else x)

    print(df)

    return render(request, 'Funcionarios/manipulated_data.html', {'df': df.to_html()})
