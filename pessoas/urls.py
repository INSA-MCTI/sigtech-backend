from django.urls import path

from . import views

app_name = 'pessoas'

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # CRUD Pessoa
    path('lista/', views.pessoa_lista, name='pessoa_lista'),
    path('criar/', views.pessoa_criar, name='pessoa_criar'),
    path('<int:pk>/', views.pessoa_detalhe, name='pessoa_detalhe'),
    path('<int:pk>/editar/', views.pessoa_editar, name='pessoa_editar'),
    path(
        '<int:pk>/desativar/',
        views.pessoa_desativar,
        name='pessoa_desativar',
    ),

    # Cargo / Unidade
    path(
        '<int:pk>/cargo/add/',
        views.pessoa_cargo_add,
        name='pessoa_cargo_add',
    ),
    path(
        '<int:pk>/unidade/add/',
        views.pessoa_unidade_add,
        name='pessoa_unidade_add',
    ),

    # Agenda
    path('agenda/', views.agenda, name='agenda'),
    path('agenda/evento/', views.evento_criar, name='evento_criar'),
    path('agenda/ferias/', views.evento_ferias, name='evento_ferias'),

    # Arquivos
    path(
        '<int:pk>/arquivo/',
        views.arquivo_upload,
        name='arquivo_upload',
    ),

    # Dados Estatísticos
    path(
        'estatisticos/',
        views.dado_estatistico_lista,
        name='dado_estatistico_lista',
    ),
    path(
        'estatisticos/servidores/',
        views.estatistico_servidores,
        name='estatistico_servidores',
    ),
    path(
        'estatisticos/criar/',
        views.dado_estatistico_criar,
        name='dado_estatistico_criar',
    ),

    # Exportações
    path(
        'exportar/pessoas/',
        views.exportar_pessoas_csv,
        name='exportar_pessoas_csv',
    ),
    path(
        'exportar/estatisticos/',
        views.exportar_estatisticos_csv,
        name='exportar_estatisticos_csv',
    ),

    # Importação
    path(
        'importar/pessoas/',
        views.importar_pessoas_csv,
        name='importar_pessoas_csv',
    ),

    # Auditoria
    path('auditoria/', views.log_auditoria, name='log_auditoria'),
]
