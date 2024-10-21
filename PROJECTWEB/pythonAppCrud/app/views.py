from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password
from app.forms import FuncionariosForm, LoginForm, PlanSalarioForm
from app.models import Login, Funcionarios, PlanSalario
import pandas as pd
import calendar
from decimal import Decimal, ROUND_HALF_UP
import numpy as np
#from django.contrib.auth.decorators import login_required



# Página inicial
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

def calcular_salario_mes(salario, qtde_dias_Mes, dias_trabalhados):
    if salario == 0 or qtde_dias_Mes == 0 or dias_trabalhados == 0:
        return None 
    return (salario / qtde_dias_Mes) * dias_trabalhados

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

def calcular_INSS(salario_Mes, cargo, ferias=Decimal(0), decimo_terceiro_ferias=Decimal(0), periculosidade=Decimal(0), outras_entradas=Decimal(0)):
    # Substitui None por Decimal(0)
    salario_Mes = salario_Mes if salario_Mes is not None else Decimal(0)
    ferias = ferias if ferias is not None else Decimal(0)
    decimo_terceiro_ferias = decimo_terceiro_ferias if decimo_terceiro_ferias is not None else Decimal(0)
    periculosidade = periculosidade if periculosidade is not None else Decimal(0)
    outras_entradas = outras_entradas if outras_entradas is not None else Decimal(0)

    if cargo not in ["Estagiario", "PJ"]:
        total = salario_Mes + ferias + decimo_terceiro_ferias + periculosidade + outras_entradas

        if total < Decimal(1):
            return Decimal(0)
        else:
            if total < Decimal(1412):
                return np.ceil(total * Decimal(0.075))
            elif total < Decimal(2666.68):
                return np.ceil(total * Decimal(0.09) - Decimal(21.18))
            else:
                return np.ceil(total * Decimal(0.12) - Decimal(101.18))
    else:
        return Decimal(0)

def calcular_FGTS(salario_Mes, cargo, ferias=Decimal(0), decimo_terceiro_ferias=Decimal(0)):
    # Substitui None por Decimal(0)
    salario_Mes = salario_Mes if salario_Mes is not None else Decimal(0)
    ferias = ferias if ferias is not None else Decimal(0)
    decimo_terceiro_ferias = decimo_terceiro_ferias if decimo_terceiro_ferias is not None else Decimal(0)

    if cargo not in ["Estagiario", "PJ"]:
        total = (salario_Mes + ferias + decimo_terceiro_ferias)
    else:
        total = Decimal(0)
        
    return total * Decimal(0.08)

def calcular_VT(salario_Mes):
    # Substitui None por Decimal(0)
    salario_Mes = salario_Mes if salario_Mes is not None else Decimal(0)

    # Calcula o VT como 6% do salário
    vt = salario_Mes * Decimal(0.06)

    # Arredonda para duas casas decimais
    vt_arredondado = vt.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

    return vt_arredondado

def manipulate_funcionarios(request):
    # Obtém dados dos funcionários
    funcionarios = Funcionarios.objects.all()
    data = {
        'nome': [f.nome for f in funcionarios],
        'registro': [f.registro for f in funcionarios],
        'funcao': [f.funcao for f in funcionarios],
        'data_admissao': [f.data_admissao for f in funcionarios],
        'salario': [f.salario for f in funcionarios],
        'cargo': [f.cargo for f in funcionarios],  # Corrigido aqui
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

    # Aplica a função com a condição
    df['salario_Mes'] = df.apply(lambda row: calcular_salario_mes(
        df2['salario'][row.name], row['qtde_dias_Mes'], row['dias_trabalhados']), axis=1)
    
    # Arredondando os valores de salario_Mes para 2 casas decimais, ignorando None
    df['salario_Mes'] = df['salario_Mes'].apply(lambda x: round(x, 2) if x is not None else x)

    # Calcula o bruto_Mes
    df['bruto_Mes'] = df.apply(lambda row: calcular_bruto_folha_final(
        row['salario_Mes'], row['arred'], row['ferias'], row['decimo_terceiro_ferias'],
        row['periculosidade'], row['salario_familia'], row['outras_entradas']), axis=1)
    
    # Adiciona a coluna INSS aplicando a função calcular_INSS
    df['INSS'] = df.apply(lambda row: calcular_INSS(
        row['salario_Mes'], df2['cargo'][row.name], row['ferias'], 
        row['decimo_terceiro_ferias'], row['periculosidade'], row['outras_entradas']), axis=1)
    
    df['FGTS'] = df.apply(lambda row: calcular_FGTS(
        row['salario_Mes'], df2['cargo'][row.name], row['ferias'], row['decimo_terceiro_ferias']), axis=1)
    
    df['VT'] = df.apply(lambda row: calcular_VT(
        row['salario_Mes']), axis=1)
    
    # Arredondando bruto_Mes, FGTS e INSS para 2 casas decimais, ignorando None
    df['bruto_Mes'] = df['bruto_Mes'].apply(lambda x: round(x, 2) if x is not None else x)
    df['FGTS'] = df['FGTS'].apply(lambda x: round(x, 2) if x is not None else x)
    df['INSS'] = df['INSS'].apply(lambda x: round(x, 2) if x is not None else x)

    print(df)
    return render(request, 'Funcionarios/manipulated_data.html', {'df': df.to_html()})

############################################################## LOGIN ###########################################################

# Login de usuário
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Verifica se existe um usuário com o nome de usuário fornecido
        try:
            user = Login.objects.get(username=username)
            
            # Comparação direta de senha, sem criptografia
            if user.password == password:
                # Redirecionar o usuário para a página inicial após o login
                return redirect('home')
            else:
                messages.error(request, 'Senha incorreta. Tente novamente.')
        except Login.DoesNotExist:
            messages.error(request, 'Nome de usuário não encontrado.')

    return render(request, 'login/login.html')

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