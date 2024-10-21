from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Funcionarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150)),
                ('registro', models.CharField(max_length=50)),
                ('funcao', models.CharField(max_length=100)),
                ('data_nascimento', models.CharField(max_length=150)),
                ('data_admissao', models.CharField(max_length=150)),
                ('cpf', models.CharField(max_length=11)),
                ('conta_inter', models.CharField(max_length=20)),
                ('ultimo_exame', models.DateField(null=True, blank=True)),
                ('proximo_exame', models.DateField(null=True, blank=True)),
                ('email', models.EmailField(max_length=100)),
                ('salario', models.DecimalField(max_digits=10, decimal_places=2)),
                ('status', models.CharField(max_length=150)),
                ('cargo', models.CharField(max_length=150)),       
            ],
            options={
                'verbose_name': 'Funcionário',
                'verbose_name_plural': 'Funcionários',
            },
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('funcionario', models.ForeignKey(on_delete=models.SET_NULL, to='app.Funcionarios', null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Login',
                'verbose_name_plural': 'Logins',
            },
        ),
        migrations.CreateModel(
    name='PlanSalario',
    fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('nome', models.CharField(max_length=150)),
        ('mesAno', models.IntegerField()),  # Para o mês e ano de referência
        ('qtde_dias_Mes', models.IntegerField()), 
        ('dias_trabalhados', models.IntegerField()), 
        ('arred', models.DecimalField(max_digits=10, decimal_places=2)),
        ('ferias', models.DecimalField(max_digits=10, decimal_places=2)),
        ('decimo_terceiro_ferias', models.DecimalField(max_digits=10, decimal_places=2)),
        ('periculosidade', models.DecimalField(max_digits=10, decimal_places=2)),
        ('salario_familia', models.DecimalField(max_digits=10, decimal_places=2)),
        ('outras_entradas', models.DecimalField(max_digits=10, decimal_places=2)),
        ('ir_ferias', models.DecimalField(max_digits=10, decimal_places=2)),
        ('vales_e_faltas', models.DecimalField(max_digits=10, decimal_places=2)),
        ('vt', models.DecimalField(max_digits=10, decimal_places=2)),
        ('troco', models.DecimalField(max_digits=10, decimal_places=2)),
        ('geral', models.DecimalField(max_digits=10, decimal_places=2)),
        # Novos campos relacionados ao plano de saúde
        ('plano_saude', models.CharField(max_length=150)),  # Nome do plano de saúde
        ('tipo_plano_saude', models.CharField(max_length=150)),  # Nome do plano de saúde
        ('coparticipacao', models.DecimalField(max_digits=10, decimal_places=2)),  # Valor da coparticipação
        ('mes', models.DecimalField(max_digits=10, decimal_places=2)),  # Mês de referência para o plano de saúde
        ('funcionario', models.ForeignKey(on_delete=models.CASCADE, to='app.Funcionarios')),
    ],
    options={
        'verbose_name': 'Plano de Salário',
        'verbose_name_plural': 'Planos de Salário',
    },
)

    ]
