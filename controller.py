import requests
import json
import datetime
import options as o
import os

def get_url_data(url, headers):
  # try to get data from a URL and convert the result into json
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return json.loads(response.text)
    except:
        print("Error accessing URL")

def get_last_season(tournament):
  # access the seasons endpoint and get the latest
  url = f"https://api.sofascore.com/api/v1/tournament/{tournament['id']}/seasons"
  seasons = get_url_data(url, o.headers)
  print(f"Última temporada: {seasons['seasons'][0]['year']}")
  return seasons['seasons'][0]['id']

def get_standings(tournament, season):
  '''
    get the teams playing this tournament in the season by the most recent standing and stores into an object
    the object has 2 properties, id and name, so we can use it to create a menu to choose a team or loop through everyone
    the standings property is a list with 3 items: home + away, home and away, so I pick the first one
  '''
  url = f"https://api.sofascore.com/api/v1/tournament/{tournament['id']}/season/{season}/standings/total"
  standings = get_url_data(url, o.headers)['standings'][0]
  result = []
  for row in standings['rows']:
    data = {}
    data['id'] = row['team']['id']
    data['name'] = row['team']['name']
    result.append(data)
  return result

def get_events(tournament, season, team):
  '''
    Get all the events from a tournament in a specific season, then stores into a list for a specific team
    An event have a status code to determine if the game was finished or not, so I pick only the finished ones
    I pick the id, tournament, converted day, the team, oponent and the goals scored
    I print the count of events just to verify
  '''
  result = []
  url = f"https://api.sofascore.com/api/v1/tournament/{tournament['id']}/season/{season}/events"
  data = get_url_data(url, o.headers)
  events = [item for item in data['events']]
  for event in events:
    if event['status']['code'] == 100 and (event['homeTeam']['name'] == team['name'] or event['awayTeam']['name'] == team['name']):
      event_data = {}
      event_data['id'] = event['id']
      event_data['tournament'] = event['tournament']['name']
      event_data['day'] = datetime.datetime.fromtimestamp(event['startTimestamp']).strftime('%Y-%m-%d')
      event_data['homeTeam'] = event['homeTeam']['name']
      event_data['homeScore'] = event['homeScore']['current']
      event_data['awayTeam'] = event['awayTeam']['name']
      event_data['awayScore'] = event['awayScore']['current']
      result.append(event_data)
  print(f"{len(result)} matches played to date.")
  return result

def get_statistics(events):
  '''
    After gathering the events, for each one, I get the statistics with the get_event_statistics function
  '''
  for event in events:
    statistics = get_event_statistics(event['id'])
    event['statistics'] = statistics
    print(f"{event['homeTeam']} {event['homeScore']}-{event['awayScore']} {event['awayTeam']}")
  return events
    
def get_event_statistics(id):
  '''
    Try to get the statistics for a specific event
    I created a list with the most important stats for me, you can change it in the options.py file
    It has 2 lists, groups and statisticsItems
    I put all the possible stats in a comment, so you can copy and append in the lists
    The statistics object is a list with 3 items: full Period, first half and second half, so I pick the first item
  '''
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

def check_if_folder_exists(tournament):
  '''
    Create a folder with the tournament name if it not exists
  '''
  name = tournament['name']
  if not os.path.exists(f"{name}"):
      os.makedirs(name)
      print(f"Folder {name} successfully created.")
  else:
      print(f"The folder {name} exists already.")
        
def create_file(tournament, team, data):
  '''
    Create the file in the tournament folder if it not exists
  '''
  folder_name = tournament['name']
  file_name = f"{team['name']}.json"
  check_if_folder_exists(tournament)
  path = os.path.join(folder_name, file_name)
  with open(path, 'w') as file:
    json.dump(data, file)
  print(f"File {file_name} successfully created.")