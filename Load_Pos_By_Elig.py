#  Load_Pos_By_Elig - use the PLayer_Positions_By_Count table to generate position eligibility and store it in a table
#
#  set current year for season (CCYY format)
#  set database filename to KBSS.db
#  initialize counts
#  open the database connection
#
#  read all the player positions for that season into a list
#
#  for each player in the list
#    find the max games for the player = max played; if zero up it to 1, but not more than 20
#    for each position
#      if the games played for the player are greater than or equal to the max games
#        set the appropriate column value to 'X'
#    create a new list with CCYY, player's RW_ID, first name, last name, position(s)
#    append the new list to the AllPlayersPosition list
#
#  DELETE the CCYY entries in the Player_Positions_By_Elig table, if they exist
#  CREATE the Player_Positions_By_Elig table if it doesn't exist
#  INSERT the AllPlayersPosition list into the Player_Positions_By_Elig table
#
#  COMMIT the changes
#  close the database connection

import Standard_Declarations as SD

#  set current year for season (CCYY format)
SeasonCCYY = 2024

#  set database filename to RotoDB.db
DBName = SD.MainPathName + str(SeasonCCYY + 1) + '\\Database\\KBSS.db'
print ('DBname:', DBName)

#  initialize counts
CountOfPlayersRead     = 0
CountOfPlayersWrit     = 0
PlayerList             = []
AllPlayersPositionList = []

#  open the RotoDB connection and create a cursor for it
try:
    conn = SD.sqlite3.connect(DBName)
    curs = conn.cursor()

#  read all the player positions for that season into a list
    SQLSelect = 'SELECT * FROM Player_Positions_By_Count WHERE CCYY = ' + str(SeasonCCYY)
    print('sql:', SQLSelect)
    curs.execute(SQLSelect)
    PlayerList = curs.fetchall()
    print('players:', PlayerList)

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

    except SD.sqlite3.OperationalError:
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

except OSError as err:
    print('connection attempt failed with error:', err)
    conn.close()
    SD.sys.exit()

#  commit the import changes
conn.commit()

#  close the database connection
conn.close()