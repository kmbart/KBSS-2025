#  CompareWklyStats-2025: Compare category totals for each team between RotoWire and the KBSS standings.
#  Uses two parameters - the season = CCYY and the stat week = MMDD
#  Read in KBSS standings and pull out category totals for each team, then store them in the KS dictionary.
#  Read in Rotowire standings and pull out category totals for each team, then store them in the RW dictionary.
#  Compare the RW category entries with the equivalent KS entries; if they differ, put them on a new list.
#  Show the differences or confirm they match.

#  Read in KBSS standings and pull out category totals for each team, then store them in the KS dictionary.
#    Open the KBSS standings file and read in the contents
#    For each line in the KBSS file
#      If line contains "Totals:"
#        Pull off the team name
#        If line contains "Pitcher"
#          Load KS dictionary with team name and category/value for
#            W (2), SV (2), IP (4.1), H (3), BB (3), ER (3), K (3),ERA (2.3), WHIP (2.3)
#        If line contains "Hitter"
#          Load KS dictionary with team name and category/value for
#            AB (4), H (4), HR (3), RBI (3), RS (3), SB (3), BA (1.4)

import Standard_Declarations as SD

SeasonCCYY = '2025'

weekOf = SeasonCCYY + '0415'
print ('Running for the week of: ', weekOf)

reTotals  = SD.re.compile(r'.*Totals')
rePitcher = SD.re.compile(r'.*Pitcher')
reHitter  = SD.re.compile(r'.*Hitter')

pathName = SD.MainPathName + str(SeasonCCYY) + '\\Database'
fileName = '\\Standings-KBSS\\KBSS-Standings-' + weekOf + '-WK.txt'

# print ('path:', pathName, ',file:', fileName)
fullName = pathName + fileName
# fullName = 'C:\\Users\\keith\\Documents\\Fantasy Baseball\\2025\\Database\\Standings-KBSS\\WK20250408.txt'
print ('KBSS filename:', fullName)
KBSSfile = open (pathName + fileName)
linelist = KBSSfile.readlines()
KBSSfile.close()
# print ('lineList:', linelist)
# SD.sys.exit()

KSTotals = {}

for line in linelist:
    if reTotals.search(line):
        teamName = line[3:7]
        if rePitcher.search(line):
            KSTotals.setdefault(teamName + '-W', int(line[56:60]))
            KSTotals.setdefault(teamName + '-SV', int(line[60:64]))
            KSTotals.setdefault(teamName + '-K', int(line[89:94]))
            KSTotals.setdefault(teamName + '-ERA', round(float(line[95:102]), 3))
            KSTotals.setdefault(teamName + '-WHIP', round(float(line[103:110]), 4))
#            print(teamName, 'ERA-raw', line[93:100], ',ERA-float', float(line[93:100]), ',ERA-round', round(float(line[93:100]),3))
#            print(teamName, 'WHIP-raw', line[103:110], ',WHIP-float', float(line[103:110]), ',WHIP-round', round(float(line[103:110]), 4))
#            KSTotals.setdefault(teamName+'-IP',float(line[57:64]))
#            KSTotals.setdefault(teamName+'-PHits',int(line[64:69]))
#            KSTotals.setdefault(teamName+'-BB',int(line[69:74]))
#            KSTotals.setdefault(teamName+'-ER',int(line[74:79]))

        if reHitter.search(line):
#            KSTotals.setdefault(teamName+'-AB', int(line[28:33]))
#            KSTotals.setdefault(teamName+'-HHits', int(line[33:38]))
#            print ('line:', line)
            KSTotals.setdefault(teamName + '-HR', int(line[69:72]))
            KSTotals.setdefault(teamName + '-RBI', int(line[73:77]))
            KSTotals.setdefault(teamName + '-RS', int(line[78:82]))
            KSTotals.setdefault(teamName + '-SB', int(line[84:87]))
            KSTotals.setdefault(teamName + '-BA', round(float(line[89:95]), 4))

#  Read in RW standings and pull out category totals for each team, then store them in the RW dictionary.
#    Open the RW standings file and read in the contents
#    Build dictionary for category lookups
#    Build dictionary for team name lookups
#    Build dictionary for integer vs. floating category values
#    Set skipLine to True
#    For each line in the RW file
#      If the line is 'PDFPDF' set skipLine to False
#      If the line is 'RotoWire Twitter' set skipLine to True
#      If skipLine then skip line
#      If 'Name   Total   Points' or '<https:' then skip line
#      If a category name is found then sent the catgType
#      If a team name found then set the teamName
#      If a numeric value is found then load the RW dictionary with the value

pathName   = SD.MainPathName + str(SeasonCCYY) + '\\Database'
RWfilename = pathName + '\\Standings-Rotowire\\RW-Standings-' + weekOf + '-WK.txt'
print ('RW filename:', RWfilename)
RWfile = open(RWfilename)

linelist = RWfile.readlines()
RWfile.close()

RWTotals = {}
categoryName = ''
RWTeamNames = {'Kops': 'KOPS', 'Chris': 'CRIT', 'Pinball': 'PWIZ', 'BoilerRakers': 'RAKE',
               'So.Philly': 'SQDS', 'Juanna': 'BLEV', 'PMOB': 'PMOB','Lou\'s': 'LOUS',
               'BobsBigBoys': 'BOYS', 'Wall-Aces': 'ACES', 'Wardens': 'WARD', 'Z': 'Z**2'}
RWCategoryNames = {'AVG': 'BA', 'HR': 'HR', 'RBI': 'RBI', 'R': 'RS', 'SB': 'SB', 'ERA': 'ERA', 'SV': 'SV', 'K': 'K',
                   'WHIP': 'WHIP', 'W': 'W'}

preComma = SD.re.compile(r'(.*?),')  # Success!

categoryName = ''
teamName = ''

skipLine = True

for line in linelist:
#    print('line=', line[0:55])

    if line[0:6] == 'PDFPDF':
#    if line[0:17] == 'Export Table Data':  #last half of 2024

        skipLine = False
        continue
    elif line[0:16] == 'RotoWire Twitter':
        skipLine = True
    if skipLine or line == '\n' or line[0:4] == 'Name' or line[0:7] == '<https:':
        continue
    else:
        line = line.replace('\t', ' ')
        line = line.replace('\n', '')
#        print('repline=',line[0:55],'*')

#  pre-2023 the numeric values were on the same line as the HTML formatting for the team name
        if not (line == '' or line == ' '):
            lineElts = line.split(' ')
#            print('line elts:', lineElts)

#  in 2023 the numeric values were on the next line (count, points)
#            if line[0].isdigit() or line[0] == '.'
#               tempVal = lineElts[0]

#  in early 2024 the leagueID&teamID are in front of the numeric values for the count and points
#            if lineElts[0][0:9] == 'leagueID=':
#                tempVal = lineElts[1]
#                print('tempVal:', tempVal)

#  in late 2024 the team name, category value, and points were on the same line
#             else:
#            tempStr = lineElts[0]
#            print('tempStr:', tempStr)

#  in 2025 the layout is:
#    category
#    NAME TOTAL POINTS header
#    team name <tab> <stat value> <tab> <point value>
            tempStr = lineElts[0]
#            print('tempStr:', tempStr)

            catgTemp = RWCategoryNames.get(tempStr, 'None')
            if catgTemp != 'None':
                categoryName = catgTemp
                continue

            teamTemp = RWTeamNames.get(tempStr, 'None')
            if teamTemp != 'None':
                teamName = teamTemp
                tempVal = lineElts[-2]      # workaround for team names with spaces
#                print('tempVal:', tempVal)
#                print('catgName:', categoryName)
#                print('teamName:', teamName)

#    print ('Team Name found:',teamName,', Category Name:',categoryName,'tempVal=',tempVal)
    if categoryName == 'BA':
        teamFloatValue = round(float(tempVal), 4)
        RWTotals.setdefault(teamName + '-' + categoryName, teamFloatValue)

    elif categoryName == 'ERA':
        teamFloatValue = round(float(tempVal), 3)
        RWTotals.setdefault(teamName + '-' + categoryName, teamFloatValue)

    elif categoryName == 'WHIP':
        teamFloatValue = round(float(tempVal), 4)
        RWTotals.setdefault(teamName + '-' + categoryName, teamFloatValue)

    else:
        teamIntValue = int(tempVal)
        RWTotals.setdefault(teamName + '-' + categoryName, teamIntValue)

#    print ('tempStr=',tempStr,'tempVal=',tempVal)

# print (RWTotals)

#    Compare the KS and RW dictionaries and print confirmation message or differences

# print ('KSTotals:',KSTotals)
# print ('RWTotals:',RWTotals)

if KSTotals == RWTotals:
    print('Values match!')

else:
    print('Differences:')
    for k, v in KSTotals.items():
        if k in RWTotals:
            x = RWTotals.get(k, None)
            if v != x:
                print(k, 'has values: KS=', v, 'and RW=', x)
        else:
            print(k, 'not found in RW')

    print('=' * 55)

    for k, v in RWTotals.items():
        if not (k in KSTotals):
            print(k, 'not found in KS')
