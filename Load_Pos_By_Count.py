#  Load_Pos_By_Count - use the DraftBuddy stats to load the position counts into a table
#    (last year's Rotowire positions will not have the AL-ers who have come over)
#
#  set current year for season (CCYY format)
#  set database filename to KBSS.db
#  initialize counts
#  open the database connection
#
#  set pathname for the positions-with-DH CSV file
#  set the Player_Positions_By_Count table name
#  set the filename for the positions-with-DH CSV file
#  read the positions-with-DH CSV file into a list
#
#  for each player in the list
#    skip the first row with the headers
#    insert the CCYY and player's placeholder RW_ID
#    update the names using UNIDECODE to remove foreign characters
#
#  DELETE the CCYY entries in the Player_Positions_By_Count table, if they exist
#  CREATE the Player_Positions_By_Count table if it doesn't exist
#  INSERT the Player_Positions_By_Count list into the Player_Positions_By_Count table
#  UPDATE the Player_Positions_By_Count table with the RW_ID
#  UPDATE the RW_ID for the players with duplicate names (Josh Bell, Will Smith, ...)
#  SELECT the Player_Positions_By_Count table rows with NULL RW_ID and show them
#  SELECT the NL_Rosters HITTERS with no Player_Positions_By_Count entry and show them
#
#  COMMIT the changes
#  close the database connection
# from unidecode import unidecode
import Standard_Declarations as SD

#  set current year for season (CCYY format)
SeasonCCYY = 2025

#  set database filename to RotoDB.db
DBName = SD.MainPathName + str(SeasonCCYY) + '\\Database\\KBSS.db'
print ('DBname:', DBName)

#  initialize counts
CountOfPlayersRead     = 0
CountOfPlayersWrit     = 0
DHList                 = []
AllDHs                 = []
# ALTeams = ['BAL','BOS','CLE','CWS','DET','HOU','KC','LAA','MIN','NYY','OAK','SEA','TB','TEX','TOR']

#  open the RotoDB connection and create a cursor for it
try:
    conn = SD.sqlite3.connect(DBName)
    curs = conn.cursor()

# set pathname for the Draft Buddy positions CSV file
    positionsFilename = SD.MainPathName + str(SeasonCCYY) \
                        + '\\Metadata\\Draft Buddy Positions - ' \
                        + str(SeasonCCYY - 1) + '.csv'
    print('positionsFilename:', positionsFilename)

    #  set the Player_Positions_By_Count table name
    TableName = 'Player_Positions_By_Count'

#  read the positions-with-DH CSV file into a list
    try:
        with open(positionsFilename, 'r') as DHFile:
            reader = SD.csv.reader(DHFile)

            CSVList = list()
            linesRead = 0
            linesWrit = 0

#  for each player in the list
            for row in reader:
                linesRead = linesRead + 1
#                print ('row:', linesRead, ' = ', row)

#  skip the first row with the headers
                if linesRead != 1:

#  insert the CCYY and player's placeholder RW_ID
                    row.insert(0, SeasonCCYY)
                    row.insert(1, '00000000')

#  update the names using UNIDECODE to remove foreign characters
                    row[2] = SD.unidecode.unidecode(row[2])
                    row[3] = SD.unidecode.unidecode(row[3])
                    row[4] = SD.unidecode.unidecode(row[4])
#                    print('row:', row)
                    CSVList.append(row)

                    linesWrit = linesWrit + 1

            print ('rows read:   ', linesRead)
            print ('rows written:', linesWrit)

    except Error as err:
            print('read on CSV failed with error:', err)
            conn.close()
            sys.exit()

#  DELETE the CCYY entries in the Player_Positions_By_Count table, if they exist
    try:
        curs.execute('DELETE FROM ' + TableName + ' WHERE CCYY = ' + str(SeasonCCYY))
        print('Deleting all entries for:', SeasonCCYY)

    except sqlite3.OperationalError:
        print('No ' + TableName + ' table, creating it')

#  CREATE the Player_Positions_By_Count table if it doesn't exist
    curs.execute('CREATE TABLE IF NOT EXISTS ' + TableName +
        '(CCYY         INTEGER,'
        'RW_ID         INTEGER,'
        'Full_Name     TEXT,'
        'First_Name    TEXT,'
        'Last_Name     TEXT,'
        'Team          TEXT,'
        'Games_C       INTEGER,'
        'Games_1B      INTEGER,'
        'Games_2B      INTEGER,'
        'Games_3B      INTEGER,'
        'Games_SS      INTEGER,'
        'Games_LF      INTEGER,'
        'Games_CF      INTEGER,'
        'Games_RF      INTEGER,'
        'Games_OF      INTEGER,'
        'Games_DH      INTEGER)')

#  INSERT the Draft Buddy positions list into the Player_Positions_By_Count table
    SQLInsert = 'INSERT INTO ' +  TableName + \
        '(CCYY, RW_ID, Full_Name, First_Name, Last_Name, Team, Games_C, Games_1B, Games_2B, Games_3B, ' + \
        'Games_SS, Games_LF, Games_CF, Games_RF, Games_OF, Games_DH) ' + \
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    print ('ins:', SQLInsert)

    curs.executemany (SQLInsert, CSVList)
    print (curs.rowcount, 'rows inserted')

#  UPDATE the Player_Positions_By_Count table with the RW_ID
    SQLUpdate = 'UPDATE ' + TableName + ' SET RW_ID = (SELECT L.RW_ID FROM ID_Lookup as L WHERE' +\
                ' upper(L.Name_First_Last) = upper(' + TableName + '.Full_Name))'
    curs.execute(SQLUpdate)
    print('upd:', SQLUpdate)
    print(curs.rowcount, 'rows updated')

#  UPDATE the RW_ID for the players with duplicate names (Matt Reynolds, Josh Bell, Will Smith, Luis Garcia)
#   !!! NONE IN 2024 !!!
#    SQLUpdate = 'UPDATE ' + TableName + ' SET RW_ID = 579039 WHERE RW_ID = 389296'  # Matt Reynolds
#    curs.execute(SQLUpdate)
#    print('upd:', SQLUpdate, 'Matt Reynolds')

#  SELECT the Player_Positions_By_Count table rows with NULL RW_ID and show them
    SQLSelect = 'SELECT CCYY, RW_ID, First_Name, Last_Name, Team FROM ' + TableName + ' WHERE RW_ID IS NULL'
    curs.execute(SQLSelect)
#    print('sel:', SQLSelect)
    print('***NAME MISMATCHES***')
    rows = curs.fetchall()
    Cnt_Mismatches = 0
    for row in rows:
        if row[4] not in SD.AL_Teams:
            print(row)
            Cnt_Mismatches =+ 1
    print(Cnt_Mismatches, 'Players with a NULL ID')

#  SELECT the NL_Rosters HITTERS with no Player_Positions_By_Count entry and show them
    SQLSelect = 'SELECT ROST.RW_ID, ROST.Full_Name FROM NL_Rosters_' + str(SeasonCCYY) \
                + ' AS ROST ' + 'LEFT JOIN ' + TableName \
                + ' AS POS ON ROST.Full_Name = POS.Full_Name ' \
                'WHERE ROST.Position = "H" AND POS.Full_Name IS NULL AND ROST.CCYY = ' \
                + str(SeasonCCYY)
    curs.execute(SQLSelect)
#    print ('sel:', SQLSelect)
    print('***MISSING HITTERS***')
    rows = curs.fetchall()
    for row in rows:
        print (row)
    print (len(rows), 'Rostered HITTERS with no position last year')

except Error as err:
    print('connection attempt failed with error:', err)
    conn.close()
    SD.sys.exit()

#  commit the import changes
conn.commit()

#  close the database connection
conn.close()