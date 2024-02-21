import requests
import json
import datetime
import options as o
import os

def get_url_data(url, headers):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return json.loads(response.text)
    except:
        print("Erro ao acessar a URL")

def get_last_season(campeonato):
  url = f"https://api.sofascore.com/api/v1/tournament/{campeonato['id']}/seasons"
  seasons = get_url_data(url, o.headers)
  print(f"Temporada {seasons['seasons'][0]['year']}")
  return seasons['seasons'][0]['id']

def get_events(tournament, season):
  result = []
  url = f"https://api.sofascore.com/api/v1/tournament/{tournament['id']}/season/{season}/events"
  data = get_url_data(url, o.headers)
  events = [item for item in data['events']]
  for event in events:
    if event['status']['code'] == 100:
      event_data = {}
      event_data['id'] = event['id']
      event_data['campeonato'] = event['tournament']['name']
      event_data['dia'] = datetime.datetime.fromtimestamp(event['startTimestamp']).strftime('%Y-%m-%d')
      event_data['timeCasa'] = event['homeTeam']['name']
      event_data['golsCasa'] = event['homeScore']['current']
      event_data['timeFora'] = event['awayTeam']['name']
      event_data['golsFora'] = event['awayScore']['current']
      result.append(event_data)
  print(f"{len(result)} jogos realizados.")
  return result

def get_statistics(events):
  for event in events:
    statistics = get_event_statistics(event['id'])
    event['statistics'] = statistics
    print(f"{event['timeCasa']} {event['golsCasa']}-{event['golsFora']} {event['timeFora']}")
  return events
    
def get_event_statistics(id):
    result = []
    url = f"https://api.sofascore.com/api/v1/event/{id}/statistics"
    data = get_url_data(url, o.headers)
    statistics = data['statistics'][0]
    for g in statistics['groups']:
        if g['groupName'] in o.groups:
            items = g['statisticsItems']
            for i in items:
                if i['name'] in o.statisticsItems:
                    result.append(i)
    return result

def check_if_folder_exists(campeonato):
    nome = campeonato['nome']
    if not os.path.exists(f"{nome}"):
        os.makedirs(nome)
        print(f"Pasta {nome} criada com sucesso.")
    else:
        print(f"A pasta {nome} já existe.")
        
def create_file(campeonato, dados):
    nome_pasta = campeonato['nome']
    nome_arquivo = f"{nome_pasta}.json"
    check_if_folder_exists(campeonato)
    caminho = os.path.join(nome_pasta, nome_arquivo)
    with open(caminho, 'w') as arquivo:
        json.dump(dados, arquivo)
    print(f"Arquivo JSON {nome_arquivo} criado com sucesso.")