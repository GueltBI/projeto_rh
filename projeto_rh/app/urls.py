from django.urls import path
from .views import register_view, login_view, logout_view, home_view, protected_view, detalhes_view, editar_view, inserir_view

urlpatterns = [
    
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('protected/', protected_view, name='protected_view'),  # Corrigido para 'protected_view'
    path('', login_view, name='login'),
    path('detalhes/<int:id_candidato>/', detalhes_view, name='detalhes'),
    path('editar/<int:id_candidato>/', editar_view, name='editar'),
    path('inserir/', inserir_view, name='inserir'),

]