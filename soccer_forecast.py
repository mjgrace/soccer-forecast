import http.client
from datetime import datetime, timedelta
import json
import pprint

SEASON=2024
CURRENT="true"
f = open(".api_key", "r")
API_KEY=f.read()
f.close()

# SEASON_IDS = [39, 253, 140, 135, 61, 262]
SEASON_IDS = [39]
# 39 - Premier League
# 253 - MLS - USA
# 140 - La Liga - Spain
# 135 - Serie A - Italy
# 61 - Ligue 1 - France
# 262 - Liga MX - Mexico
# 78 - Bundesliga - Germany

START_DATE = datetime.today()
time_delta = timedelta(days=7)
END_DATE = START_DATE + time_delta
START_DATE = START_DATE.strftime("%Y-%m-%d")
END_DATE = END_DATE.strftime("%Y-%m-%d")

# # Get current leagues/seasons - only need to run if refreshing - data is saved in JSON file
# conn = http.client.HTTPSConnection("v3.football.api-sports.io")

# headers = {
#     'x-rapidapi-host': "v3.football.api-sports.io",
#     'x-rapidapi-key': API_KEY,
#     'season': SEASON,
#     'current': CURRENT
#     }

# conn.request("GET", "/leagues", headers=headers)

# res = conn.getresponse()
# seasons_data = res.read()

# f = open("test_data/2024_seasons.json", "w")
# f.write(json.dumps(seasons_data.decode("utf-8"), indent=4))
# f.close()

# print(season_data.decode("utf-8"))

for season_id in SEASON_IDS:

    # # Get standings and trend for each league
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': API_KEY,
        }

    conn.request("GET", f"/standings?league={season_id}&season={SEASON}", headers=headers)

    res = conn.getresponse()
    standings_data = res.read()
    standings_data = json.loads(standings_data.decode("utf-8"))

    # # # print(standings_data.decode("utf-8"))

    # f = open("test_data/2024_standings.json", "r")
    # standings_data = json.loads(f.read())
    # f.close()

    standings = {}

    # print(json.dumps(standings_data, indent=2))
    for division in standings_data["response"][0]["league"]["standings"]:
        for standings_result in division:
            standings[standings_result["team"]["id"]] = standings_result
            # print(standings[standings_result["team"]["id"]])
            # print("==============================================")

    # # Get upcoming games/fixtures for each league
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': API_KEY
        }

    conn.request("GET", f"/fixtures?league={season_id}&season={SEASON}&from={START_DATE}&to={END_DATE}", headers=headers)

    res = conn.getresponse()
    fixtures_data = res.read()
    fixtures_data = json.loads(fixtures_data.decode("utf-8"))

    # # print(data.decode("utf-8"))

    # f = open("test_data/2024_fixtures.json", "w")
    # f.write(json.dumps(fixtures_data.decode("utf-8"), indent=4))
    # f.close()

    # f = open("test_data/2024_fixtures.json", "r")
    # fixtures_data = json.loads(f.read())
    # f.close()

    fixtures = fixtures_data["response"]

    for fixture in fixtures:
        print(f'Home: {fixture["teams"]["home"]["name"]}')
        print(f'Rank: {standings[fixture["teams"]["home"]["id"]]["rank"]}')
        print(f'Form: {standings[fixture["teams"]["home"]["id"]]["form"]}')
        print(f'Goal Diff: {standings[fixture["teams"]["home"]["id"]]["goalsDiff"]}')
        print(f'Away: {fixture["teams"]["away"]["name"]}')
        print(f'Rank: {standings[fixture["teams"]["away"]["id"]]["rank"]}')
        print(f'Form: {standings[fixture["teams"]["away"]["id"]]["form"]}')
        print(f'Goal Diff: {standings[fixture["teams"]["away"]["id"]]["goalsDiff"]}')
        print("======================")

    # print(json.dumps(fixtures, indent=2))
