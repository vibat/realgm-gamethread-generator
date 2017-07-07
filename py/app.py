"""
NBA Game Thread Generator
Ben H
batsmasher@gmail.com
May 2017
"""

import requests
import pandas as pd
import json
import BeautifulSoup
import time
import re
import nba_py
from nba_py import team, game
from pprint import pprint as pp
Soup = BeautifulSoup.BeautifulSoup

BASKETBALL_TEAMS = 2
BASE_URL = 'http://www.espn.com/nba/scoreboard/_/date/{0}'
date = time.strftime('%Y%m%d')
url = BASE_URL.format(date)

teams = {
    'Atlanta Hawks' : 1610612737,
    'Boston Celtics' : 1610612738,
    'Brooklyn Nets' : 1610612751,
    'Charlotte Hornets': 1610612766,
    'Chicago Bulls': 1610612741,
    'Cleveland Cavaliers': 1610612739,
    'Dallas Mavericks': 1610612742,
    'Denver Nuggets': 1610612743,
    'Detroit Pistons': 1610612765,
    'Golden State Warriors': 1610612744,
    'Houston Rockets': 1610612745,
    'Indiana Pacers': 1610612754,
    'Los Angeles Clippers': 1610612746,
    'Los Angeles Lakers': 1610612747,
    'Memphis Grizzlies': 1610612763,
    'Miami Heat': 1610612748,
    'Milwaukee Bucks': 1610612749,
    'Minnesota Timberwolves': 1610612750,
    'New Orleans Pelicans': 1610612740,
    'New York Knicks': 1610612752,
    'Oklahoma City Thunder': 1610612760,
    'Orlando Magic': 1610612753,
    'Philadelphia 76ers': 1610612755,
    'Phoenix Suns': 1610612756,
    'Portland Trail Blazers': 1610612757,
    'Sacramento Kings': 1610612758,
    'San Antonio Spurs': 1610612759,
    'Toronto Raptors': 1610612761,
    'Utah Jazz': 1610612762,
    'Washington Wizards': 1610612764
}

class GameSummary:
    def __init__(self,id,home,away):
        self.id = id
        self.home = home
        self.away = away

class TeamSummary:
    def __init__(self,name,id,record,logo,color1,color2):
        self.name = name
        self.id = id
        self.record = record
        self.logo = logo
        self.color1 = color1
        self.color2 = color2


def scrape_data():
    #r = requests.get(url).text
    soup = Soup(open('C:\Users\ASUS\Downloads\espn.html'))

    src = soup.find("script",text=re.compile("window.espn.scoreboardData")).split("=",1)[1].rstrip(";")
    game_data = []

    js = json.loads(src[:src.index(";")])
    for i in range(len(js["events"])):
        data = js["events"][i]["competitions"][0]
        game_data.append(data)
    return game_data


def print_data(game_data):
    for gd in game_data:
        pass #pp(gd)


def get_game_summaries(games_data):
    summaries = []
    for gd in games_data:
        team_summaries = get_team_summaries(gd)
        gs = GameSummary(gd['id'],
                         team_summaries[0],
                         team_summaries[1])
        summaries.append(gs)
    return summaries


def get_team_summaries(game_data):
    """
    Lord help me when Basketball becomes a 3 team game
    :param game_data: The JSON to extract game data from
    :return: A list of TeamSummarys
    """

    ordered = True

    if game_data['competitors'][0]['homeAway'] == 'away': ordered = False

    summaries = []

    for i in range(BASKETBALL_TEAMS):
        t = TeamSummary(
            game_data['competitors'][i]['team']['displayName'],
            get_team_id(game_data['competitors'][i]['team']['displayName']),
            game_data['competitors'][i]['records'][0]['summary'],
            game_data['competitors'][i]['team']['logo'],
            game_data['competitors'][i]['team']['color'],
            game_data['competitors'][i]['team']['alternateColor']
        )
        summaries.append(t)

    return sorted(summaries, reverse=not ordered)


def get_team_id(name):
    return teams[name]


def main():
    gd = scrape_data()
    summaries = get_game_summaries(gd)
    print summaries[0].home.color1
    #print_data(gd)

main()

pd.set_option('display.max_columns', None)

#test = nba_py.Scoreboard(month=5,day=12,year=2017,league_id='00',offset=0)
#print test.available()
#print team.TeamLastNGamesSplits(1610612756).last5()
#print team.TeamGameLogs(1610612756).info()
#print team.TeamSummary(1610612756).info()
