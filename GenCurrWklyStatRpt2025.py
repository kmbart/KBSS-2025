#  GenCurrWklyStatRpt - generate stats on a weekly basis for part or all of a season
#  create a sort order dictionary for player status
#  create a sort order dictionary for roster positions
#
#  create a dictionary for each season (CCYY) with a tuple of the stat dates in each season (MMDD)
#  set current year for season (CCYY format), select that season's weeks tuple
#  set the league name
#  set pathname for database access
#
#  set connection filenames for KBSS
#
#  initialize counts
#
#  connect to the databases
#  create cursors for the databases
#
#  SQL SELECT on the team info
#  sort on team owner's name and create a list of the sorted team names
#
#  for each week in the tuple
#    initialize the counters for the league
#
#    for each team in the league
#      initialize the counters for the team
#      append the team header info to the team page
#      get all the players on the team for that week
#
#      for each player on the team
#        get the stats for that player
#        if the player is active
#          add to the team's stats
#        append the player to the appropriate category (active, reserved, minors, etc.)
#
#      append the active player stats to the team page
#      append the pending player stats to the team page
#      append the reserved player stats to the team page
#      append the minor player stats to the team page
#      append the team stat totals to the team page
#
#      insert the team stat totals into the standings lists
#
#    calculate the standings
#    print the standings
#    for each team
#      print the team page


import Standard_Declarations as SD

# create a template for team stats as a list of dictionary elts
seasonStatsDict = {}
weeklyStatsDict = {}

teamStatsTemplate = {}
teamStatsTemplate['AB'] = 0
teamStatsTemplate['H_Runs'] = 0
teamStatsTemplate['H_Hits'] = 0
teamStatsTemplate['H_HR'] = 0
teamStatsTemplate['H_RBI'] = 0
teamStatsTemplate['H_SB'] = 0
teamStatsTemplate['P_Wins'] = 0
teamStatsTemplate['P_Saves'] = 0
teamStatsTemplate['P_IP'] = 0
teamStatsTemplate['P_Hits'] = 0
teamStatsTemplate['P_BB'] = 0
teamStatsTemplate['P_ERuns'] = 0
teamStatsTemplate['P_K'] = 0

emptyStats = (0,) * 36

# calculate difference of two groups of stats
def calcStatDiff(n, o):
    diff = ('StatDiff'
            , n[1]
            , n[2]
            , n[3]
            , n[4]
            , n[5]  - o[5]
            , n[6]  - o[6]
            , n[7]  - o[7]
            , n[8]  - o[8]
            , n[9]  - o[9]
            , n[10] - o[10]
            , n[11] - o[11]
            , n[12] - o[12]
            , n[13] - o[13]
            , n[14] - o[14]
            , n[15] - o[15]
            , n[16] - o[16]
            , n[17] - o[17]
            , n[18] - o[18]
            , n[19] - o[19]
            , n[20] - o[20]
            , n[21] - o[21]
            , n[22] - o[22]
            , n[23] - o[23]
            , n[24] - o[24]
            , n[25] - o[25]
            , n[26] - o[26]
            , n[27] - o[27]
            , n[28] - o[28]
            , n[29] - o[29]
            , n[30] - o[30]
            , n[31] - o[31]
            , n[32] - o[32]
            , n[33] - o[33]
            , n[34] - o[34]
            , n[35] - o[35]
            )
#    print ('diff:', diff)
    return (diff)


# find eligible positions using a stats tuple and type = 'c'urrent or 'p'revious season
def findPositions(s,t) -> str:
    eligPos = ''

# if hitter then find positions
    if s[18:24] != (0, 0, 0, 0, 0, 0):

# if previous season
        if t == 'p':
            if s[18:24] != (0, 0, 0, 0, 0, 0):
                maxPos = min(20, max(s[18], s[19], s[20], s[21], s[22], s[23]))
            if s[18] >= maxPos:
                eligPos = eligPos + 'C'
            if s[19] >= maxPos:
                eligPos = eligPos + '1'
            if s[20] >= maxPos:
                eligPos = eligPos + '2'
            if s[21] >= maxPos:
                eligPos = eligPos + '3'
            if s[22] >= maxPos:
                eligPos = eligPos + 'S'
            if s[23] >= maxPos:
                eligPos = eligPos + 'O'

# else current (in-season) determination
        else:
            if s[18] > 0:
                eligPos = eligPos + 'C'
            if s[19] > 0:
                eligPos = eligPos + '1'
            if s[20] > 0:
                eligPos = eligPos + '2'
            if s[22] > 0:
                eligPos = eligPos + 'S'
            if s[21] > 0:
                eligPos = eligPos + '3'
            if s[23] > 0:
                eligPos = eligPos + 'O'

#    print ('pos type:', t, s[1], s[2], s[3], eligPos)

    return (eligPos)


# determine if player is hitter or pitcher
def getListType(s, p):  # status, player type
    if s > 1:
        lType = 'E'
    elif p == 'P':
        lType = 'P'
    else:
        lType = 'H'

    return (lType)


# do a SQL SELECT on the stats for a given player for that season & week
def getPlayerStats(sWk, PID):

#    _SQL = 'select * from Weekly_Stats_' + str(sWk)[0:4] + ' where CCYYMMDD = ? and RW_ID = ?'
    _SQL = 'select * from Weekly_Stats_' + str(seasonCCYY) + ' where CCYYMMDD = ? and RW_ID = ?'
    cursKBSS.execute(_SQL, (sWk, PID))
#    print ('swk:', sWk, ',PID:', PID, ',sql:', _SQL)

    return (cursKBSS.fetchone())


# determine if player is hitter or pitcher
def getPlayerType(s, p) -> str:  # stats, position type
#    print ('stats:', s, ',pos:', p)
    if s == None:
#        print ('stats = None')
        if p == '01':
            pType = 'P'
        else:
            pType = 'H'

    elif s[6:24] != (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0):
        pType = 'H'

    else:
        pType = 'P'

#    print ('ptype:', pType)
    return (pType)


# print headers for hitters
def makeHeaderHitters() -> str:
    return ("{:^36}".format('Player')
            + "{:^10}".format('ID')
            + "{:^5}".format('$')
            + "{:^4}".format('Con')
            + "{:^6}".format('AB')
            + "{:^6}".format('Hits')
            + "{:^5}".format('HR')
            + "{:^5}".format('RBI')
            + "{:^5}".format('RS')
            + "{:^5}".format('SB')
            + "{:^7}".format('BA')
            + "{:^11}".format('Positions')
            )


# print headers for pitcher
def makeHeaderPitchers() -> str:
    return ("{:^36}".format('Player')
            + "{:^10}".format('ID')
            + "{:^5}".format('$')
            + "{:^4}".format('Con')
            + "{:^5}".format('W')
            + "{:^4}".format('SV')
            + "{:^10}".format('IP')
            + "{:^4}".format('H')
            + "{:^4}".format('BB')
            + "{:^6}".format('ER')
            + "{:^6}".format('K')
            + "{:^8}".format('ERA')
            + "{:^8}".format('WHIP')
            )


# print hitter stats
def makeHitterStatsStr(s, e) -> str:  # stats, positions

    if s[6] == 0: battingAverage = 0
    else:         battingAverage = s[8] / s[6]

    sStr = ' '.join(
        [' '
            , "{: 4d}".format(s[6])              # AB
            , "{: 5d}".format(s[8])              # hits
            , "{: 4d}".format(s[11])             # HR
            , "{: 4d}".format(s[12])             # RBI
            , "{: 4d}".format(s[7])              # runs
            , "{: 4d}".format(s[13])             # steals
            , "{: 6.4f}".format(battingAverage)  # BA
            , ' <' + e + '>'                     # positions
         ])

    return (sStr)


# print pitcher stats
def makePitcherStatsStr(s) -> str:  # stats

    if s[28] == 0:
        ERA  = 0
        WHIP = 0
    else:
        ERA =  s[34] / s[28]
        WHIP = (s[29] + s[31]) / s[28]

    sStr = ' '.join(
        [' '
            , "{: 3d}".format(s[24])        # wins
            , "{: 3d}".format(s[26])        # saves
            , "{: 7.1f}".format(s[28])      # innings pitched
            , "{: 5d}".format(s[29])        # hits
            , "{: 4d}".format(s[31])        # walks
            , "{: 4d}".format(s[34])        # earned runs
            , "{: 5d}".format(s[35])        # strikeouts
            , "{: 7.3f}".format(9 * ERA)    # ERA
#            , "{: 7.3f}".format(WHIP)       # WHIP
            , "{: 8.4f}".format(WHIP)  # WHIP
         ])
#    print ('p str:', sStr)
    return (sStr)


# print player info
def makePlayerInfoStr(p,s) -> str:  # player,seasonYYstr
    if (p[5] >= 2.50 and p[6] != 'F') or (p[6] == seasonYYstr):
        aster = '*'
    else:
        aster = ' '

    status = '  ' + p[0][0]
#    print (p[2], p[3], 'id:', p[4], 'status:', status)
    if status == '  P':
        status = '!!!'
    elif status == '  O':
        status = '???'

    infoStr = ' '.join(
        ["{:>3s}".format(aster)                     # asterisk
            , "{:>3s}".format(status)               # status
            , "{:2s}".format(p[1])                  # position
            , "{:25s}".format(p[3] + ' ' + p[2])    # full name
            , "{:0>8d}".format(p[4])                # ID
            , "{: >5.2f}".format(p[5])              # salary
            , "{:2s}".format(p[6])                  # contract
         ])

    return (infoStr)


# print hitter stat totals for a team
def makeTeamHitterTotalsStr(l, t) -> str:  # league, team
    totStr = ' '.join(
        ['  ', t                                 # team abbr
            , ' - Hitter Totals:                             '
            , "{: 5d}".format(l[t]['AB'])                     # AB
            , "{: 5d}".format(l[t]['H_Hits'])                 # hits
            , "{: 4d}".format(l[t]['H_HR'])                   # HR
            , "{: 4d}".format(l[t]['H_RBI'])                  # RBI
            , "{: 4d}".format(l[t]['H_Runs'])                 # runs
            , "{: 4d}".format(l[t]['H_SB'])                   # steals
            , "{: 6.4f}".format(l[t]['H_Hits'] / l[t]['AB'])  # BA
         ])

    return (totStr)


# print pitcher stat totals for a team
def makeTeamPitcherTotalsStr(l, t) -> str:  # league, team
#    print ('team:', t, 'IP:', l[t]['P_IP'])
    if l[t]['P_IP'] == 0:
        tempERA  = 0
        tempWHIP = 0
    else:
        tempERA  = 9 * (l[t]['P_ERuns'] / l[t]['P_IP'])
        tempWHIP = (l[t]['P_Hits'] + l[t]['P_BB']) / l[t]['P_IP']

    totStr = ' '.join(
        ['  ', t                                   # team abbr
            , ' - Pitcher Totals:                             '
            , "{: 3d}".format(l[t]['P_Wins'])   # wins
            , "{: 3d}".format(l[t]['P_Saves'])  # saves
            , "{: 7.1f}".format(l[t]['P_IP'])   # IP
            , "{: 5d}".format(l[t]['P_Hits'])   # hits
            , "{: 4d}".format(l[t]['P_BB'])     # walks
            , "{: 4d}".format(l[t]['P_ERuns'])  # earned runs
            , "{: 5d}".format(l[t]['P_K'])      # strikeouts
            , "{: 7.3f}".format(tempERA)        # ERA
#            , "{: 7.3f}".format(tempWHIP)       # WHIP
            , "{: 8.4f}".format(round(tempWHIP,4))  # WHIP
         ])
#    print ('tot p:', totStr)

    return (totStr)


# sum hitter stats for a team
def sumHitterStats(d, t, s):  # stat dictionary, team, stats
    d[t]['AB'] += s[6]      # AB
    d[t]['H_Runs'] += s[7]  # runs
    d[t]['H_Hits'] += s[8]  # hits
    d[t]['H_HR'] += s[11]   # HR
    d[t]['H_RBI'] += s[12]  # RBI
    d[t]['H_SB'] += s[13]   # steals

#    print ('sumHitterStats:', d)

# sum pitcher stats for a team
def sumPitcherStats(d, t, s):  # stat dictionary, team, stats
#    print ('in sumPitcherStats:', d, ',team:', t, ',stats:', s)
    d[t]['P_Wins'] += s[24]   # wins
    d[t]['P_Saves'] += s[26]  # saves
    d[t]['P_IP'] += s[28]     # innings pitched
    d[t]['P_Hits'] += s[29]   # hits
    d[t]['P_BB'] += s[31]     # walks
    d[t]['P_ERuns'] += s[34]  # earned runs
    d[t]['P_K'] += s[35]      # strikeouts

#   print ('sumPitcherStats:', d)

# put points on list - assumes list is sorted (asc or desc) and that each elt is a tuple of team name
#   and catg value;
#   return a list of tuples that are team name, catg value, and points
def putPointsOnList(n, catgList):  # number of teams, category list (team, value) -> (team, value, points)
# set remaining points to max
# set max team index to max
# set team index to 0
# set loop-at-end to false
    remainingPts = n
    maxTeamIx = n - 1
    teamIx = 0
    loopAtEnd = False

    while not loopAtEnd:
#        print('in outer loop team:', teamIx, ' pts=', remainingPts)
#        print('catgList:', catgList)
#        print('ix:', teamIx, ',team:', catgList[teamIx][0], ',val:', catgList[teamIx][1])
        if teamIx == maxTeamIx:
#            print('at last team:', teamIx, catgList[teamIx][0], ' val=', catgList[teamIx][0], ' pts=', remainingPts)
            catgList[teamIx] += (remainingPts,)

#   elif this value <> next value
#     this list entry gets remaining points
        elif catgList[teamIx][1] != catgList[teamIx + 1][1]:
#            print('diff vals:', teamIx, catgList[teamIx][0], ' val=', catgList[teamIx][1],
#                  teamIx + 1, catgList[teamIx + 1][0], ' val=', catgList[teamIx + 1][1], ' pts=', remainingPts)
            catgList[teamIx] += (remainingPts,)
            remainingPts -= 1

        #   else this value = next value, begin looping through tied teams
        #     set team offset to 0
        #     shared points = remaining points
        #     set loop-at-end to false
        else:
            teamOffset = 0
            sharedPoints = remainingPts
            loopAtEnd = False

            #     while not loop-at-end
            #       if team+offset > max
            #         set loop-at-end to true
            while not loopAtEnd:
#                print('tied at:', teamIx, catgList[teamIx + teamOffset][0], ' val=', catgList[teamIx + teamOffset][0],
#                      ' pts=', remainingPts, 'offset=', teamOffset, 'shared=', sharedPoints)

                if teamIx + teamOffset == maxTeamIx:
#                    print('reached max teams')
                    loopAtEnd = True

                #       if this team+offset value = next value
                #         subtract 1 from remaining points
                #         add remaining points to shared points
                #         add 1 to team offset
                elif catgList[teamIx + teamOffset][1] == catgList[teamIx + teamOffset + 1][1]:
#                    print('tied team:', teamIx + teamOffset)
                    remainingPts -= 1
                    sharedPoints += remainingPts
                    teamOffset += 1

                #       else
                #         set loop-at-end to true
                else:
#                    print('end of tied teams:', teamIx + teamOffset)
                    loopAtEnd = True

            #     shared points = shared points / (offset - 1)
            #     for team in range (team index, team+offset + 1)
            #       list entry gets shared points
            sharedPoints = sharedPoints / (teamOffset + 1)
#            print('shared pts:', sharedPoints)
            for ix in range(teamIx, teamIx + teamOffset + 1):
#                print('shared at:', ix, ' = ', sharedPoints)
                catgList[ix] += (sharedPoints,)

            #     team index = team+offset
            #     subtract 1 from remaining
            teamIx = teamIx + teamOffset
            remainingPts -= 1
#            print('ix after tie but before inc:', teamIx, 'and remaining pts=', remainingPts)

        teamIx += 1

        if teamIx > maxTeamIx:
            loopAtEnd = True
        else:
            loopAtEnd = False

#    print('list with points:', catgList)

    return ()

#   MAIN ROUTINE
# set current and previous years for season (CCYY format), select the weeks tuple, and the league name
leagueName         = 'DSL'
numOfTeams         = 12

seasonCCYY         = 2025
seasonYYstr        = str(seasonCCYY)[2:4]
weeksList          = SD.weeks[seasonCCYY]
prevSeasonCCYY     = seasonCCYY - 1
prevSeasonLastWeek = str(prevSeasonCCYY) + SD.weeks[prevSeasonCCYY][-2]   # '0000' is  the last week in the tuple
prevWeek           = ''

tempPWFilename     = ''
tempPYFilename     = ''

# set pathname for database access
pathNameDB = SD.MainPathName + str(seasonCCYY) + '\\Database\\KBSS.db'

# set pathname for standings
pathNameStdgs = SD.MainPathName + str(seasonCCYY) + '\\Database\\Standings-KBSS'

# initialize counts
countOfWeeks = 0

try:
# connect to the databases
    connKBSS = SD.sqlite3.connect(pathNameDB)

# create cursors for the databases
    cursKBSS = connKBSS.cursor()

# Generate dictionary of previous season's positions for all players
    _SQL = 'select * from Weekly_Stats_' + str(prevSeasonCCYY) + ' where CCYYMMDD = ?'
    lastWk = int(prevSeasonLastWeek)
    cursKBSS.execute(_SQL, (lastWk,))
    previousSeasonPos = cursKBSS.fetchall()
#   2021 EOY stats have incorrect position counts
#    print ('prevPos:', previousSeasonPos)
    prevPosDict = {}
    for px in previousSeasonPos:
        prevPosDict[px[3]] = findPositions(px,'p')
#        print ('id=', px[3], px[1], px[2], '(', prevPosDict[px[3]], ')')

# SQL SELECT on the team info
    _SQL = 'select Team_Abbr, Team_Owner, Team_Name, Team_Phone_Number, Team_Email, Dead_Skipper ' + \
        'from Team_Info where CCYY = ? and League_Abbr = ?'
    cursKBSS.execute(_SQL, (seasonCCYY, leagueName))
#    print ('sel =', _SQL)
# get the results of the SQL call
    teamInfoResults = cursKBSS.fetchall()

# sort on team owner's name and create a list of the sorted team names
    teamAbbrList = [teamTuple[0] for teamTuple in
                    (sorted(teamInfoResults, key=lambda teamInfo: (teamInfo[1].split()[1] + teamInfo[1].split()[0])))]
#    print ('teams:', teamAbbrList)

#    sys.exit()

# for each team in the league create empty season stats list
    for team in teamAbbrList:
        seasonStatsDict[team] = SD.copy.deepcopy(teamStatsTemplate)

#     print ('season stats at start:', seasonStatsDict)

# for each week in the tuple
    for week in weeksList:

        statWeek = str(seasonCCYY) + week

#  Adjust current, previous stat week values and filename for 0000 roster
        if week == '0000':
            statWeek = str(seasonCCYY) + weeksList[-2]
#    Comment out the prevWeek line for the first week of the season
            if weeksList[-2] != weeksList[0]:
                prevWeek = str(seasonCCYY) + weeksList[-3]
            else:
                prevWeek = ''

        currFileName = str(seasonCCYY) + week
        print ('week of:', week, ',statWeek:', statWeek, ',prev:', prevWeek, ',currFileName:', currFileName)

# open temp files for player weekly and year-to-date stat lines
        tempPWFilename = pathNameStdgs + '\\KBSS-Standings-' + \
                         currFileName + '-WK.txt'
        playerWKFile = open(tempPWFilename, 'w')
        tempPYFilename = pathNameStdgs + '\\KBSS-Standings-' + \
                         currFileName + '-YR.txt'
        playerYTDFile = open(tempPYFilename, 'w')
        print('PW file:', tempPWFilename)
        print('PY file:', tempPYFilename)

# for each team in the league
        for team in teamAbbrList:
 #           print ('team:', team)

# initialize lists for extras, hitters, pitchers, team info
            tempYTDExtraList   = []
            tempYTDHitterList  = []
            tempYTDPitcherList = []
            tempYTDTeamList    = []
            tempWKExtraList    = []
            tempWKHitterList   = []
            tempWKPitcherList  = []
            tempWKTeamList     = []

# parse the team info
            teamInfo    = [aTuple for aTuple in teamInfoResults if aTuple[0] == team]
            teamAbbr    = teamInfo[0][0]
            teamOwner   = teamInfo[0][1]
            teamName    = teamInfo[0][2]
            teamPhone   = teamInfo[0][3]
            teamEmail   = teamInfo[0][4]
            teamSkipper = teamInfo[0][5]
            if teamPhone == None: teamPhone = '<no phone>'
            if teamEmail == None: teamEmail = '<no email>'
#            print ('teaminfo:', teamAbbr, ',', teamName, ',', teamOwner, ',',
#                                teamPhone, ',', teamEmail, ',', teamSkipper)

# append the team header info to the team page
            teamHdr = str (teamName
                      + ' ('
                      + teamAbbr
                      + ') '
                      + teamOwner
                      + ','
                      + str(teamPhone)
                      + ','
                      + teamEmail
                      + ','
                      + teamSkipper
                      )

            tempYTDTeamList.append(teamHdr)
            tempWKTeamList.append(teamHdr)

# initialize the stats dictionary for this team
            weeklyStatsDict[teamAbbr] = SD.copy.deepcopy(teamStatsTemplate)

# do a SELECT for this season + week + + league + team to get all the players on the team
            _SQL = 'select Status, Position, Last_Name, First_Name, RW_ID, Salary, Contract from Rosters_' + \
                   str(seasonCCYY) + ' where CCYYMMDD = ? and League = ? and Team = ?'
            cursKBSS.execute(_SQL, (currFileName, leagueName, teamAbbr))
#            print ('sql:', _SQL, 'parms:', currFileName, leagueName, teamAbbr)
            roster = cursKBSS.fetchall()

# sort the roster by status
#            for p in roster:
#                print(p[2], p[3], 'status:', p[0], 'pos:', p[1])
            roster.sort(key=lambda k: str(SD.statusOrder[k[0]]) + SD.positionOrder[k[1]] + k[2] + k[3])
#            print ('sorted:', roster)

            oldStatus = 0
            oldPosition = ' '

            for player in roster:

                playerID = player[4]
#                print ('player:', player[2], player[3], player[4])
                currStatus = SD.statusOrder[player[0]]
#                print ('currStatus:', currStatus)
                currPosition = SD.positionOrder[player[1]]

                currYTDStats = getPlayerStats(statWeek, playerID)
#                print ('player:', player[2], player[3], currStatus)
#                print ('currstats:', currYTDStats);

                playerType = getPlayerType(currYTDStats, currPosition)
#                print ('p type:', playerType)

# if the player was not found then zero out all the stats
                if currYTDStats == None:
                    currYTDStats = emptyStats

# check for break of active pitchers or hitters - change in status or change in position
#                print ('team:', teamAbbr)
#                print ('currStatus:', currStatus, 'oldStatus:', oldStatus)
                if oldStatus != currStatus:
                    if oldStatus == 1:
                        tempWKPitcherList.append(makeTeamPitcherTotalsStr(weeklyStatsDict, teamAbbr))
                        tempWKHitterList.append(makeTeamHitterTotalsStr(weeklyStatsDict, teamAbbr))
                        tempYTDPitcherList.append(makeTeamPitcherTotalsStr(seasonStatsDict, teamAbbr))
                        tempYTDHitterList.append(makeTeamHitterTotalsStr(seasonStatsDict, teamAbbr))

                oldStatus = currStatus
                oldPosition = currPosition

                fileType = getListType(currStatus, playerType)
#                print ('f type:', fileType)
                if fileType == 'E':
                    tempYTDList = tempYTDExtraList
                    tempWKList  = tempWKExtraList
                elif fileType == 'P':
                    tempYTDList = tempYTDPitcherList
                    tempWKList  = tempWKPitcherList
                else:
                    tempYTDList = tempYTDHitterList
                    tempWKList  = tempWKHitterList

                playerInfoStr = makePlayerInfoStr(player,seasonYYstr)
#                print ('pInfo:', playerInfoStr)

                if currYTDStats == None:
                    statsYTDStr = '  <No stats returned>'

                else:
                    if prevWeek != '':
                        prevYTDStats = getPlayerStats(prevWeek, playerID)
                        if prevYTDStats == None:
                            prevYTDStats = emptyStats
                    else:
                        prevYTDStats = emptyStats
#                    print (); print ('prevYTDStats:', prevYTDStats); print ()

# find difference of current and previous week's stats
                    currWKStats = calcStatDiff(currYTDStats, prevYTDStats)
#                    print ('WK diff=', currWKStats)

                    if playerType == 'P':
                        if currStatus == 1:
                            sumPitcherStats(weeklyStatsDict, teamAbbr, currWKStats)
                            if week != '0000':
                                sumPitcherStats(seasonStatsDict, teamAbbr, currWKStats)
                        statsYTDStr = makePitcherStatsStr(currYTDStats)
                        statsWKStr  = makePitcherStatsStr(currWKStats)

                    else:
                        currPos = findPositions(currYTDStats,'c')

                        if prevPosDict.get(playerID) == None:
                            prevPos = ''
                        else:
                            prevPos = prevPosDict[playerID]
                        bothPos = ''
                        if 'C' in prevPos or 'C' in currPos: bothPos += 'C'
                        if '1' in prevPos or '1' in currPos: bothPos += '1'
                        if '2' in prevPos or '2' in currPos: bothPos += '2'
                        if 'S' in prevPos or 'S' in currPos: bothPos += 'S'
                        if '3' in prevPos or '3' in currPos: bothPos += '3'
                        if 'O' in prevPos or 'O' in currPos: bothPos += 'O'
#                        print ('pID=', playerID, ',prev=', prevPos, ',curr=', currPos, 'both=', bothPos)
                        currPos = bothPos

                        if currStatus == 1:
                            sumHitterStats(weeklyStatsDict, teamAbbr, currWKStats)
                            if week != '0000':
                                sumHitterStats(seasonStatsDict, teamAbbr, currWKStats)
#                        print ('hitStats:', currStats)
                        statsYTDStr = makeHitterStatsStr(currYTDStats, currPos)
                        statsWKStr  = makeHitterStatsStr(currWKStats, currPos)

# append the current player's info and stats to the appropriate list
                tempYTDList.append(playerInfoStr + statsYTDStr)
                tempWKList.append(playerInfoStr + statsWKStr)

# insert the contents of each list into the output file
            for aLine in tempYTDTeamList: print('  ' + aLine, file=playerYTDFile)
            for aLine in tempWKTeamList: print('  ' + aLine, file=playerWKFile)

            print(makeHeaderPitchers(), file=playerYTDFile)
            print(makeHeaderPitchers(), file=playerWKFile)

            for aLine in tempYTDPitcherList: print(aLine, file=playerYTDFile)
            for aLine in tempWKPitcherList: print(aLine, file=playerWKFile)

            print(' ', file=playerYTDFile)
            print(' ', file=playerWKFile)

            print(makeHeaderHitters(), file=playerYTDFile)
            print(makeHeaderHitters(), file=playerWKFile)

            for aLine in tempYTDHitterList: print(aLine, file=playerYTDFile)
            for aLine in tempWKHitterList: print(aLine, file=playerWKFile)

            print(' ', file=playerYTDFile)
            print(' ', file=playerWKFile)

            print(' ', team, ' - Reserved and Minor League Players', file=playerYTDFile)
            print(' ', team, ' - Reserved and Minor League Players', file=playerWKFile)

            for aLine in tempYTDExtraList: print(aLine, file=playerYTDFile)
            for aLine in tempWKExtraList: print(aLine, file=playerWKFile)

            print(' ', file=playerYTDFile)
            print(' ', file=playerWKFile)

            print(' ', file=playerYTDFile)
            print(' ', file=playerWKFile)

# save this week as the previous week
        prevWeek = str(seasonCCYY) + week

# close weekly temp file
        playerYTDFile.close()

# create weekly category lists and then calculate points based on those lists
        PWList = sorted([(t[0], t[1]['P_Wins']) for t in weeklyStatsDict.items()], key=lambda k: k[1], reverse=True)
        putPointsOnList(numOfTeams, PWList)
        PSList = sorted([(t[0], t[1]['P_Saves']) for t in weeklyStatsDict.items()], key=lambda k: k[1], reverse=True)
        putPointsOnList(numOfTeams, PSList)
        PKList = sorted([(t[0], t[1]['P_K']) for t in weeklyStatsDict.items()], key=lambda k: k[1], reverse=True)
        putPointsOnList(numOfTeams, PKList)

        PERAList = sorted([(t[0], 0 if t[1]['P_IP'] == 0 \
            else float((t[1]['P_ERuns'] * 9) / t[1]['P_IP'])) \
                for t in weeklyStatsDict.items()], key=lambda k: k[1])
        putPointsOnList(numOfTeams, PERAList)
#        print ('PERAList:', PERAList)

        PWHIPList = sorted([(t[0], 0 if t[1]['P_IP'] == 0 \
            else float((t[1]['P_Hits'] + t[1]['P_BB']) / t[1]['P_IP'])) \
                for t in weeklyStatsDict.items()], key=lambda k: k[1])
        putPointsOnList(numOfTeams, PWHIPList)
#        print ('PWHIPList:', PWHIPList)

        HHRList = sorted([(t[0], t[1]['H_HR']) for t in weeklyStatsDict.items()], key=lambda k: k[1], reverse=True)
        putPointsOnList(numOfTeams, HHRList)
        HRBIList = sorted([(t[0], t[1]['H_RBI']) for t in weeklyStatsDict.items()], key=lambda k: k[1], reverse=True)
        putPointsOnList(numOfTeams, HRBIList)
        HRUNSList = sorted([(t[0], t[1]['H_Runs']) for t in weeklyStatsDict.items()], key=lambda k: k[1], reverse=True)
        putPointsOnList(numOfTeams, HRUNSList)
        HSBList = sorted([(t[0], t[1]['H_SB']) for t in weeklyStatsDict.items()], key=lambda k: k[1], reverse=True)
        putPointsOnList(numOfTeams, HSBList)
        HBAList = sorted([(t[0], 0 if t[1]['AB'] == 0 \
            else float(t[1]['H_Hits'] / t[1]['AB'])) \
                for t in weeklyStatsDict.items()], key=lambda k: k[1],
                    reverse=True)
        putPointsOnList(numOfTeams, HBAList)

# reset weekly category lists
        pointTotals = {}
        for ix in PWList:
            pointTotals[ix[0]] = [ix[2], 0, ix[2]]
        for ix in PSList:
            pointTotals[ix[0]] = [pointTotals[ix[0]][0] + ix[2], pointTotals[ix[0]][1], pointTotals[ix[0]][2] + ix[2]]
        for ix in PKList:
            pointTotals[ix[0]] = [pointTotals[ix[0]][0] + ix[2], pointTotals[ix[0]][1], pointTotals[ix[0]][2] + ix[2]]
        for ix in PERAList:
            pointTotals[ix[0]] = [pointTotals[ix[0]][0] + ix[2], pointTotals[ix[0]][1], pointTotals[ix[0]][2] + ix[2]]
        for ix in PWHIPList:
            pointTotals[ix[0]] = [pointTotals[ix[0]][0] + ix[2], pointTotals[ix[0]][1], pointTotals[ix[0]][2] + ix[2]]

        for ix in HHRList:
            pointTotals[ix[0]] = [pointTotals[ix[0]][0], pointTotals[ix[0]][1] + ix[2], pointTotals[ix[0]][2] + ix[2]]
        for ix in HRBIList:
            pointTotals[ix[0]] = [pointTotals[ix[0]][0], pointTotals[ix[0]][1] + ix[2], pointTotals[ix[0]][2] + ix[2]]
        for ix in HRUNSList:
            pointTotals[ix[0]] = [pointTotals[ix[0]][0], pointTotals[ix[0]][1] + ix[2], pointTotals[ix[0]][2] + ix[2]]
        for ix in HSBList:
            pointTotals[ix[0]] = [pointTotals[ix[0]][0], pointTotals[ix[0]][1] + ix[2], pointTotals[ix[0]][2] + ix[2]]
        for ix in HBAList:
            pointTotals[ix[0]] = [pointTotals[ix[0]][0], pointTotals[ix[0]][1] + ix[2], pointTotals[ix[0]][2] + ix[2]]

        pitRankList = sorted(pointTotals.items(), key=lambda k: k[1][0], reverse=True)
#        print (pitRankList)
        hitRankList = sorted(pointTotals.items(), key=lambda k: k[1][1], reverse=True)
#        print (hitRankList)
        totRankList = sorted(pointTotals.items(), key=lambda k: k[1][2], reverse=True)
#        print (totRankList)

# open standings file for weekly stats
        statsFilename = pathNameStdgs + 'WK' + str(seasonCCYY) + str(week) + '.txt'
        standingsFile = open(statsFilename, 'w')

# print weekly file header
        print(' ', file=standingsFile)
        hdrLine = '  Weekly Stats for: ' + str(seasonCCYY)\
                  + '-' + str(week[0:2]) + '-' + str(week[2:])
        print(hdrLine, file=standingsFile)
        print(' ', file=standingsFile)
        print(' ', file=standingsFile)

# print weekly category standings
        print('         Wins',
            '               Saves',
            '           Strikeouts',
            '              ERA',
            '                   WHIP',
            file=standingsFile)

        for ix in range(0, numOfTeams):
            print('  ', PWList[ix][0], "{: 4d}".format(PWList[ix][1]), "{: 5.1f}".format(PWList[ix][2]), '   ',
                  PSList[ix][0], "{: 4d}".format(PSList[ix][1]), "{: 5.1f}".format(PSList[ix][2]), '   ',
                  PKList[ix][0], "{: 5d}".format(PKList[ix][1]), "{: 5.1f}".format(PKList[ix][2]), '   ',
                  PERAList[ix][0], "{: 7.4f}".format(PERAList[ix][1]), "{: 5.1f}".format(PERAList[ix][2]), '   ',
                  PWHIPList[ix][0], "{: 7.4f}".format(PWHIPList[ix][1]), "{: 5.1f}".format(PWHIPList[ix][2]),
                  file=standingsFile)

        print(' ', file=standingsFile)
        print('          HR',
              '                RBI',
              '                Runs',
              '                SB',
              '                 BA',
              file=standingsFile)
        for ix in range(0, numOfTeams):
            print('  ', HHRList[ix][0], "{: 4d}".format(HHRList[ix][1]), "{: 5.1f}".format(HHRList[ix][2]), '   ',
                  HRBIList[ix][0], "{: 4d}".format(HRBIList[ix][1]), "{: 5.1f}".format(HRBIList[ix][2]), '   ',
                  HRUNSList[ix][0], "{: 4d}".format(HRUNSList[ix][1]), "{: 5.1f}".format(HRUNSList[ix][2]), '   ',
                  HSBList[ix][0], "{: 4d}".format(HSBList[ix][1]), "{: 5.1f}".format(HSBList[ix][2]), '   ',
                  HBAList[ix][0], "{: 7.4f}".format(HBAList[ix][1]), "{: 5.1f}".format(HBAList[ix][2]),
                  file=standingsFile)

        print(' ', file=standingsFile)
        print('   Pitching Points    ', 'Hitting Points      ', 'Total Points', file=standingsFile)
        for ix in range(0, numOfTeams):
            print('  ', pitRankList[ix][0], "{: 10.1f}".format(pitRankList[ix][1][0]), '   ',
                  hitRankList[ix][0], "{: 10.1f}".format(hitRankList[ix][1][1]), '   ',
                  totRankList[ix][0], "{: 10.1f}".format(totRankList[ix][1][2]), file=standingsFile)

# put a spacer line after standings and before team stats
        print (' ', file=standingsFile)
        print (' ', file=standingsFile)

# append the player stat lines to the weekly standings
# close the file; re-open it for read; append it to the standings; close it again; delete it
        playerWKFile.close()
        playerWKFile = open(tempPWFilename, 'r')
        for aLine in playerWKFile:
            print (aLine, end='', file=standingsFile)
        playerWKFile.close()
#        SD.os.remove(tempPWFilename)

# close weekly temp and stats files
        playerYTDFile.close()
        standingsFile.close()


except OSError as err:
    print('KBSS connection attempt failed with error:', err)
    connKBSS.close()
    SD.sys.exit()


# open season temp stats file
statsFilename = pathNameStdgs + 'YR' + str(seasonCCYY) + weeksList[-1] + '.txt'
seasonStatsFile = open(statsFilename, 'w')

# print season file header
print(' ', file=seasonStatsFile)
hdrLine = '  Season Stats as of: ' + str(seasonCCYY)\
          + '-' + str(weeksList[-1][0:2]) + '-' + str(weeksList[-1][2:])
print(hdrLine, file=seasonStatsFile)
print(' ', file=seasonStatsFile)
print(' ', file=seasonStatsFile)

# if not the CURR file, print the season YTD standings
# if week != '0000':

# create season category lists and then calculate points based on those lists
PWList = sorted([(t[0], t[1]['P_Wins']) for t in seasonStatsDict.items()], key=lambda k: k[1], reverse=True)
putPointsOnList(numOfTeams, PWList)
PSList = sorted([(t[0], t[1]['P_Saves']) for t in seasonStatsDict.items()], key=lambda k: k[1], reverse=True)
putPointsOnList(numOfTeams, PSList)
PKList = sorted([(t[0], t[1]['P_K']) for t in seasonStatsDict.items()], key=lambda k: k[1], reverse=True)
putPointsOnList(numOfTeams, PKList)
PERAList = sorted([(t[0], float((t[1]['P_ERuns'] * 9) / t[1]['P_IP'])) for t in seasonStatsDict.items()],
                  key=lambda k: k[1])
putPointsOnList(numOfTeams, PERAList)
PWHIPList = sorted([(t[0], float((t[1]['P_Hits'] + t[1]['P_BB']) / t[1]['P_IP'])) for t in seasonStatsDict.items()],
                   key=lambda k: k[1])
putPointsOnList(numOfTeams, PWHIPList)

HHRList = sorted([(t[0], t[1]['H_HR']) for t in seasonStatsDict.items()], key=lambda k: k[1], reverse=True)
putPointsOnList(numOfTeams, HHRList)
HRBIList = sorted([(t[0], t[1]['H_RBI']) for t in seasonStatsDict.items()], key=lambda k: k[1], reverse=True)
putPointsOnList(numOfTeams, HRBIList)
HRUNSList = sorted([(t[0], t[1]['H_Runs']) for t in seasonStatsDict.items()], key=lambda k: k[1], reverse=True)
putPointsOnList(numOfTeams, HRUNSList)
HSBList = sorted([(t[0], t[1]['H_SB']) for t in seasonStatsDict.items()], key=lambda k: k[1], reverse=True)
putPointsOnList(numOfTeams, HSBList)
HBAList = sorted([(t[0], float(t[1]['H_Hits'] / t[1]['AB'])) for t in seasonStatsDict.items()], key=lambda k: k[1],
                 reverse=True)
putPointsOnList(numOfTeams, HBAList)

# print season category header
print('         Wins',
      '               Saves',
      '           Strikeouts',
      '              ERA',
      '                   WHIP',
      file=seasonStatsFile)

for ix in range(0, numOfTeams):
    print('  ', PWList[ix][0], "{: 4d}".format(PWList[ix][1]), "{: 5.1f}".format(PWList[ix][2]), '   ',
          PSList[ix][0], "{: 4d}".format(PSList[ix][1]), "{: 5.1f}".format(PSList[ix][2]), '   ',
          PKList[ix][0], "{: 5d}".format(PKList[ix][1]), "{: 5.1f}".format(PKList[ix][2]), '   ',
          PERAList[ix][0], "{: 7.4f}".format(PERAList[ix][1]), "{: 5.1f}".format(PERAList[ix][2]), '   ',
          PWHIPList[ix][0], "{: 7.4f}".format(PWHIPList[ix][1]), "{: 5.1f}".format(PWHIPList[ix][2]),
          file=seasonStatsFile)

print(' ', file=seasonStatsFile)
print('          HR',
      '                RBI',
      '                Runs',
      '                SB',
      '                 BA',
      file=seasonStatsFile)
for ix in range(0, numOfTeams):
    print('  ', HHRList[ix][0], "{: 4d}".format(HHRList[ix][1]), "{: 5.1f}".format(HHRList[ix][2]), '   ',
          HRBIList[ix][0], "{: 4d}".format(HRBIList[ix][1]), "{: 5.1f}".format(HRBIList[ix][2]), '   ',
          HRUNSList[ix][0], "{: 4d}".format(HRUNSList[ix][1]), "{: 5.1f}".format(HRUNSList[ix][2]), '   ',
          HSBList[ix][0], "{: 4d}".format(HSBList[ix][1]), "{: 5.1f}".format(HSBList[ix][2]), '   ',
          HBAList[ix][0], "{: 7.4f}".format(HBAList[ix][1]), "{: 5.1f}".format(HBAList[ix][2]),
          file=seasonStatsFile)

# put  season category points on hitting/pitching/overall totals
pointTotals = {}
for ix in PWList:
    pointTotals[ix[0]] = [ix[2], 0, ix[2]]
for ix in PSList:
    pointTotals[ix[0]] = [pointTotals[ix[0]][0] + ix[2], pointTotals[ix[0]][1], pointTotals[ix[0]][2] + ix[2]]
for ix in PKList:
    pointTotals[ix[0]] = [pointTotals[ix[0]][0] + ix[2], pointTotals[ix[0]][1], pointTotals[ix[0]][2] + ix[2]]
for ix in PERAList:
    pointTotals[ix[0]] = [pointTotals[ix[0]][0] + ix[2], pointTotals[ix[0]][1], pointTotals[ix[0]][2] + ix[2]]
for ix in PWHIPList:
    pointTotals[ix[0]] = [pointTotals[ix[0]][0] + ix[2], pointTotals[ix[0]][1], pointTotals[ix[0]][2] + ix[2]]

for ix in HHRList:
    pointTotals[ix[0]] = [pointTotals[ix[0]][0], pointTotals[ix[0]][1] + ix[2], pointTotals[ix[0]][2] + ix[2]]
for ix in HRBIList:
    pointTotals[ix[0]] = [pointTotals[ix[0]][0], pointTotals[ix[0]][1] + ix[2], pointTotals[ix[0]][2] + ix[2]]
for ix in HRUNSList:
    pointTotals[ix[0]] = [pointTotals[ix[0]][0], pointTotals[ix[0]][1] + ix[2], pointTotals[ix[0]][2] + ix[2]]
for ix in HSBList:
    pointTotals[ix[0]] = [pointTotals[ix[0]][0], pointTotals[ix[0]][1] + ix[2], pointTotals[ix[0]][2] + ix[2]]
for ix in HBAList:
    pointTotals[ix[0]] = [pointTotals[ix[0]][0], pointTotals[ix[0]][1] + ix[2], pointTotals[ix[0]][2] + ix[2]]

pitRankList = sorted(pointTotals.items(), key=lambda k: k[1][0], reverse=True)
# print (pitRankList)
hitRankList = sorted(pointTotals.items(), key=lambda k: k[1][1], reverse=True)
# print (hitRankList)

# attach tiebreaker calcs to all teams
for ix in pointTotals:
    ipNum = int (round (3 * seasonStatsDict[ix]['P_IP'],0))
    abNum = seasonStatsDict[ix]['AB']
#    print ('ix:', ix, 'ip:', ipNum, 'ab:', abNum)
    pointTotals[ix].append(ipNum)
    pointTotals[ix].append(abNum)
    pointTotals[ix].append(3 * ipNum + abNum)

# print ('ptTots:', pointTotals)
totRankList = sorted(pointTotals.items(), key=lambda k: (k[1][2],k[1][5]), reverse=True)
# print ('totRk:', totRankList)

print(' ', file=seasonStatsFile)
print('   Pitching Points    ', 'Hitting Points      ', 'Total Points', file=seasonStatsFile)

tieList = []
for ix in range(0, numOfTeams):
    tieStr = str('   3*IP + AB = '
                 + str(3 * totRankList[ix][1][3])
                 + ' + '
                 + str(totRankList[ix][1][4])
                 + ' = '
                 + str(totRankList[ix][1][5])
                 )
    if ((ix > 0 and totRankList[ix - 1][1][2] == totRankList[ix][1][2])
            or (ix < (numOfTeams - 1) and totRankList[ix][1][2] == totRankList[ix + 1][1][2])):
        tieList.append(tieStr)
    else:
        tieList.append(' ')
#       print ('ix:', ix, 'tie:', tieList)
    print('  ', pitRankList[ix][0], "{: 10.2f}".format(pitRankList[ix][1][0]), '   ',
          hitRankList[ix][0], "{: 10.2f}".format(hitRankList[ix][1][1]), '   ',
          totRankList[ix][0], "{: 10.2f}".format(totRankList[ix][1][2]),
          tieList[ix],
          file=seasonStatsFile)

# put a spacer line after title/standings and before team stats
print (' ', file=seasonStatsFile)
print (' ', file=seasonStatsFile)

# append the player stat lines to the season standings
# close the file; re-open it for read; append it to the standings; close it again; delete it
playerYTDFile.close()
playerYTDFile = open(tempPYFilename, 'r')
for aLine in playerYTDFile:
    print (aLine, end='', file=seasonStatsFile)
playerYTDFile.close()
