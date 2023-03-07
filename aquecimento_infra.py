import requests
import json
import numpy as np
import pandas as pd
from pandas import json_normalize
from pandas_profiling import ProfileReport

# função para criar uma string formatada a partir de um objeto JSON
def jprint(obj):

    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


# define a url base da api
url_api = f'https://randomuser.me/api/'

#define caminho do arquivo a ser gravado
file_name = 'dados/out.csv'



# Etapa 1: Entendendo os dados
# ===================================


def get_dic_dados(url):
    response = requests.get(url)
    return response

print("Atividade 1")
print("dicionário de dados:")

jprint(get_dic_dados(url_api).json())

# ===================================

#Etapa 2: Coletando dados

# ===================================

#função para retornar dataframe a partir de requisição JSON (recebendo parâmetros)
def get_dataframe(url, qtd, parameters):
    # cria um dataframe a partir de uma requisição à api

    # define a quantidade de resultados desejada
    url_qtd_results = f'{url}?results={qtd}'

    # faz a requisição passando os parâmetros
    response = requests.get(url_qtd_results, params=parameters)

    # define o formato para JSON
    json = response.json()

    # converte para dataframe
    df = pd.DataFrame(json["results"])

    return df

#função para retornar um dataframe a partir de requisiçãqo JSON
def get_df(url, qtd):
    # cria um dataframe a partir de uma requisição à api

    # define a quantidade de resultados desejada
    url_qtd_results = f'{url}?results={qtd}'

    # faz a requisição passando os parâmetros
    response = requests.get(url_qtd_results)

    # define o formato para JSON
    json = response.json()

    # converte para dataframe
    df = pd.DataFrame(json["results"])

    return df


def save_dataframe(df,path):
    from pathlib import Path  
    filepath = Path(path)  
    filepath.parent.mkdir(parents=True, exist_ok=True)  
    df.to_csv(filepath) 


# define os parâmetos da consulta
parameters = {
    "gender": "female"
}

#obtém o dataframe
df = get_dataframe(url_api, 5, parameters)

print("Atividade 2")
#imprime o dataframe
print(df)

#salva o df em arquivo csv
save_dataframe(df,file_name)

# ===================================

#Etapa 3: Manipulando dados

# ===================================

# def format_data(df,country):
#     f'https://randomuser.me/api/?nat={}'

#teste = get_dic_dados(url_api+"?results=10&inc=name,nat,cell,phone")    
#jprint(teste.json())

# ===================================

#4: Analisando dados sem agrupamento 

# ===================================

#função que recebe um dataframe e gera um relatório em HTML
def report_from_df(df):
    profile =  ProfileReport(df,title="Relátorio Atividade 4")
    profile.to_file("Report.html")

url_rep = url_api+"?results=10"

print("Atividade 4 - gera report em HTML")
dp = get_df(url_api,10)
#print(dp)
rtrn = report_from_df(dp)

# ===================================

#Etapa 5: Analisando dados com agrupamento
 
# ===================================


#não completado





