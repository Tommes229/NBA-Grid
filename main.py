import random
from nba_api.stats.endpoints import playercareerstats, CommonPlayerInfo, CommonAllPlayers
import json
import pandas as pd
import numpy as np


def getTeamHistory(p_id):
    lst = playercareerstats.PlayerCareerStats(player_id=p_id).get_dict()["resultSets"]
    teamsSet = set()
    for dic in lst:
        if dic["name"] == "SeasonTotalsRegularSeason":
            for year in dic["rowSet"]:
                teamsSet.add(year[4])

    teamsSet.remove("TOT")
    return teamsSet


def getPlayerName(p_id):
    data = CommonPlayerInfo(player_id=p_id).get_dict()["resultSets"][0]["rowSet"][0]
    return data[3]


def getPlayer(name):
    for player in CommonAllPlayers(False).get_dict()["resultSets"][0]["rowSet"]:
        if name.lower() == player[2].lower():
            return [player[2], player[0], getTeamHistory(player[0])]

    return ["No Player"]


def checkTeamIntersection(playerInf, team):
    return playerInfo[2].isdisjoint(team)


def generateGrid():
    teams = ["ATL", "BOS", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA",
             "MIL", "MIN", "NOH", "NYK", "BKN", "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS", "TOR", "UTH", "WAS"]
    grid = [[" 00", " 01", " 02", " 03"], [" 10", " 11", " 12", " 13"], [" 20", " 21", " 22", " 23"], [" 30", " 31", " 32", " 33"]]

    for i in range(0, 2):
        for k in range(1, 4):
            randNumber = random.randint(0, 29)

            if i == 0:
                grid[i][k] = teams[randNumber]
            else:
                grid[k][0] = teams[randNumber]

            teams.remove(teams[randNumber])
    return grid


def printGrid(grid):
    print(grid[0])
    print(grid[1])
    print(grid[2])
    print(grid[3])


if __name__ == '__main__':
    playerInfo = getPlayer("kevin durant")
    print(playerInfo)
    printGrid(generateGrid())
