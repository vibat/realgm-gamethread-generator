#!/usr/bin/python

"""
NBA Game Thread Generator
Ben H
batsmasher@gmail.com
Created May 2017 - Updated July 2017
"""

import requests
import json
import bs4
from HTMLParser import HTMLParser
import time
import re
import nba_py
from nba_py import team, game
from pprint import pprint as pp

from flask import Flask, render_template, request

app = Flask(__name__)

Soup = bs4.BeautifulSoup
h = HTMLParser()
game_summaries = []

BASKETBALL_TEAMS = 2
BASE_URL = 'http://www.espn.com.au/nba/scoreboard/_/date/{0}'

teams = {
    'Atlanta Hawks': 1610612737,
    'Boston Celtics': 1610612738,
    'Brooklyn Nets': 1610612751,
    'Charlotte Hornets': 1610612766,
    'Chicago Bulls': 1610612741,
    'Cleveland Cavaliers': 1610612739,
    'Dallas Mavericks': 1610612742,
    'Denver Nuggets': 1610612743,
    'Detroit Pistons': 1610612765,
    'Golden State Warriors': 1610612744,
    'Houston Rockets': 1610612745,
    'Indiana Pacers': 1610612754,
    'LA Clippers': 1610612746,
    'LA Lakers': 1610612747,
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
    def __init__(self, id, home, away, venue):
        self.id = id
        self.home = home
        self.away = away
        self.venue = venue


class TeamSummary:
    def __init__(self, name, id, record, logo, color1, color2, players, coaches, stats, last5):
        self.name = name
        self.id = id
        self.record = record
        self.logo = logo
        self.color1 = color1
        self.color2 = color2
        self.players = players
        self.coaches = coaches
        self.stats = stats
        self.last5 = last5


class Player:
    def __init__(self, name, age, height, weight, position, number):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        self.position = position
        self.number = number


class Coach:
    def __init__(self, name, coach_type):
        self.name = name
        self.coach_type = coach_type


class TeamStats:
    def __init__(self, fg, fgr, ft, ftr, tpp, tppr, pts, ptsr, reb, rebr, ast, astr, stl, stlr, blk, blkr):
        self.fg = fg
        self.fgr = fgr
        self.ft = ft
        self.ftr = ftr
        self.tpp = tpp
        self.tppr = tppr
        self.pts = pts
        self.ptsr = ptsr
        self.reb = reb
        self.rebr = rebr
        self.ast = ast
        self.astr = astr
        self.stl = stl
        self.stlr = stlr
        self.blk = blk
        self.blkr = blkr


class Last5:
    def __init__(self, record, stats):
        self.record = record
        self.stats = stats


def scrape_data(date):
    url = BASE_URL.format(date)
    print url
    # r = requests.get(url).text
    # open('C:\Users\ASUS\Downloads\espn.html')
    soup = Soup(open('C:\Users\ASUS\Downloads\espn4.html').read(), "html.parser")

    src = h.unescape(
        soup.find("script", text=re.compile("window.espn.scoreboardData")).text.split("=", 1)[1].rstrip(";"))
    game_data = []

    js = json.loads(src[:src.index(";")])
    for i in range(len(js["events"])):
        data = js["events"][i]["competitions"][0]
        game_data.append(data)
    return game_data


def print_data(game_data):
    for gd in game_data:
        pass  # pp(gd)


def get_game_summary(gid):
    for game_summary in game_summaries:
        if game_summary.id == gid:
            return game_summary
    return "Can\'t find the game"


def get_game_summaries(games_data):
    summaries = []
    for gd in games_data:
        team_summaries = get_team_summaries(gd)
        gs = GameSummary(gd['id'],
                         team_summaries[0],
                         team_summaries[1],
                         gd['venue']['fullName'])
        summaries.append(gs)
    return summaries


def get_team_summaries(game_data):
    """
    Lord help me when Basketball becomes a 3 team game
    :param game_data: The JSON to extract game data from
    :return: A list of TeamSummarys
    """

    summaries = []

    for i in range(BASKETBALL_TEAMS):
        t = TeamSummary(
            game_data['competitors'][i]['team']['displayName'],
            get_team_id(game_data['competitors'][i]['team']['displayName']),
            game_data['competitors'][i]['records'][0]['summary'],
            game_data['competitors'][i]['team']['logo'],
            game_data['competitors'][i]['team']['color'],
            game_data['competitors'][i]['team']['alternateColor'],
            None,
            None,
            None,
            None
        )
        summaries.append(t)

    return sorted(summaries, reverse=(game_data['competitors'][0]['homeAway'] == 'away'))


def get_team_id(name):
    """
    Finds the NBA team ID associated with the inputted name
    :param name: The string name of an NBA team
    :return: The NBA team ID
    """
    try:
        return teams[name]
    except LookupError:
        print "Team name not found"


def get_detailed_summary(game_summary):
    """
    Updates the basic GameSummary and returns a more detailed version
    :rtype: GameSummary
    :param game_summary:
    :return: An updated GameSummary with stats, players and coaches
    """


    game_summary.id
    return


def get_team_details(team_summary):
    # type: (TeamSummary) -> TeamSummary

    coaches = []
    players = []

    for coach in nba_py.team.TeamCommonRoster(team_summary.id).coaches():
        coaches.append(Coach(coach["COACH_NAME"],
                             coach["COACH_TYPE"]))

    for player in nba_py.team.TeamCommonRoster(team_summary.id).roster():
        players.append(Player(player["PLAYER"],
                              player["AGE"],
                              player["HEIGHT"],
                              player["WEIGHT"],
                              player["POSITION"],
                              player["NUM"]))

    team_summary.coaches = coaches
    team_summary.players = players

    last5record = ""

    for row in nba_py.team.TeamGameLogs(team_summary.id,season='2016-17', season_type='Regular Season').info()[:5].iterrows():
        last5record += row[1]['MATCHUP'] + " - " + row[1]['WL'] + "\n"

    team_summary.last5 = Last5(last5record,None)

    return team_summary


def get_game_stats(team_id, ngames=None):
    # type: (str, str) -> TeamStats

    if (ngames is not None) and ngames <82:
        pass

    return


@app.route("/get_games/")
def get_games():
    try:
        selected_date = request.args['date'].replace('-', '')

        gd = scrape_data(selected_date)
        pp(gd)
        games = get_game_summaries(gd)

        global game_summaries
        game_summaries = games

        return render_template('index.html', games=games)
    except LookupError:
        return render_template('index.html')


@app.route("/summary/", methods=["POST"])
def summary():
    try:
        gid = request.form['gid']
        gs = get_game_summary(gid)

        global game_summaries
        return render_template('index.html',
                               game=render_template('gamethread.txt', game=gs),
                               games=game_summaries)
    except LookupError:
        return render_template('index.html')


@app.route("/")
def main():
    return render_template('index.html')


if __name__ == "__main__":
    #print nba_py.team.TeamGeneralSplits(get_team_id('Phoenix Suns')).overall()['FG3_PCT_RANK']
    app.run()
    #print nba_py.team.TeamCommonRoster(get_team_id('Phoenix Suns')).coaches()["COACH_NAME"]