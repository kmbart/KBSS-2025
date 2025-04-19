#  Load_Steamer - get Steamer Projections for Hitters and Pitchers

#  set the SeasonCCYY
#  set the database name
#  set the path for the projections file
#  set the projections source name

#  try to open the database connection and create a cursor for it

#  HITTER TABLE
#  set the projections hitter table name
#  DROP the projections hitter table name if it exists
#  CREATE the projections hitter table name with fields for the season and the RW_ID
#  get the column header names and numbers as a list of tuples
#  for each column header append it to the header list
#  set the hitter filename
#  read in the hitter file without the header line
#  add the season date column and the RW_ID column values, then append the row to the list
#  update the names using UNIDECODE to remove foreign characters
#  set a parm string of '?,' ColumnCnt times for the VALUES feed
#  remove the last character, i.e. linefeed
#  INSERT the entire hitter file into the new table
#  UPDATE the projections hitter file with the RW_ID
#  SELECT the projections hitter table rows with NULL RW_ID and show them

#  PITCHER TABLE
#  set the projections pitcher table name
#  DROP the projections pitcher table name if it exists
#  CREATE the projections pitcher table name with fields for the season and the RW_ID
#  get the column header names and numbers as a list of tuples
#  for each column header append it to the header list
#  set the pitcher filename
#  read in the pitcher file without the header line
#  add the season date column and the RW_ID column values, then append the row to the list
#  update the names using UNIDECODE to remove foreign characters
#  set a parm string of '?,' ColumnCnt times for the VALUES feed
#  remove the last character, i.e. linefeed
#  INSERT the entire pitcher file into the new table
#  UPDATE the projections pitcher file with the RW_ID
#  SELECT the projections pitcher table rows with NULL RW_ID and show them

#  commit the  changes
#  close the RWDB connection

import Standard_Declarations as SD

#  set the SeasonCCYY
SeasonCCYY = '2025'

#  set the database name
DBName = SD.MainPathName + str(SeasonCCYY) + '\\Database\\KBSS.db'
print ('database is:', DBName)

#  set the path for the projections file
PathName = SD.MainPathName + str(SeasonCCYY) + '\\Database\\Projections\\'
print ('path is:', PathName)

#  set the projections source name
ProjectionsSource = 'Steamer'
print ('projections source:', ProjectionsSource)

#  try to open the database connection and create a cursor for it
try:
    conn = SD.sqlite3.connect(DBName)
    curs = conn.cursor()
    
except Error as err:
    print ('connection attempt failed with error:', err)
    conn.close()
    SD.sys.exit()

#  set the hitter filename
FileName = ProjectionsSource + '-' + str(SeasonCCYY) + '-Hitters.csv'
print('proj filename:', FileName)

#  set the hitter tablename
#  set the projections hitter table name
TableName = 'Projections_' + ProjectionsSource + '_' + str(SeasonCCYY) + '_Hitters'
print('proj tbl name:', TableName)

# SD.sys.exit()

#  DROP the projections hitter table name if it exists
curs.execute('DROP TABLE IF EXISTS ' + TableName)

#  CREATE the projections hitter table name with fields for the season and the RW_ID
curs.execute('CREATE TABLE IF NOT EXISTS ' + TableName +
             '(CCYY         INTEGER,'
             'RW_ID         INTEGER,'
             'Rank          INTEGER,'
             'Full_Name     TEXT,'
             'Team          TEXT,'
             'Games         INTEGER,'
             'PA            INTEGER,'
             'AB            INTEGER,'
             'Hits          INTEGER,'
             'Doubles       INTEGER,'
             'Triples       INTEGER,'
             'HR            INTEGER,'
             'R             INTEGER,'
             'RBI           INTEGER,'
             'BB            INTEGER,'
             'SO            INTEGER,'
             'HBP           INTEGER,'
             'SB            INTEGER,'
             'CS            INTEGER,'
             'BB_PCT        REAL,'
             'SO_PCT        REAL,'
             'ISO           REAL,'
             'BABIP         REAL,'
             'BA            REAL,'
             'OBP           REAL,'
             'SLG           REAL,'
             'OPS           REAL,'
             'WOBA          REAL,'
             'WRCPlus       INTEGER,'
             'ADP           REAL)')
#             'InterSD       REAL,'
#             'InterSK       REAL,'
#             'IntraSD       REAL)')

#  get the column header names and numbers as a list of tuples
curs.execute('PRAGMA table_info(' + TableName + ');')
ColumnNames = curs.fetchall()
print('column names:', ColumnNames)

ColumnCnt = len(ColumnNames)
print('column count:', ColumnCnt)

#  The column name tuples have the column's #, name, type, 0, None, 0
#    so the column name itself is in position 1
#  for each column header append it to the header list
ColumnNameList = list()
for hdr in ColumnNames:
    ColumnNameList.append(hdr[1])
#    print ('column name list:', ColumnNameList)

    Headers = ','.join(ColumnNameList)
#    print ('headers:', Headers)

# SD.sys.exit()

#  read in the hitter file without the header line
try:
    with open(PathName + FileName, 'r') as HitterFile:
        reader = SD.csv.reader(HitterFile)

        CSVList = list()
        linesRead = 0
        for row in reader:
            linesRead = linesRead + 1
#            print ('row:', linesRead, ' = ', row)
#  skip the first row with the headers
            if linesRead != 1:
#  add the season date column and the RW_ID column values, then append the row to the list
                row.insert(0, SeasonCCYY)
                row.insert(1, '00000000')

#  update the names using UNIDECODE to remove foreign characters
                row[3] = SD.unidecode.unidecode(row[3])
                CSVList.append(row)
#                print ('row:', row)
#                print ('csvlist:', CSVList)

        #  set a parm string of '?,' ColumnCnt times for the VALUES feed
        ParmStr = '?,' * ColumnCnt

#  remove the last character, i.e. linefeed
        ParmStr = ParmStr[:-1]
#        print ('parm str:', ParmStr)

#  INSERT the entire file into the new table
        SQLInsert = 'INSERT INTO ' + TableName + '(' + Headers + ') VALUES (' + ParmStr + ')'
        curs.executemany(SQLInsert, CSVList)

#        print the entire line
#            for line in linelist:
#                print ('line:', line.strip())

#  UPDATE the projections hitter file with the RW_ID
        SQLUpdate = 'UPDATE ' + TableName + ' SET RW_ID = (SELECT L.RW_ID FROM ID_Lookup as L ' + 'WHERE upper(L.Name_First_Last) = upper(' \
                    + TableName + '.Full_Name))'
#        print ('SQLU:', SQLUpdate)
        curs.execute(SQLUpdate)

#  SELECT the projections hitter table rows with NULL RW_ID and show them
    SQLSelect = 'SELECT CCYY, RW_ID, Full_Name, Team FROM ' + TableName + ' WHERE RW_ID IS NULL'
    print ('sel:', SQLSelect)
    curs.execute(SQLSelect)
    rows = curs.fetchall()
    print ('*** PROJECTIONS FOR HITTERS - NULLS FOUND ***')
    Cnt_Nulls = 0
    for row in rows:
        if (row[3] != '' and row[3] not in SD.AL_Teams):
            Cnt_Nulls += 1
            print (row)
    print (Cnt_Nulls, 'NULLS found')

except IOError:
    print('Error opening file:', FileName)

# SD.sys.exit()

#  PITCHER TABLE
#  set the projections filename
FileName = ProjectionsSource + '-' + str(SeasonCCYY) + '-Pitchers.csv'
print('proj filename:', FileName)

#  set the projections hitter table name
TableName = 'Projections_' + ProjectionsSource + '_' + str(SeasonCCYY) + '_Pitchers'
print('proj tbl name:', TableName)

#  DROP the projections pitcher table name if it exists
curs.execute('DROP TABLE IF EXISTS ' + TableName)

#  CREATE the projections pitcher table name with fields for the season and the RW_ID
curs.execute('CREATE TABLE IF NOT EXISTS ' + TableName +
             '(CCYY         INTEGER,'
             'RW_ID         INTEGER,'
             'Rank          INTEGER,'
             'Full_Name     TEXT,'
             'Team          TEXT,'
             'GamesStarted  INTEGER,'
             'Games         INTEGER,'
             'IP            INTEGER,'
             'Wins          INTEGER,'
             'losses        INTEGER,'
             'Qual_Starts   INTEGER,'
             'Saves         INTEGER,'
             'Holds         INTEGER,'
             'Hits          INTEGER,'
             'ER            INTEGER,'
             'HR            INTEGER,'
             'K             INTEGER,'
             'BB            INTEGER,'
             'SO_9          REAL,'
             'BB_9          REAL,'
             'SO_BB         REAL,'
             'HR_9          REAL,'
             'BA            REAL,'
             'WHIP          REAL,'
             'BABIP         REAL,'
             'LOB_PCT       REAL,'
             'ERA           REAL,'
             'FIP           REAL,'
             'ADP           REAL)')
#             'InterSD       REAL,'
#             'InterSK       REAL,'
#             'IntraSD       REAL)')

#  get the column header names and numbers as a list of tuples
curs.execute('PRAGMA table_info(' + TableName + ');')
ColumnNames = curs.fetchall()
print('column names:', ColumnNames)

ColumnCnt = len(ColumnNames)
print('column count:', ColumnCnt)

#  The column name tuples have the column's #, name, type, 0, None, 0
#    so the column name itself is in position 1
#  for each column header append it to the header list
ColumnNameList = list()
for hdr in ColumnNames:
    ColumnNameList.append(hdr[1])
#    print ('column name list:', ColumnNameList)

    Headers = ','.join(ColumnNameList)
#    print ('headers:', Headers)

#  read in the pitcher file without the header line
try:
    with open(PathName + FileName, 'r') as PitcherFile:
        reader = SD.csv.reader(PitcherFile)

        CSVList = list()
        linesRead = 0
        for row in reader:
            linesRead = linesRead + 1
#            print ('row:', linesRead, ' = ', row)
#  skip the first row with the headers
            if linesRead != 1:
#  add the season date column and the RW_ID column values, then append the row to the list
                row.insert(0, SeasonCCYY)
                row.insert(1, '00000000')

#  update the names using UNIDECODE to remove foreign characters
                row[3] = SD.unidecode.unidecode(row[3])
                CSVList.append(row)
#                print ('csvlist:', CSVList)

#  set a parm string of '?,' ColumnCnt times for the VALUES feed
        ParmStr = '?,' * ColumnCnt

#  remove the last character, i.e. linefeed
        ParmStr = ParmStr[:-1]
#        print ('parm str:', ParmStr)

#  INSERT the entire file into the new table
        SQLInsert = 'INSERT INTO ' + TableName + '(' + Headers + ') VALUES (' + ParmStr + ')'
        curs.executemany(SQLInsert, CSVList)

#  UPDATE the projections pitcher file with the RW_ID
        SQLUpdate = 'UPDATE ' + TableName + ' SET RW_ID = (SELECT L.RW_ID FROM ID_Lookup as L ' + 'WHERE upper(L.Name_First_Last) = upper(' \
                    + TableName + '.Full_Name))'
        curs.execute(SQLUpdate)

#  SELECT the projections pitcher table rows with NULL RW_ID and show them
    SQLSelect = 'SELECT CCYY, RW_ID, Full_Name, Team FROM ' + TableName + ' WHERE RW_ID IS NULL'
    print ('sel:', SQLSelect)
    curs.execute(SQLSelect)
    rows = curs.fetchall()
    print ('*** PROJECTIONS FOR PITCHERS - NULLS FOUND ***')
    Cnt_Nulls = 0
    for row in rows:
        if (row[3] != '' and row[3] not in SD.AL_Teams):
            Cnt_Nulls += 1
            print (row)
    print (Cnt_Nulls, 'NULLS found')

#        print the entire line
#            for line in linelist:
#                print ('line:', line.strip())

except IOError:
    print('Error opening file:', FileName)


#  commit the  changes
conn.commit()

#  close the RWDB connection
conn.close()

print ('END OF PROGRAM - lines read:', linesRead)
