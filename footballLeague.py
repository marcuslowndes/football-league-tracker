def calcPoints(tR):
    """Calculates goal difference (GD)
    and total points for a team."""
    tR[6] = tR[4] - tR[5]  # GD
    tR[7] = 3 * tR[1] + tR[2]  # Points
    return tR


def firstKey(dataDict):
    """Returns the first key of a dict."""
    return list(dataDict.keys())[0]


def createLeague(leagueDocName):
    """Reads the league data from the csv file,
    inputs it into a dictionary and works out the
    goal difference and points for each team."""
    leagueResultsDoc = open(leagueDocName, 'r')
    leagueResults = {}
    l = 0
    for line in leagueResultsDoc:
        if l > 1:  # Skip first 2 lines
            line += ',0,0'
            line = line.split(',')
            teamResults = line[1:8]
            teamResults.append(line[8].rstrip('\n'))
            teamResults = list(map(int, teamResults))
            leagueResults[line[0]] = calcPoints(teamResults)
        l += 1
    leagueResultsDoc.close()
    return leagueResults


def getTeam(teamName, leagueResults):
    """Returns all results for a team."""
    for team in leagueResults:
        if teamName == team:
            return leagueResults[team]


def getWinningTeams(minMax, winningTeams, resultIndex):
    """Finds the team with the number of a specified
    result, e.g. least matches lost."""
    resultList = []
    teamDict = {}
    for team, results in winningTeams.items():
        resultList.append(results[resultIndex])
    for team, results in winningTeams.items():
        if minMax(resultList) == results[resultIndex]:
            teamDict[team] = results
    return teamDict


def getWinner(leagueResults):
    """Returns the team with the most points and
    least lost matches if there is a draw. If there
    is still a draw, returns team with highest GD."""
    winningTeams = {}
    pointsList = []

    for team, results in leagueResults.items():
        pointsList.append(results[7])
    for team, results in leagueResults.items():
        if max(pointsList) == results[7]:
            winningTeams[team] = [results[3], results[6]]

    if len(winningTeams) == 1:
        return firstKey(winningTeams)
    elif len(winningTeams) > 1:
        leastMatchesLostTeams = getWinningTeams(
            min, winningTeams, 0
        )

        if len(leastMatchesLostTeams) == 1:
            return firstKey(leastMatchesLostTeams)
        elif len(leastMatchesLostTeams) > 1:
            return firstKey(getWinningTeams(
                max, leastMatchesLostTeams, 1
            ))  # Highest GD


def updateTable(teamOne, tOneGoals, teamTwo,
                tTwoGoals, leagueResults):
    """Updates all the results for both teams using
    the number of goals scored in a match."""
    bothTeams = {teamOne: tOneGoals,
                 teamTwo: tTwoGoals}

    if tOneGoals == tTwoGoals: winner = 'draw'
    elif tOneGoals > tTwoGoals: winner = teamOne
    else: winner = teamTwo

    for team, goalsFor in bothTeams.items():
        for eachTeam, results in leagueResults.items():
            if team == eachTeam:
                results[0] += 1
                if winner == team: results[1] += 1
                elif winner == 'draw': results[2] += 1
                elif winner != team: results[3] += 1
                results[4] += goalsFor
                for otherTeam, goalsAgainst in bothTeams.items():
                    if otherTeam != team: results[5] += goalsAgainst
                leagueResults[team] = calcPoints(results)
    return leagueResults

