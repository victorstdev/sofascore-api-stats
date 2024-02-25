import tournaments as t
import controller as c
import menu as m
import options as o
import time

start = time.time()

tournament = m.choose_option(t.tournaments)
season = c.get_last_season(tournament)
teams = c.get_standings(tournament, season)

for team in teams:
  events = c.get_events(tournament, season, team)
  statistics = c.get_statistics(events)
  file = c.create_file(tournament, team, statistics)

end = time.time()
duration = (end - start) / 60
print(f'Total execution time: {duration:.2f} m')
time.sleep(3)