import requests
from requests.structures import CaseInsensitiveDict
import json
import datetime

event = {"date": "2022-08-12"}

def wootric (event:dict, context:dict = None):
    

    #Extraindo o token de acesso
    with open('wootric_login.txt') as f:
        username, password= [x.strip("\n") for x in f.readlines()]
        data =  {
                'grant_type': 'password',
                'username': str(username),
                'password': str(password)
            }

    r = requests.post('https://api.wootric.com/oauth/token', data=data)
    token = json.loads(r._content.decode("utf-8"))
    token = token['access_token']
        
    page = 1
    date = event["date"]
    days = 1    

    #Configurando a data dos dados
    date_format = datetime.datetime.strptime(date,"%Y-%m-%d")
    data_inicio = datetime.datetime.timestamp(date_format)
    data_fim = date_format + datetime.timedelta(days=days)
    data_fim = datetime.datetime.timestamp(data_fim)
    data_fim    
    
    #Ajustando a URL da requisição
    url="https://api.wootric.com/v1/responses/"
    url += f"?per_page=50&page={page}"
    url += f'&created[gt]={int(data_inicio)}'
    url += f'&created[lt]={int(data_fim)}'

    #Ajustando os parametros de acesso
    headers = CaseInsensitiveDict()
    headers["Authorization"] = f"Bearer {token}"

    #Fazendo a requisição
    req = requests.get(url, headers=headers)
    resp = json.loads(req._content.decode("utf-8"))
    
    while json.loads(req._content.decode("utf-8")) != []:
        page += 1
        url="https://api.wootric.com/v1/responses/"
        url += f"?per_page=50&page={page}"
        url += f'&created[gt]={int(data_inicio)}'
        url += f'&created[lt]={int(data_fim)}'
        req = requests.get(url, headers=headers)
        resp += json.loads(req._content.decode("utf-8"))
    
    return resp

wootric(event)