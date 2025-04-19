#  Load_NL_Rosters - get NL Rosters from CSV file

#  set the SeasonCCYY
#  set the database name
#  set the path for the rosters file

#  try to open the database connection and create a cursor for it

#  set the rosters table name
#  DROP the rosters table name if it exists
#  CREATE the rosters table name with fields for the season and the RW_ID

#  get the column header names and numbers as a list of tuples
#  for each column header append it to the header list
#  set the rosters filename
#  read in the rosters file without the header line
#  add the season date column and the RW_ID column values, then append the row to the list
#  update the names  using UNIDECODE to remove foreign characters
#  set a parm string of '?,' ColumnCnt times for the VALUES feed
#  remove the last character, i.e. linefeed
#  INSERT the entire rosters file into the new table

#  UPDATE the rosters file with the RW_ID


#  commit the  changes
#  close the RWDB connection

import Standard_Declarations as SD

#  set the SeasonCCYY
SeasonCCYY = '2025'

#  register a dialect for the CSV reader that removes spaces
SD.csv.register_dialect ('trimmed', skipinitialspace=True)

#  set the database name
DBName = SD.MainPathName + str(SeasonCCYY) + '\\Database\\KBSS.db'
print ('database is:', DBName)

#  set the path for the Roster file
rosterFilename = SD.MainPathName + str(SeasonCCYY) + '\\Database\\Rosters\\NL Rosters-2025.csv'
print ('roster filename is:', rosterFilename)

#  try to open the database connection and create a cursor for it
try:
    conn = SD.sqlite3.connect(DBName)
    curs = conn.cursor()
    
except Error as err:
    print ('connection attempt failed with error:', err)
    conn.close()
    SD.sys.exit()

#  set the rosters table name
TableName = 'NL_Rosters_' + SeasonCCYY
print('NL rosters tbl name:', TableName)

#  DROP the rosters table name if it exists
curs.execute('DROP TABLE IF EXISTS ' + TableName)

#  CREATE the rosters table name with fields for the season and the RW_ID
curs.execute('CREATE TABLE IF NOT EXISTS ' + TableName +
             '(CCYY         INTEGER,'
             'RW_ID         INTEGER,'
             'Team          TEXT,'
             'Position      TEXT,'
             'Status        TEXT,'
             'First_Name    TEXT,'
             'Last_Name     TEXT,'
             'Full_Name     TEXT)')

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

#  read in the rosters file without the header line
try:
    with open(rosterFilename, 'r') as RosterFile:
        reader = SD.csv.reader(RosterFile)

        CSVList = list()
        linesRead = 0
        for row in reader:
#            print('row in:', row)
            linesRead = linesRead + 1
#            print ('row:', linesRead, ' = ', row)
#  skip the first row with the headers
            if linesRead != 1:
#  add the season date column and the RW_ID column values, then append the row to the list
                row.insert(0, SeasonCCYY)
                row.insert(1, '00000000')

#  update the names  using UNIDECODE to remove foreign characters
                row[5] = SD.unidecode.unidecode(row[5])
                row[6] = SD.unidecode.unidecode(row[6])
                row.insert(7, row[5] + ' ' + row[6])
#                print('row:', row)
                CSVList.append(row)

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

#  UPDATE the rosters file with the RW_ID
        SQLUpdate = 'UPDATE ' + TableName + ' SET RW_ID = (SELECT L.RW_ID FROM ID_Lookup as L ' + \
                    'WHERE upper(L.Name_First_Last) = upper(' + TableName + '.Full_Name))'
        #        print ('SQLU:', SQLUpdate)
        curs.execute(SQLUpdate)
        print('cnt=:', curs.rowcount)

#  SELECT the NL_Roster table rows with NULL RW_ID and show them
        SQLSelect = 'SELECT CCYY, RW_ID, Full_Name, Team FROM ' + TableName + ' WHERE RW_ID IS NULL'
        print('sel:', SQLSelect)
        curs.execute(SQLSelect)
        rows = curs.fetchall()
        print('*** NL_ROSTERS - NULL RW_IDs ***')
        Cnt_Nulls = 0
        for row in rows:
            if row[3] not in SD.AL_Teams:
                Cnt_Nulls += 1
                print(row)
        print(Cnt_Nulls, 'NULL RW_IDs found')

#  SELECT the players with names that appear multiple times in the RW_ID table
        SQLSelect = 'SELECT Full_Name, count(ID_Lookup.RW_ID) FROM ' + TableName + ' JOIN ID_Lookup' + \
                    ' WHERE upper(Name_First_Last) = upper(' + TableName + '.Full_Name)' + \
                    ' GROUP BY Name_First_Last' + \
                    ' HAVING count(ID_Lookup.RW_ID) > 1'
        print ('sel:', SQLSelect)
        curs.execute(SQLSelect)
#        Dups_Found = curs.fetchall()
        rows = curs.fetchall()
        print('*** NL_ROSTERS - DUPLICATE NAMES ***')
        Cnt_Dups = 0
        for row in rows:
            Cnt_Dups += 1
            print(row)
        print (Cnt_Dups, ' duplicate names found')

except IOError:
    print('Error opening file:', FileName)


#  commit the  changes
conn.commit()

#  close the RWDB connection
conn.close()

print ('END OF PROGRAM - lines read:', linesRead)
