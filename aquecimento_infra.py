import requests
import json
import numpy as np
import pandas as pd
from pandas import json_normalize
from ydata_profiling import ProfileReport

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

proxies = {
   'http': 'http://proxy.rio.rj.gov.br:8080',
   'https':'http://proxy.rio.rj.gov.br:8080',
}

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

def get_dic_dados(url):
    response = requests.get(url,proxies=proxies)#,headers=headers)
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
    response = requests.get(url_qtd_results, params=parameters,proxies=proxies)

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
    response = requests.get(url_qtd_results,proxies=proxies)

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

# faz a requisição passando os parâmetros
response = requests.get(url_api+"?results=10&inc=location",proxies=proxies)

# define o formato para JSON
json = response.json()

# converte para dataframe
df = pd.DataFrame(json["results"])

#normaliza o JSON
dfn=pd.json_normalize(json["results"])

#imprime país e estado
print("país - estado")
print(dfn['location.country']+" - "+dfn['location.state'])

#função para agrupar dataframe por país e estado
def df_group(df):
    dfg = df.groupby(["location.country","location.state"])
    return dfg

#dataframe agrupado
dfg = dfn.groupby(["location.country","location.state"])

#imprime o dataframe
print("dfg")
for key, item in dfg:
    print(dfg.get_group(key), "\n\n")

# ===================================

#Etapa 7: Parametrizando seu código    

# ===================================

#função que recebe argumentos e executa uma query
def custom_query(**kwargs):
    #cria o dicionário de parâmetros
    params = {}
    #adiciona os argumentos recebidos ao dicionário
    for key,value in kwargs.items():
        params[key]=value
    
    #retorna a lista de parâmetros da query
    return params

#cria um parâmetro passando o argumento "gender=female"
p = custom_query(gender="female")

#imprime o parÂmetro criado com a função
print(p)

# passa o parâmetro e cria um dataframe a partir da query
dfp = get_dataframe(url_api,5,p)

#imprime o dataframe
print("dataframe with params")
print(dfp)


#teste