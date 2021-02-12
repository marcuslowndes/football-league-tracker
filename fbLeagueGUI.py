from tkinter import *
from tkinter import messagebox  # doesn't work unless i do this
import footballLeague as fbL


def Choose(parent, selecType, makeChoice, dataDict):
    """Return a choice made from a list of integers,
    for use when selecting from a ListBox.
    Returns an error when no choice is made."""
    try: return list(dataDict.keys())[list(map(int, makeChoice))[0]]
    except IndexError or NameError or TypeError:
        messagebox.showerror(
            "Error", f"Please select a {selecType}", parent=parent
        )
        return None


def chooseLeague(leagueChoice, leagues):
    """Creates a global variable choice to be
    carried to the main window when it is created."""
    global choice
    choice = Choose(initWindow, 'league',
                    leagueChoice, leagues)
    if choice is not None: initWindow.destroy()


def displayTeamInfo(teamName, leagueResults):
    """Displays all the information about a selected team."""
    if teamName is not None:  # tI = teamInfo
        tI = list(map(str, fbL.getTeam(teamName, leagueResults)))
        return messagebox.showinfo(teamName, (
            f"Games Played: {tI[0]}\nGames Won: {tI[1]}"
            f"\nGames Drawn: {tI[2]}\nGames Lost: {tI[3]}"
            f"\nGoals For: {tI[4]}\nGoals Against: {tI[5]}"
            f"\nGoal Difference: {tI[6]}\nTotal Points: {tI[7]}"
        ), parent=mainWindow)


def displayWinningTeam(leagueResults):
    """Displays the team that is in First Place."""
    winner = fbL.getWinner(leagueResults)
    return messagebox.showinfo(
        "First Place", winner, parent=mainWindow
    )


def makeUpdate(window, tOne, tOneS, tTwo, tTwoS, lR):
    """Asks the user if they would commit to changing the
    league table and if they do, make the valid changes
    based on their input."""
    if messagebox.askyesno("Commit?", (
            f"Are you sure?\nThis will permanently "
            f"change the league tables.")) is True:
        try:
            lR = fbL.updateTable(
                tOne, tOneS.get(), tTwo, tTwoS.get(), lR
            )
            window.destroy()
            return lR
        except: return messagebox.showerror(
            "Error", "Please enter only integers.", parent=window
        )


def updateResults(lR):  # lR = leagueResults
    """Displays a window allowing the user to add the
    scores from a new match to the league results."""
    matchWindow = Tk()
    matchWindow.title("Add Match")
    matchWindow.resizable(0, 0)

    teamOne = StringVar(matchWindow)
    teamOne.set(fbL.firstKey(lR))
    teamOneScore = IntVar(matchWindow)
    teamOneScore.set(0)

    teamTwo = StringVar(matchWindow)
    teamTwo.set(fbL.firstKey(lR))
    teamTwoScore = IntVar(matchWindow)
    teamTwoScore.set(0)

    Label(matchWindow, text="Team").grid(
        row=0, column=1, padx=10,
    )
    Label(matchWindow, text="Score").grid(
        row=0, column=2, padx=10,
    )

    Label(matchWindow, text="1").grid(
        row=1, column=0, ipadx=5, pady=5
    )
    OptionMenu(matchWindow, teamOne, *lR.keys()).grid(
        row=1, column=1, padx=10,
    )
    scoreOneEnt = Entry(
        matchWindow, width=5, textvariable=teamOneScore
    )
    scoreOneEnt.grid(row=1, column=2, padx=10)

    Label(matchWindow, text="2").grid(
        row=2, column=0, padx=5, pady=10
    )
    OptionMenu(matchWindow, teamTwo, *lR.keys()).grid(
        row=2, column=1, padx=10, pady=10
    )
    scoreTwoEnt = Entry(
        matchWindow, width=5, textvariable=teamTwoScore
    )
    scoreTwoEnt.grid(row=2, column=2, padx=10, pady=10)

    updateBut = Button(
        matchWindow, text="Update Results",
        command=lambda: makeUpdate(
            matchWindow, teamOne.get(), teamOneScore,
            teamTwo.get(), teamTwoScore, lR
        )
    )
    updateBut.grid(row=3, columnspan=3)

    return matchWindow.mainloop()


choice = None
leagueResults = None
leagues = {"English Premier League": "premierLeagueResult.csv",
           "Spanish La Liga": "laLigaTable.csv"}


"""Initial Window for Choosing the League"""
initWindow = Tk()
initWindow.title("Leagues")
initWindow.resizable(0, 0)

Label(initWindow, pady=5, text="Please choose a League.").pack()
leagueOptions = Listbox(initWindow)
leagueOptions.pack(ipadx=20, padx=20, pady=5)
for leagueName, leagueDoc in leagues.items():
    leagueOptions.insert(END, leagueName)

Button(initWindow, width=20, pady=5, text="Choose League",
       bd=3, command=lambda: chooseLeague(
           leagueOptions.curselection(), leagues)
       ).pack()

initWindow.mainloop()


"""Main window for displaying information."""
mainWindow = Tk()
mainWindow.resizable(0, 0)

for leagueName, leagueDoc in leagues.items():
    if choice == leagueName:
        mainWindow.title(leagueName)
        leagueResults = fbL.createLeague(leagueDoc)

leagueTable = LabelFrame(
    bd=5, relief=SUNKEN, labelanchor=N,
    text="Choose a Team to View Info"
)
leagueTable.pack(padx=10, pady=10)

scrollbar = Scrollbar(mainWindow)
scrollbar.pack(in_=leagueTable, side=RIGHT, fill=Y)

teamListbox = Listbox(
    mainWindow, relief=RIDGE, selectborderwidth=3,
    setgrid=2, highlightthickness=0, font='arial',
    width=12, selectbackground='purple',
    yscrollcommand=scrollbar.set
)
teamListbox.pack(in_=leagueTable, ipadx=70)
if choice is not None:
    for team in leagueResults.keys():
        teamListbox.insert(END, team)
scrollbar.config(command=teamListbox.yview)

viewTeamBut = Button(
    mainWindow, text="View Team\nInfo", bd=3,
    command=lambda: displayTeamInfo(Choose(
        mainWindow, 'team', teamListbox.curselection(),
        leagueResults), leagueResults
    ), bg='lightblue'
)
viewTeamBut.pack(side='left', padx=5, ipadx=5, ipady=5)

winningTeamBut = Button(
    mainWindow, text="Display Team\nin First Place", bg='lightgreen',
    command=lambda: displayWinningTeam(leagueResults), bd=3
)
winningTeamBut.pack(side='left', padx=5, ipadx=5, ipady=5)

addNewMatchBut = Button(
    mainWindow, text="Update League\nResults", bg='pink',
    command=lambda: updateResults(leagueResults), bd=3
)
addNewMatchBut.pack(side='left', padx=5, ipadx=5, ipady=5)

if choice is not None:
    mainWindow.mainloop()