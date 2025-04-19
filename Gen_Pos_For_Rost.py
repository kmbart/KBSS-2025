#  Gen_Pos_For_Rost - Update the ROST0000.DSL file with positions
#    This will use the Player_Postiions_By_Elig table

#  before running this program:
#    1) Load the Player_Positions_By_Count table for the previous year
#    2) Generate the Player_Positions_By_Elig for the previous year
#
#  set current season (CCYY format)
#  set database filename to KBSS.db
#  initialize counts
#  open the database connection
#  read the Player_Positions_By_Elig table into a list  (ID, C, 1B, 2B, 3B, OF, DH)
#  for each player in the list
#    skip the "None"s
#    convert the position "X" markers to single characters and concatenate them
#
#  open the ROST0000.DSL file
#  read the ROST0000.DSL file into a list
#  close the ROST0000.DSL file
#
#  for each elt in the list
#    if the elt is a player line
#      if the player has ID = 00000000 then
#          overlay the positions with ???
#          write the player to the "missing" file
#
#      else
#        search for the player in the Player_Positions_By_Elig
#        if the player is found then overlay his positions
#
#        else
#          search for the player in the year-before-last
#          if the player is found then overlay his positions
#
#          else
#            overlay the positions with ???
#            write the player to the "missing" file
#
#    append the modified elt to the new list
#
#  open the ROST0000.POS file
#  write the new list to the ROST0000.POS file
#  close the ROST0000.POS file
#
#  close the database connection

import Standard_Declarations as SD

#  set current year for season (CCYY format)
SeasonCCYY = 2025
# Weeks = SD.weeks[SeasonCCYY]

#  set the database name
DBName = SD.MainPathName + str(SeasonCCYY) + '\\Database\\KBSS.db'
print ('database is:', DBName)

#  initialize counts
CountOfPlayersRead     = 0
CountOfPlayersWrit     = 0
MissingPosList         = []
PlayerList             = []
PositionDict           = {}
PrevPositionDict       = {}

#  open the RotoDB connection and create a cursor for it
try:
    conn = SD.sqlite3.connect(DBName)
    curs = conn.cursor()

#  read the Player_Positions_By_Elig table for last year's values into a dictionary
#       (ID, (C/1/2/S/3/O/D))
    SQLSelect = ('SELECT RW_ID, Elig_C, Elig_1B, Elig_2B, Elig_3B, Elig_SS, Elig_OF, Elig_DH '
                 'FROM Player_Positions_By_Elig WHERE CCYY = ') + str(SeasonCCYY - 1)
    print('sql:', SQLSelect)
    curs.execute(SQLSelect)
    PlayerPosList = curs.fetchall()
#    print('PlayerPos:', PlayerPosList)

#  read the Player_Positions_By_Elig table for year before last values into a dictionary
#       (ID, (C/1/2/S/3/O/D))
    SQLSelect = ('SELECT RW_ID, Elig_C, Elig_1B, Elig_2B, Elig_3B, Elig_SS, Elig_OF, Elig_DH '
                 'FROM Player_Positions_By_Elig WHERE CCYY = ') + str(SeasonCCYY - 2)
    print('sql:', SQLSelect)
    curs.execute(SQLSelect)
    PrevPlayerPosList = curs.fetchall()
#    print('PlayerPos:', PlayerPosList)

#  close the database connection
    conn.close()

except OSError as err:
    print('connection attempt failed with error:', err)
    conn.close()
    SD.sys.exit()

#  for each player in the PlayerPosList
#    skip the "None"s
#    convert the position "X" markers to single characters and concatenate them
#    add the new elt to the PositionDict
for aLine in PlayerPosList:
#    print ('id=', aLine [0], 'c=', aLine [1], '1B=', aLine [2], '2B=', aLine [3], '3B=', \
#        aLine[4], 'SS=', aLine[5], 'OF=', aLine[6], 'DH=', aLine[7])
    eligPos = ''
    if aLine [1] == 'X': eligPos = eligPos + 'C'
    if aLine [2] == 'X': eligPos = eligPos + '1'
    if aLine [3] == 'X': eligPos = eligPos + '2'
    if aLine [4] == 'X': eligPos = eligPos + '3'
    if aLine [5] == 'X': eligPos = eligPos + 'S'
    if aLine [6] == 'X': eligPos = eligPos + 'O'
    if aLine [7] == 'X' and eligPos == '': eligPos = 'DH Only'
    PositionDict [aLine [0]] = eligPos
#    print('posDict=', PositionDict)

#  Repeat the position assignments for the PrevPlayerPosList
for aLine in PrevPlayerPosList:
#    print ('id=', aLine [0], 'c=', aLine [1], '1B=', aLine [2], '2B=', aLine [3], '3B=', \
#        aLine[4], 'SS=', aLine[5], 'OF=', aLine[6], 'DH=', aLine[7])
    eligPos = ''
    if aLine [1] == 'X': eligPos = eligPos + 'C'
    if aLine [2] == 'X': eligPos = eligPos + '1'
    if aLine [3] == 'X': eligPos = eligPos + '2'
    if aLine [4] == 'X': eligPos = eligPos + '3'
    if aLine [5] == 'X': eligPos = eligPos + 'S'
    if aLine [6] == 'X': eligPos = eligPos + 'O'
    if aLine [7] == 'X' and eligPos == '': eligPos = 'DH Only'
    PrevPositionDict [aLine [0]] = eligPos
#    print('posDict=', PositionDict)

#  open the ROST0000.DSL file, read it into a list, close the file
rosterFilename = SD.MainPathName + str(SeasonCCYY) + \
   '\\Database\\Rosters\\ROST0000.DSL'
print('input filename= ', rosterFilename)
rosterFile = open(rosterFilename)

PlayerList = rosterFile.readlines()
#    print('ROST0000 list:', PlayerList)

rosterFile.close()

#  open the ROST0000.POS file
newposFilename = SD.MainPathName + str(SeasonCCYY) + '\\Database\\Rosters\\ROST0000.POS'
print('newpos filename= ', newposFilename)
newposFile = open(newposFilename, 'w')

#  for each elt in the list
for aLine in PlayerList:

    #  remove the newline characters
    aLine = aLine.rstrip('\n\r')
#    print (aLine)

#  if the elt is a player line
    if aLine [0] in ['+','-','?','!','&','/']:
        if aLine [34] != 'P':

#  if ID = 00000000 then overlay the positions with ??? and write it to the "missing" file
#  else
#    if the player is in the PositionsDict then overlay the positions
#    else overlay the positions with ??? and write it to the "missing" file
            if aLine [19:27]  == '00000000':
                aLine = aLine [0:39] + '???     ' + aLine [47:]
#                print ('w/zeroes=', aLine)
                MissingPosList.append(aLine)

            else:
                eligPos = PositionDict.get(int(aLine [19:27]))
#                print ('id=', int(aLine [19:27]), 'pos=', eligPos)
                if eligPos == None:
#                    print('no pos=', aLine)
                    eligPos = PrevPositionDict.get(int(aLine[19:27]))
#                    print('2 yr pos=', eligPos)
                    if eligPos == None:
                        eligPos = '???'
#                        print('w/o pos=', aLine)
                        aLine = aLine[0:39] + aLine[47:]
                        MissingPosList.append(aLine)

                aLine = aLine[0:39] + eligPos.ljust(8) + aLine[47:]

    print (aLine, file=newposFile)
#    print ('to newpos', aLine)

newposFile.close()

#  open the MISSING.TXT file, write the MissingPosList, close the file
missingFilename = SD.MainPathName + str(SeasonCCYY) + '\\Database\\Rosters\\MISSING.TXT'
print('missing filename= ', missingFilename)
missingFile = open(missingFilename, 'w')

for aLine in MissingPosList:
    print (aLine, file=missingFile)

missingFile.close()
