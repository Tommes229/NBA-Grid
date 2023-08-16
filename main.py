import random
from nba_api.stats.endpoints import playercareerstats, CommonPlayerInfo, CommonAllPlayers
import tkinter as tk

teams = []
grid = [[" 00", " 01", " 02", " 03"],
        [" 10", " 11", " 12", " 13"],
        [" 20", " 21", " 22", " 23"],
        [" 30", " 31", " 32", " 33"]]
buttonList = []


def getTeamHistory(p_id):
    lst = playercareerstats.PlayerCareerStats(player_id=p_id).get_dict()["resultSets"]
    teamsSet = set()
    for dic in lst:
        if dic["name"] == "SeasonTotalsRegularSeason":
            for year in dic["rowSet"]:
                teamsSet.add(year[4])

    teamsSet.discard("TOT")
    return teamsSet


def getPlayerName(p_id):
    data = CommonPlayerInfo(player_id=p_id).get_dict()["resultSets"][0]["rowSet"][0]
    return data[3]


def getPlayer(name):
    for player in CommonAllPlayers(False).get_dict()["resultSets"][0]["rowSet"]:
        if name.lower() == player[2].lower():
            return [player[2], player[0], getTeamHistory(player[0])]

    return None


def generateGrid():
    allTeams = ["ATL", "BOS", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA",
                "MIL", "MIN", "NOH", "NYK", "BKN", "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS", "TOR", "UTH", "WAS"]

    global grid
    grid = [[" 00", " 01", " 02", " 03"],
            [" 10", " 11", " 12", " 13"],
            [" 20", " 21", " 22", " 23"],
            [" 30", " 31", " 32", " 33"]]

    maxTeamNumber = 29
    selTeams = []

    for i in range(0, 2):
        for k in range(1, 4):
            randNumber = random.randint(0, maxTeamNumber)

            if i == 0:
                grid[i][k] = allTeams[randNumber]
            else:
                grid[k][0] = allTeams[randNumber]

            selTeams.append(allTeams[randNumber])
            allTeams.remove(allTeams[randNumber])
            maxTeamNumber = maxTeamNumber - 1

    # return grid
    return selTeams


def printGrid(grid):
    print(grid[0])
    print(grid[1])
    print(grid[2])
    print(grid[3])


def createTkGrid():
    window = tk.Tk()
    window.title("NBA - Grid")
    window.geometry('300x200')

    teamsGrid = generateGrid()

    # random teams
    c = 0
    for i in range(0, 2):
        for k in range(1, 4):
            if i == 0:
                tk.Label(window, text=teamsGrid[c]).grid(row=0, column=k)
            else:
                tk.Label(window, text=teamsGrid[c]).grid(row=k, column=0)
            c = c + 1

    # select buttons
    global buttonList
    global selected
    selected = tk.IntVar()
    for i in range(1, 10):
        buttonList.append(tk.Radiobutton(window, text=str(i), value=i, variable=selected))

    c = 0
    for i in range(1, 4):
        for k in range(1, 4):
            buttonList[c].grid(column=k, row=i)
            c = c + 1

    # searchbar
    global playerInp
    playerInp = tk.Text(window, height=1, width=20)
    playerInp.grid(row=4, column=4)
    submit = tk.Button(window, text="submit", command=submitPlayer)
    submit.grid(row=5, column=4)

    window.mainloop()


def checkTeamIntersection(playerInf, team):
    return not playerInf[2].isdisjoint(team)


def checkPT(playerInf, row, column):
    return checkTeamIntersection(playerInf, {grid[0][column]}) and checkTeamIntersection(playerInf, {grid[row][0]})


def getCoord():
    column = selected.get()
    row = 1
    while column > 3:
        column = column - 3
        row = row + 1

    return row, column


def removeField(row, column):
    bPos = row * 3 + column - 4
    print(bPos)
    buttonList[bPos].destroy()


def handleResult(success, row, column):
    if success:
        print("success")
        removeField(row, column)
    else:
        print("no success")


def submitPlayer():
    playerName = playerInp.get(1.0, "end-1c")
    playerInf = getPlayer(playerName)

    if playerInf is not None:
        row, column = getCoord()

        if column == 0:
            print("No field selected!")
        else:
            handleResult(checkPT(playerInf, row, column), row, column)
    else:
        print("No Player!")


if __name__ == '__main__':
    createTkGrid()
