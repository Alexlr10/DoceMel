from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import *
from . import views



urlpatterns = [

    path('',views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html',redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # USUARIO
    path('usuarios/', views.usuarios, name='usuarios'),
    path('updateusuarios/<int:pk>/', views.usuariosEdit, name='usuarios_edit'),
    path('usuarios/delete/<pk>',
         login_required(usuariosDelete.as_view()), name='usuarios_delete'),
    path('meus_dados/', views.editar_meus_dados, name='meusdados'),

    # Cliente
    path('cliente/', views.cliente, name='cliente'),
    path('cliente_edit/<int:pk>/', views.cliente_edit, name='cliente_edit'),
    path('cliente_delete/<int:pk>/', views.cliente_delete, name='cliente_delete'),

    # Produto
    path('produto/', views.produto, name='produto'),
    path('produto_edit/<int:pk>/', views.produto_edit, name='produto_edit'),
    path('produto_delete/<int:pk>/', views.produto_delete, name='produto_delete'),

    # Estoque
    path('estoque/', views.estoque, name='estoque'),
    path('estoque_edit/<int:pk>/', views.estoque_edit, name='estoque_edit'),
    path('estoque_delete/<int:pk>/', views.estoque_delete, name='estoque_delete'),

    # Compra
    path('compra/', views.compra, name='compra'),
    path('compra_edit/<int:pk>/', views.compra_edit, name='compra_edit'),
    path('compra_delete/<int:pk>/', views.compra_delete, name='compra_delete')


]

