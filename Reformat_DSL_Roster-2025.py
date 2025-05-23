#  Reformat_Roster:  Reformat a roster text file into player and team CSV files.
#  Set up the import of Standard_Declarations and define the regex type(s)
#  Set the SeasonCCYY, Weeks, and Pathname variables
#
#  for each week in the season
#    Open the Roster file
#    Read the entire Roster file into a tuple
#    Close the Roster file
#
#    Open the player and team CSV files
#
#    Read each line in the roster file
#      if the record type is:
#        '*' then change the TeamAbbr
#        '=' then set asterisk trade and write to team CSV file
#        '+' or '-' or '&' or '~' line then
#            parse player (last name, first name, ID, salary, position, contract)
#              and write to player CSV file
#        '$' then parse FAB (month, day, amount, last name, first name) and write to team CSV file
#        '#' then parse pick (year, optional team, round/pick#) and write to team CSV file
#    Close the player and team CSV files
#
#  write counts for number of teams, players per team, etc.

import Standard_Declarations as SD

reCurrent  = SD.re.compile(r'.*Current')

# set current year for season (CCYY format) and select the weeks tuple
#  (there are not rosters for seasons prior to 2018)
SeasonCCYY = 2025
Weeks = SD.weeks[SeasonCCYY]
bypassTypes = {'/':'Free Agent', '%':'Owner', '@':'Email'}
playerTypes = {'+':'Active', '?':'Open', '-':'Reserved', '&':'Minors', '~':'Waived', '!':'Pending'}

rosterPathname = SD.MainPathName + str(SeasonCCYY) + '\\Database\\Rosters\\'
# print('roster pathname= ', rosterPathname)

for Week in Weeks:

# Generate input date (SeasonCCYY + Week)
    inputDate = str(SeasonCCYY) + Week
    inputCCYY = inputDate[0:4]
    inputMMDD = inputDate[4:8]
    teamAbbr = ''
#    print ('inputDate=', inputDate)

    rosterFilename = rosterPathname + 'ROST' + inputMMDD + '.DSL'
    print('input filename= ', rosterFilename)

# Open roster file
    rosterFile = open(rosterFilename)

# Read in roster file
    lineList = rosterFile.readlines()
#    print('roster file:', lineList)

# Close roster file
    rosterFile.close()

    CSVPathname = rosterPathname + 'CSV Files\\'
#    print('CSV pathname= ', CSVPathname)

# Open player CSV file
    CSVPFile = open(CSVPathname + 'CSVP' + inputMMDD + '.txt','w')
# Open team CSV file
    CSVTFile = open(CSVPathname + 'CSVT' + inputMMDD + '.txt','w')

# Read each line in roster file
    lineCnt = 0
    for line in lineList:
        lineCnt += 1
#        if lineCnt > 111: break
    
        lineType = line[0:1]
#        print ('read in type:', lineType, ' on line=', line[0:44])

#        SD.sys.exit()

        # if it is a '*' line, change the TeamAbbr
        if lineType == '*':
            if teamAbbr != '':
                print (inputDate, ',', teamAbbr, ',', 'FAB Remaining  = $', ',', format(round (FABRemaining, 2), "5.2f"), file=CSVTFile)
                print(inputDate, ',', teamAbbr, ',', 'Salary Active   = $', format(round(salaryActive, 2), "5.2f"), file=CSVTFile)
                print(inputDate, ',', teamAbbr, ',', 'Salary Reserved = $', format(round(salaryReserved, 2), "5.2f"),
                  file=CSVTFile)
            teamAbbr = line[1:5]
            FABRemaining   = 10
            salaryActive   = 0
            salaryReserved = 0

#        print ('found abbreviation:', teamAbbr)
        
# if it is a '=' line then set asterisk trade
        elif lineType == '=':
            teamAsterisk = line[16:25].strip()
            print (inputDate, ',', teamAbbr, ',', 'Asterisk', ',', teamAsterisk, file=CSVTFile)

#    if it is a '+' or '-' or '&' or '~' line then ParsePlayer
        elif lineType in playerTypes:
            playerName     = line[1:19]
            names          = playerName.split(',')
#            print ('names:', names)
            lastName       = names[0]
            if len(names) < 2: print ('missing firstName:', names)
            else: firstName      = names[1]
            playerID       = line[19:27]
            playerSalary   = line[28:33]
            playerPos      = line[34:35]
            playerStatus   = playerTypes [lineType]
            if lineType == '&':
                playerContract = 'M '
            else:
                playerContract = line[36:38]
            if playerStatus == 'Active' or playerStatus == 'Open':
                salaryActive = salaryActive + float(playerSalary)
            if playerStatus == 'Reserved' or playerStatus == 'Pending':
                salaryReserved = salaryReserved + float(playerSalary)
            print (inputDate, ',', 'DSL', ',', teamAbbr, ',', playerStatus, ',', playerPos, ',', lastName,
                   ',', firstName, ',', playerID, ',', playerSalary, ',', playerContract, file=CSVPFile)
#            print ('type:', playerStatus, ', salary=', playerSalary, ', act=', salaryActive, ', res=', salaryReserved)

# if it is a '$' line then ParseFab
        elif lineType == '$':
            FABMM      = line[1:3]
            FABDD      = line[4:6]
            FABPrice   = line[25:30]
            FABName    = line[30:55].strip()
            FABLName   = ' '
            FABFName   = ' '
            if FABName != '':
                FABNames   = FABName.split(',')
                FABLName   = FABNames[0]
                FABFName   = FABNames[1]
            print (inputCCYY + FABMM + FABDD, ',', teamAbbr, ',', 'FAB', ',', FABPrice, ',', FABFName, ',', FABLName, file=CSVTFile)
            FABRemaining -= float (FABPrice)

# if it is a '#' line then ParsePick
        elif lineType == '#':
            minorsPick   = line.strip()
            minorsPickYY = '20' + minorsPick [1:3]
            if minorsPick [4:5] == '#':
                thisPick     = minorsPick [4:7]
                thisPickTeam = ' '
            else:
                thisPick     = minorsPick [9:12]
                thisPickTeam = minorsPick [4:8]
            print (inputDate, ',', teamAbbr, ',', 'Pick', ',', minorsPickYY, ',', thisPickTeam, ',', thisPick, file=CSVTFile)

        elif lineType == '/':
            if line[1:5] == 'BUMS':
                print(inputDate, ',', teamAbbr, ',', 'FAB Remaining', ',', format(round (FABRemaining, 2), "5.2f"), file=CSVTFile)
                print(inputDate, ',', teamAbbr, ',', 'Salary Active   = $', format(round(salaryActive, 2), "5.2f"), file=CSVTFile)
                print(inputDate, ',', teamAbbr, ',', 'Salary Reserved = $', format(round(salaryReserved, 2), "5.2f"),
                  file=CSVTFile)

        else:
            if not (lineType in bypassTypes): print ('invalid lineType:', lineType, ' - rejected')

# Close player CSV file
    CSVPFile.close()

# Close team CSV file
    CSVTFile.close()
