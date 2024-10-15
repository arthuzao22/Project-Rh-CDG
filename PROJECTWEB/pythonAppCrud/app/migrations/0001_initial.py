from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Funcionarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150)),
                ('registro', models.CharField(max_length=50)),
                ('funcao', models.CharField(max_length=100)),
                ('data_nascimento', models.DateField()),
                ('data_admissao', models.DateField()),
                ('cpf', models.CharField(max_length=11)),
                ('conta_inter', models.CharField(max_length=20)),
                ('ultimo_exame', models.DateField(null=True, blank=True)),
                ('proximo_exame', models.DateField(null=True, blank=True)),
                ('email', models.EmailField(max_length=100)),
                ('salario', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),  # Campo único para o usuário
                ('password', models.CharField(max_length=128)),  # Campo para armazenar senha (use hashing na aplicação)
            ],
        ),
    ]
