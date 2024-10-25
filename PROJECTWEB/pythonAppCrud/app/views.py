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
import math
from django.shortcuts import render
import numpy as np
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# Página inicial
def home(request):
    #if request.user.is_authenticated:
        data = {'db': Funcionarios.objects.all()}
        return render(request, 'index.html', data)
    #else:
        #return render(request, 'login/login.html')

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
    try:
        funcionario = Funcionarios.objects.get(pk=pk)
        dados = {
            'nome': funcionario.nome,
            'registro': funcionario.registro,
            'funcao': funcionario.funcao,
            'data_nascimento': funcionario.data_nascimento,
            'data_admissao': funcionario.data_admissao,
            'cpf': funcionario.cpf,
            'conta_inter': funcionario.conta_inter,
            'ultimo_exame': funcionario.ultimo_exame,
            'proximo_exame': funcionario.proximo_exame,
            'email': funcionario.email,
            'salario': funcionario.salario,
            'status': funcionario.status,
        }
        return JsonResponse(dados)
    except:
        return JsonResponse({'error': 'objeto nao encontrado'}, status=404)

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
    #if request.user.is_authenticated:
    status = request.GET.get('status')
    if status:
        data = {
            'db': Funcionarios.objects.filter(status=status)
        }
    else:
        data = {'db': Funcionarios.objects.all()}
    return render(request, 'Funcionarios/indexFuncionarios.html', data)
    #else:
       # return render(request, 'login/login.html')

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
    return render(request, 'Salarios/formEditSalario.html', {'form': form, 'db': funcionario_salario})

# Atualização de salário de funcionário
def update_salario(request, pk):
    funcionario_salario = get_object_or_404(PlanSalario, pk=pk)
    form = PlanSalarioForm(request.POST, instance=funcionario_salario)
    if form.is_valid():
        form.save()
        messages.success(request, "Salário do Funcionário atualizado com sucesso!")
        return redirect('index_salario')
    return render(request, 'Salarios/formEditSalario.html', {'form': form, 'db': funcionario_salario})

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

# Exibir formulário de salário
def formEditSalario(request):
    data = {'form': PlanSalarioForm()}
    return render(request, 'Salarios/formEditSalario.html', data)


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

def calcular_VT(salario_Mes, vt):
    # Substitui None por Decimal(0)
    if vt not in [2]:
        salario_Mes = salario_Mes if salario_Mes is not None else Decimal(0)

        # Calcula o VT como 6% do salário
        vt = salario_Mes * Decimal(0.06)

        # Arredonda para duas casas decimais
        vt_arredondado = vt.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    else:
        vt_arredondado = Decimal(0)
    return vt_arredondado

def calcular_plano_de_Saude(coparticipacao, mes):
    coparticipacao = coparticipacao if coparticipacao is not None else Decimal(0)
    mes = mes if mes is not None else Decimal(0)
    
    return(coparticipacao + mes)

def calcular_adiantamento(salario_Mes, cargo):
    salario_Mes = salario_Mes if salario_Mes is not None else Decimal(0)
    if cargo not in ["Estagiario", "PJ"]:
        adiantamento = math.ceil(Decimal(salario_Mes) * Decimal(0.40)) - Decimal(1)
    else:
        adiantamento = Decimal(0)
    
    return adiantamento

def calcular_total_descontos(INSS, FGTS, ferias, vales_e_faltas, VT, PlanoDeSaude, adiantamento, troco):
    try:
        INSS = INSS if INSS is not None else Decimal(0)
        FGTS = FGTS if FGTS is not None else Decimal(0)
        ferias = ferias if ferias is not None else Decimal(0)
        vales_e_faltas = vales_e_faltas if vales_e_faltas is not None else Decimal(0)
        VT = VT if VT is not None else Decimal(0)
        PlanoDeSaude = PlanoDeSaude if PlanoDeSaude is not None else Decimal(0)
        adiantamento = adiantamento if adiantamento is not None else Decimal(0)
        troco = troco if troco is not None else Decimal(0)

        total_descontos = (INSS + ferias + vales_e_faltas + VT + PlanoDeSaude + adiantamento + troco) - FGTS
        
        #print(f"INSS: {INSS}, FGTS: {FGTS}, Ferias: {ferias}, Vales: {vales_e_faltas}, VT: {VT}, Plano: {PlanoDeSaude}, Adiantamento: {adiantamento}, Troco: {troco}")
        #print(f"Total Descontos: {total_descontos}")
        
        return total_descontos
    except Exception as e:
        print(f"Erro ao calcular total de descontos: {e}")
        return None
    
def calcular_liquido_pagar(bruto_Mes, TotalDescontos):
    bruto_Mes = bruto_Mes if bruto_Mes is not None else Decimal(0)
    TotalDescontos = TotalDescontos if TotalDescontos is not None else Decimal(0)
    
    liquido_pagar = bruto_Mes - TotalDescontos
    
    return liquido_pagar


def manipulate_funcionarios(request):
    # Obtém dados dos funcionários
    funcionarios = Funcionarios.objects.all()
    data = {
        'id': [f.id for f in funcionarios],
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
        'id': [s.id for s in salarios],
        'mesAno': [s.mesAno for s in salarios],
        'dias_trabalhados': [s.dias_trabalhados for s in salarios],
        'qtde_dias_Mes': [s.qtde_dias_Mes for s in salarios],
        'arred': [s.arred for s in salarios],
        'ferias': [s.ferias for s in salarios],
        'decimo_terceiro_ferias': [s.decimo_terceiro_ferias for s in salarios],
        'periculosidade': [s.periculosidade for s in salarios],
        'salario_familia': [s.salario_familia for s in salarios],
        'outras_entradas': [s.outras_entradas for s in salarios],
        'mes': [s.mes for s in salarios],
        'coparticipacao': [s.coparticipacao for s in salarios],
        'vt': [s.vt for s in salarios],
        'vales_e_faltas': [s.vales_e_faltas for s in salarios],
        'troco': [s.troco for s in salarios],
        'funcionario_id': [s.funcionario_id for s in salarios],
        'ir_ferias': [s.ir_ferias for s in salarios],
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
    df['mes'] = df['mes'].apply(Decimal)
    df['coparticipacao'] = df['coparticipacao'].apply(Decimal)
    df['vales_e_faltas'] = df['vales_e_faltas'].apply(Decimal)
    df['troco'] = df['troco'].apply(Decimal)
    df['ir_ferias'] = df['ir_ferias'].apply(Decimal)

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
        row['salario_Mes'], row['vt']), axis=1)
    
    df['PlanoDeSaude'] = df.apply(lambda row: calcular_plano_de_Saude(
        row['coparticipacao'], row['mes']
    ), axis=1)
    
    df['adiantamento'] = df.apply(lambda row: calcular_adiantamento(
        row['salario_Mes'], df2['cargo'][row.name]
    ), axis=1)
    
    df['TotalDescontos'] = df.apply(lambda row: calcular_total_descontos(
        row['INSS'], row['FGTS'], row['ferias'], row['vales_e_faltas'], row['VT'], row['PlanoDeSaude'], row['adiantamento'], row['troco']
    ), axis=1)
    
    df['liquidoPagar'] = df.apply(lambda row: calcular_liquido_pagar(
        row['bruto_Mes'], row['TotalDescontos']
    ), axis=1)
        
    # Arredondando bruto_Mes, FGTS e INSS para 2 casas decimais, ignorando None
    df['bruto_Mes'] = df['bruto_Mes'].apply(lambda x: round(x, 2) if x is not None else x)
    df['FGTS'] = df['FGTS'].apply(lambda x: round(x, 2) if x is not None else x)
    df['INSS'] = df['INSS'].apply(lambda x: round(x, 2) if x is not None else x)
    df['TotalDescontos'] = df['TotalDescontos'].apply(lambda x: round(x, 2) if x is not None else x)
    df['liquidoPagar'] = df['liquidoPagar'].apply(lambda x: round(x, 2) if x is not None else x)

    # Serve para unir df e o df2
    df_left_join = pd.merge(df2, df, left_on='id', right_on='funcionario_id', how='inner')
    
    ############################ FILTRAR ##############################
    mesAno = request.GET.get('mesAno')
    nome = request.GET.get('nome')

    if mesAno:
        df_left_join = df_left_join[df_left_join['mesAno'] == mesAno]

    if nome:
        df_left_join = df_left_join[df_left_join['nome'] == nome]
    ############################ ------- ##############################
    
    funcionarios_list = df_left_join.to_dict(orient='records')
    
    # Retorna o template com a lista de dicionários
    return render(request, 'Salarios/manipulated_data.html', {'funcionarios': funcionarios_list})



############################################################## LOGIN ###########################################################

# Login de usuário
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Verifica se existe um usuário com o nome de usuário fornecido
        try:
            user = authenticate(username=username, password=password)
            if user:
                # Redirecionar o usuário para a página inicial após o login
                return redirect('home')
            else:
                messages.error(request, 'Senha incorreta. Tente novamente.')
        except Login.DoesNotExist:
            messages.error(request, 'Nome de usuário não encontrado.')

    return render(request, 'login/login.html')

# Criação de login
def createlogin(request):
    form = LoginForm(request.POST)
    if not form.is_valid():
       return render(request, 'login/loginForm.html', {'form': form})

    c = form.save(commit=False)
    c.password = make_password(c.password)
    c.save()
    return HttpResponseRedirect('/')