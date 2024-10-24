from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from app.views import (
    home,
    form,
    create,
    view,
    edit,
    update,
    delete,
    user_login,
    indexFuncionarios,
    createlogin,
    manipulate_funcionarios,
    form_salario,
    create_salario_funcionario,
    index_salario,
    edit_salario,
    update_salario,
    delete_salario,
    formEditSalario,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'), # login
    path('form/', form, name='form'),
    path('create/', create, name='create'),
    
    # Funcionários URLs
    path('indexFuncionarios/', indexFuncionarios, name='indexFuncionarios'),
    path('view/<int:pk>/', view, name='view'),
    path('edit/<int:pk>/', edit, name='edit'),
    path('update/<int:pk>/', update, name='update'),
    path('delete/<int:pk>/', delete, name='delete'),

    # Login URLs
    path('login', user_login, name='user_login'),
    path('createlogin/', createlogin, name='createlogin'),


    # Manipulação de Funcionários
    path('manipulate_funcionarios/', manipulate_funcionarios, name='manipulate_funcionarios'),

    # Salários dos Funcionários URLs
    path('form_salario/', form_salario, name='form_salario'),
    path('formEditSalario/', formEditSalario, name='formEditSalario'),
    path('create_salario_funcionario/', create_salario_funcionario, name='create_salario_funcionario'),
    path('index_salario/', index_salario, name='index_salario'),
    path('edit_salario/<int:pk>/', edit_salario, name='edit_salario'),
    path('update_salario/<int:pk>/', update_salario, name='update_salario'),
    path('delete_salario/<int:pk>/', delete_salario, name='delete_salario'),
]
