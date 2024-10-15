from django.contrib import admin
from django.urls import path
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
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('form/', form, name='form'),
    path('create/', create, name='create'),
    path('indexFuncionarios/', indexFuncionarios, name='indexFuncionarios'),
    path('view/<int:pk>/', view, name='view'),
    path('edit/<int:pk>/', edit, name='edit'),
    path('update/<int:pk>/', update, name='update'),
    path('delete/<int:pk>/', delete, name='delete'),
    
    # Login URLs
    path('login/', user_login, name='user_login'),
    path('createlogin/', createlogin, name='createlogin'),
    
    #manipulação
    path('manipulate_funcionarios/', manipulate_funcionarios, name='manipulate_funcionarios'),

]
