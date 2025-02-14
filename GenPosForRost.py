#  GenPosForRost - Update the ROST0000.DSL file with the positions from the previous year-end
#
#  before running this program:
#    1) Copy the ROST0000.DSL file to ROST0000.TXT
#    2) Load the Player_Positions_By_Count table for the previous year
#    3) Generate the Player_Positions_By_Elig for the previous year
#
#  set previous year for season (CCYY format)
#  set database filename to KBSS.db
#  initialize counts
#  open the database connection
#  read the Player_Positions_By_Elig table for the previous year into a list  (ID, C, 1B, 2B, 3B, OF, DH)
#  for each player in the list
#    skip the "None"s
#    convert the position "X" markers to single characters and concatenate them
#
#  open the ROST0000.TXT file
#  read the ROST0000.TXT file into a list
#  close the ROST0000.TXT file
#
#  for each elt in the list
#    if the elt is a player line
#      if the player has ID = 00000000 then
#          overlay the positions with ???
#          write the player to the "missing" file
#
#      else
#        search for the player in the Player_Positions_By_Elig for the previous year
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

import Standard_Declarations
import sqlite3
from sqlite3 import Error
import csv
import sys

#  set current year for season (CCYY format)
PrevSeasonCCYY = 2024

#  set database filename to RotoDB.db
DB = 'C:\\SQLite\\RotoDB\\KBSS.db'

#  initialize counts
CountOfPlayersRead     = 0
CountOfPlayersWrit     = 0
OldPlayerList          = []
NewPlayerList          = []

#  open the RotoDB connection and create a cursor for it
try:
    conn = sqlite3.connect(DB)
    curs = conn.cursor()

#  read the Player_Positions_By_Elig table for the previous year into a dictionary (ID, (C/1/2/S/3/O/D))
    SQLSelect = ('SELECT RW_ID, Elig_C, Elig_1B, Elig_2B, Elig_3B, Elig_SS, Elig_OF, Elig_DH '
                 'FROM Player_Positions_By_Elig WHERE CCYY = ') + str(PrevSeasonCCYY)
    print('sql:', SQLSelect)
    curs.execute(SQLSelect)
    PlayerPosList = curs.fetchall()
#    print('PlayerPos:', PlayerPosList)
#  for each player in the list
#    skip the "None"s
#    convert the position "X" markers to single characters and concatenate them
    for aLine in PlayerPosList:
#        if aLine (0) is not NULL:
#            PosList = ''
#            PosList = PosList + 'C' if aLine (1) == 'X'
        print (aLine [0], aLine [1], aLine [2], aLine [3])
    sys.exit()

    #  open the ROST0000.TXT file
    rosterPathname = 'C:\\ROSTERS\\Rosters ' + str(PrevSeasonCCYY + 1) + '\\'
    print('pathname= ', rosterPathname)
    rosterFilename = rosterPathname + 'ROST0000.TXT'
    print('input filename= ', rosterFilename)
    rosterFile = open(rosterFilename)

#  read the ROST0000.TXT file into a list
    OldPlayerList = rosterFile.readlines()

#  close the ROST0000.TXT file
    rosterFile.close()

#  for each elt in the list
    for aLine in OldPlayerList:
#        print (aLine)

#  if the elt is a player line
        if aLine [0] in ['+','-','?','!','&','/']:
#            print (aLine)

#  if the player has ID = 00000000 then
#    overlay the positions with ???
#    write the player to the "missing" file
            if aLine [19:27]  == '00000000':
                aLine = aLine [0:39] + '???     ' + aLine [47:]
                print (aLine)
#  else
#    search for the player in the Player_Positions_By_Elig for the previous year
#    if the player is found then overlay his positions
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


#    sys.exit()

#  for each player in the list
    for aPlayer in PlayerList:
        PlayerPositionList = []

#  find the max games for the player = max played; if zero then up it to 1, but not more than 20
        maxGames = max(aPlayer[6:16])
        maxGames = max(1,maxGames)
        maxGames = min(20,maxGames)
#        print('max:', maxGames, '=', aPlayer[6:16])

#  for each position
#    if the games played for the player are greater than or equal to the max games
#      append the position to the player's position list
#      set the appropriate column value to 'X'
        EligC = 'X' if aPlayer[6]  >= maxGames else ''
        Elig1 = 'X' if aPlayer[7]  >= maxGames else ''
        Elig2 = 'X' if aPlayer[8]  >= maxGames else ''
        Elig3 = 'X' if aPlayer[9]  >= maxGames else ''
        EligS = 'X' if aPlayer[10] >= maxGames else ''
        EligO = 'X' if aPlayer[14] >= maxGames else ''
        EligD = 'X' if aPlayer[15] >= maxGames else ''
#        print ('pos elig:', aPlayer[1:3], EligC, Elig1, Elig2, EligS, Elig3, EligO, EligD)

#  create a new list with CCYY, player's RW_ID, first name, last name, position(s)
        positionRow = [SeasonCCYY, aPlayer[1], aPlayer[3], aPlayer[4], EligC, Elig1, Elig2, Elig3, EligS, EligO, EligD]

#  append the new list to the AllPlayersPosition list
        AllPlayersPositionList.append(positionRow)
#        print ('all:', AllPlayersPositionList)

#  DELETE the CCYY entries in the Player_Positions_By_Elig table, if they exist
    try:
        curs.execute('DELETE FROM Player_Positions_By_Elig WHERE CCYY = ' + str(SeasonCCYY))
        print('Deleting all entries for:', SeasonCCYY)

    except sqlite3.OperationalError:
        print('No Player_Positions_By_Elig table, creating it')

#  CREATE the Player_Positions_By_Elig table if it doesn't exist
    curs.execute('CREATE TABLE IF NOT EXISTS Player_Positions_By_Elig' +
        '(CCYY         INTEGER,'
        'RW_ID         INTEGER,'
        'First_Name    TEXT,'
        'Last_Name     TEXT,'
        'Elig_C        TEXT,'
        'Elig_1B       TEXT,'
        'Elig_2B       TEXT,'
        'Elig_3B       TEXT,'
        'Elig_SS       TEXT,'
        'Elig_OF       TEXT,'
        'Elig_DH       TEXT)')

#  INSERT the AllPlayersPosition list into the Player_Positions_By_Elig table
    SQLInsert = 'INSERT INTO Player_Positions_By_Elig ' +  \
        '(CCYY, RW_ID, First_Name, Last_Name, Elig_C, Elig_1B, Elig_2B, Elig_3B, Elig_SS, Elig_OF, Elig_DH) ' + \
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
#    print ('ins:', SQLInsert)

    curs.executemany (SQLInsert, AllPlayersPositionList)
    print (curs.rowcount, 'rows inserted')

except Error as err:
    print('connection attempt failed with error:', err)
    conn.close()
    sys.exit()

#  commit the import changes
conn.commit()

#  close the database connection
conn.close()

# sys.exit()