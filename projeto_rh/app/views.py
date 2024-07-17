
# Create your views here.
from django.shortcuts import render, redirect, resolve_url , get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm, CandidatoForm
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
import pandas as pd
import locale
from django.utils.safestring import mark_safe
import psycopg2
import psycopg2.pool
import numpy as np
from django.db import connection
from .forms import CandidatoForm, FuncionarioForm
import json
from datetime import datetime, timedelta





# Configuração do pool de conexões
connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,
    user="gueltdbmaster",
    password="gueltdbpassword123",
    host="gueltdatabase-01.c3qxaey67bfc.us-east-1.rds.amazonaws.com",
    port="5432",
    database="postgres",
    options="-c search_path=guelt_db_schema"
)


def home_view(request):
    return render(request, 'app/home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'app/register.html', {'form': form})

def login_view(request):
    next_url = request.GET.get('next', '/protected/')  # Define um valor padrão para next
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next', '/protected/')  # Define um valor padrão para next
                return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form, 'next': next_url})

def logout_view(request):
    logout(request)
    return redirect('login')



########################## FUNÇÕES DE PRIMEIRA PÁGINA ######################################


def puxando(search_query=None):
    connection = None
    cursor = None

    try:
        connection = connection_pool.getconn()
        connection.autocommit = True
        cursor = connection.cursor()

        # Construir a consulta SQL dinamicamente com base na busca
        if search_query:
            sql = """
            SELECT id_candidato, "data", nome, idade, formacao, hist_prof,
                   foco, pret_sal, cinco_anos, pq_guelt, certificado,
                   observacao, status, data_envio
            FROM guelt_main.banco_de_talentos
            WHERE nome ILIKE %s;
            """
            cursor.execute(sql, [f"%{search_query}%"])
        else:
            sql = """
            SELECT id_candidato, "data", nome, idade, formacao, hist_prof,
                   foco, pret_sal, cinco_anos, pq_guelt, certificado,
                   observacao, status, data_envio
            FROM guelt_main.banco_de_talentos;
            """
            cursor.execute(sql)
        
        plan = cursor.fetchall()

        # Criar DataFrame com os dados
        df = pd.DataFrame(plan, columns=[
            "id_candidato", 
            "data", 
            "nome", 
            "idade", 
            "formacao", 
            "hist_prof",
            "foco", 
            "pret_sal", 
            "cinco_anos", 
            "pq_guelt", 
            "certificado",
            "observacao", 
            "status", 
            "data_envio"
        ])

        return df

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection_pool.putconn(connection)



@login_required
@never_cache
def protected_view(request):
    data = puxando()
    search_query = request.GET.get('search', '')
    
    if search_query:
        data = data[data['nome'].str.contains(search_query, case=False, na=False)]

    data = data[['id_candidato','nome', 'formacao', 'hist_prof', 'foco', 'status', 'observacao', 'data_envio']]
    data = data.drop_duplicates(subset=['nome', 'formacao', 'hist_prof', 'foco', 'status', 'observacao'])



    data['data_envio'] = pd.to_datetime(data['data_envio'])
    
    #CalculandO Entrevistas hoje
    qtd_entrevistas_hoje = 0
    hoje = datetime.now().date()
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year
    ontem = hoje - timedelta(days=1)


    qtd_entrevistas_hoje = data[data['data_envio'].dt.date == hoje].shape[0]
    qtd_entrevistas_mes = data[(data['data_envio'].dt.month == mes_atual) & (data['data_envio'].dt.year == ano_atual)].shape[0]
    qtd_entrevistas_ano = data[data['data_envio'].dt.year == ano_atual].shape[0]
    qtd_entrevistas_ontem = data[data['data_envio'].dt.date == ontem].shape[0]

    data = data.sort_values(by='data_envio', ascending=False)
    
    # Truncar texto longo e adicionar coluna de detalhes
    max_length = 40
    data['formacao'] = data['formacao'].apply(lambda x: (x[:max_length] + '...') if len(x) > max_length else x)
    data['hist_prof'] = data['hist_prof'].apply(lambda x: (x[:max_length] + '...') if len(x) > max_length else x)
    data['observacao'] = data['observacao'].apply(lambda x: (x[:max_length] + '...') if len(x) > max_length else x)
    data['Detalhes'] = data['id_candidato'].apply(lambda x: f'<a href="/detalhes/{x}">Detalhes</a>')

    # Dados para o gráfico
    data['mes'] = data['data_envio'].dt.strftime('%Y-%m')
    entrevistas_por_mes = data['mes'].value_counts().sort_index()

    labels = list(entrevistas_por_mes.index.astype(str))
    valores = list(map(int, entrevistas_por_mes.values))

    data['data_envio'] = data['data_envio'].dt.strftime('%Y-%m-%d %H:%M:%S')
    data.rename(columns={'nome': 'Nome', 
                         'formacao': 'Formação', 
                         'hist_prof': 'Histórico Profissional',
                         'foco': 'Foco',
                         'status': 'Status',
                         'observacao': 'Observação',
                         'data_envio': 'Data'}, inplace=True)
    
    
    # Converter o DataFrame para HTML sem escapar o HTML
    table_html = data.to_html(classes='table table-striped', index=False, escape=False)


    context = {
        'qtd_entrevistas_hoje': qtd_entrevistas_hoje,
        'qtd_entrevistas_ontem': qtd_entrevistas_ontem,
        'qtd_entrevistas_mes': qtd_entrevistas_mes,
        'qtd_entrevistas_ano': qtd_entrevistas_ano,
        'table_html': mark_safe(table_html),
        'search_query': search_query,
        'labels': json.dumps(labels),
        'valores': json.dumps(valores)
    }

    return render(request, 'app/protected.html', context)




@login_required
@never_cache
def inserir_view(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO guelt_main.banco_de_talentos
                    (id_candidato, "data", nome, idade, formacao, hist_prof, foco, pret_sal, cinco_anos, certificado, observacao, status, data_envio,linkedin, meio, uff, Banco_de_Talentos, Perfil_Comercial, DISC, Comportamento_Entrevista , pontos_forteis, pontos_fracos)
                    VALUES (nextval('guelt_main.banco_de_talentos_id_candidato_seq'::regclass), '', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, [data['nome'], data['idade'], data['formacao'], data['hist_prof'], 
                      data['foco'], data['pret_sal'], data['cinco_anos'],
                      data['certificado'],data['observacao'], data['status'],
                      data['linkedin'], data['meio'],
                      data['uff'], data['Banco_de_Talentos'], data['Perfil_Comercial'],
                      data['DISC'], data['Comportamento_Entrevista'],
                      data['pontos_forteis'], data['pontos_fracos']                   
                      ])
            return redirect('protected_view')
    else:
        form = FuncionarioForm()
    
    context = {'form': form}
    return render(request, 'app/inserir.html', context)



@login_required
@never_cache
def detalhes_view(request, id_candidato):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT     nome, idade, formacao, hist_prof, foco, pret_sal, cinco_anos, certificado, observacao, status, data_envio, 
                       pontos_fracos, pontos_forteis, area_de_interesse, obs2, obs1, comportamento_entrevista, ultima_remuneração, indicação, 
                       disc, perfil_comercial, banco_de_talentos, vaga_aplicada, uff, meio, linkedin, testes
            FROM guelt_main.banco_de_talentos
            WHERE id_candidato = %s
        """, [id_candidato])
        row = cursor.fetchone()
        candidato = {
            'nome': row[0],
            'idade': row[1],
            'formacao': row[2],
            'hist_prof': row[3],
            'foco': row[4],
            'pret_sal': row[5],
            'cinco_anos': row[6],
            'certificado': row[7],
            'observacao': row[8],
            'status': row[9],
            'data_envio': row[10],
            'pontos_fracos': row[11],
            'pontos_forteis': row[12],
            'area_de_interesse': row[13],
            'obs2': row[14],
            'obs1': row[15],
            'comportamento_entrevista': row[16],
            'ultima_remuneracao': row[17],
            'indicacao': row[18],
            'disc': row[19],
            'perfil_comercial': row[20],
            'banco_de_talentos': row[21],
            'vaga_aplicada': row[22],
            'uff': row[23],
            'meio': row[24],
            'linkedin': row[25],
            'testes': row[26]

        }
    context = {
        'candidato': candidato,
        'id_candidato': id_candidato
    }
    return render(request, 'app/detalhes.html', context)

@login_required
@never_cache
def editar_view(request, id_candidato):
    if request.method == 'POST':
        form = CandidatoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE guelt_main.banco_de_talentos
                    SET nome = %s, idade = %s, formacao = %s, hist_prof = %s, foco = %s, pret_sal = %s, cinco_anos = %s, 
                               certificado = %s, observacao = %s, status = %s, data_envio = now(), linkedin = %s, 
                               meio = %s, uff = %s, vaga_aplicada = %s, Banco_de_Talentos = %s, Perfil_Comercial = %s, 
                               DISC = %s, Indicação = %s, Ultima_Remuneração = %s, Comportamento_Entrevista = %s, 
                               OBS1 = %s, OBS2 = %s, Area_de_interesse = %s, pontos_forteis = %s, pontos_fracos = %s , testes = %s
                    WHERE id_candidato = %s
                """, [
                    data['nome'], data['idade'], data['formacao'], data['hist_prof'], 
                    data['foco'], data['pret_sal'], data['cinco_anos'], data['certificado'],
                    data['observacao'], data['status'], data['linkedin'], data['meio'],
                    data['uff'], data['vaga_aplicada'], data['Banco_de_Talentos'], data['Perfil_Comercial'],
                    data['DISC'], data['Indicação'], data['Ultima_Remuneração'], data['Comportamento_Entrevista'],
                    data['OBS1'], data['OBS2'], data['Area_de_interesse'], data['pontos_forteis'], data['pontos_fracos'], data['testes'],
                    id_candidato
                ])
            return redirect('detalhes', id_candidato=id_candidato)
    else:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT nome, idade, formacao, hist_prof, foco, pret_sal, cinco_anos, certificado, observacao, status, data_envio, 
                        pontos_fracos, pontos_forteis, area_de_interesse, obs2, obs1, comportamento_entrevista, ultima_remuneração, indicação, 
                        disc, perfil_comercial, banco_de_talentos, vaga_aplicada, uff, meio, linkedin, testes
                FROM guelt_main.banco_de_talentos
                WHERE id_candidato = %s
            """, [id_candidato])
            row = cursor.fetchone()
            initial_data = {
                'nome': row[0],
                'idade': row[1],
                'formacao': row[2],
                'hist_prof': row[3],
                'foco': row[4],
                'pret_sal': row[5],
                'cinco_anos': row[6],
                'certificado': row[7],
                'observacao': row[8],
                'status': row[9],
                'data_envio': row[10],
                'pontos_fracos': row[11],
                'pontos_forteis': row[12],
                'area_de_interesse': row[13],
                'OBS1': row[14],
                'OBS2': row[15],
                'Comportamento_Entrevista': row[16],
                'Ultima_Remuneração': row[17],
                'Indicação': row[18],
                'DISC': row[19],
                'perfil_comercial': row[20],
                'banco_de_talentos': row[21],
                'vaga_aplicada': row[22],
                'uff': row[23],
                'meio': row[24],
                'linkedin': row[25],
                'testes': row[26]
            }
        form = CandidatoForm(initial=initial_data)

    context = {
        'form': form,
        'id_candidato': id_candidato
    }
    return render(request, 'app/editar.html', context)