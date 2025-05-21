import random
import eel
from nba_api.stats.endpoints import playercareerstats, CommonPlayerInfo, CommonAllPlayers
from nba_api.stats.static import players
import os

# Initialize eel with the 'web' directory
eel.init(os.path.join(os.path.dirname(os.path.realpath(__file__)), "web"))



def getTeamHistory(p_id):
    lst = playercareerstats.PlayerCareerStats(player_id=p_id).get_dict()["resultSets"]
    teamsSet = set()
    for dic in lst:
        if dic["name"] == "SeasonTotalsRegularSeason":
            for year in dic["rowSet"]:
                teamsSet.add(year[4])

    teamsSet.discard("TOT")
    return teamsSet



def getPlayer(name):
    try:
        nba_players = players.get_players()
        name = name.lower()

        # Try to find exact match first
        for player in nba_players:
            # Check full name
            if player['full_name'].lower() == name:
                return {
                    "name": player['full_name'],
                    "id": player['id'],
                    "teams": getTeamHistory(player['id'])
                }
            # Check first name
            if player['first_name'].lower() == name:
                return {
                    "name": player['full_name'],
                    "id": player['id'],
                    "teams": getTeamHistory(player['id'])
                }
            # Check last name
            if player['last_name'].lower() == name:
                return {
                    "name": player['full_name'],
                    "id": player['id'],
                    "teams": getTeamHistory(player['id'])
                }

        # If no exact match, try partial matches
        matching_players = []
        for player in nba_players:
            if name in player['full_name'].lower():
                matching_players.append(player)

        # Return first match if any found, otherwise None
        if matching_players:
            player = matching_players[0]
            return {
                "name": player['full_name'],
                "id": player['id'],
                "teams": getTeamHistory(player['id'])
            }
        return None

    except Exception as e:
        print(f"Error finding player: {e}")
        return None


@eel.expose
def generateGrid():
    allTeams = ["ATL", "BOS", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA",
                "MIL", "MIN", "NOH", "NYK", "BKN", "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS", "TOR", "UTH", "WAS"]

    global grid
    grid = [["", "C1", "C2", "C3"],
            ["R1", "", "", ""],
            ["R2", "", "", ""],
            ["R3", "", "", ""]]

    teams = allTeams[:]

    for i in range(0, 2):
        for k in range(1, 4):
            randNumber = random.randint(0, len(teams) - 1)

            if i == 0:
                grid[i][k] = teams.pop(randNumber)
            else:
                grid[k][0] = teams.pop(randNumber)

    return {"grid": grid}


def checkTeamIntersection(playerTeams, team):
    return team in playerTeams


def checkPT(playerTeams, row, column):
    return checkTeamIntersection(playerTeams, grid[0][column]) and checkTeamIntersection(playerTeams, grid[row][0])


@eel.expose
def checkPlayer(playerName, row, column):
    player = getPlayer(playerName)

    
    if player is None:
        return {
            "success": False,
            "playerFound": False,
            "message": "Player not found"
        }
    
    # Check if player has played for both teams
    success = checkPT(player["teams"], row, column)
    
    return {
        "success": success,
        "playerFound": True,
        "playerName": player["name"],
        "message": "Success!" if success else "Player has not played for both teams"
    }


# Start the Eel application
if __name__ == "__main__":
 
    eel.start("main.html", mode="chrome", size=(1000, 1400))
