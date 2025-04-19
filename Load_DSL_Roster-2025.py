#  LoadRoster - insert a CSV roster file in the Roster table
#
#  set current year for season (CCYY format) and weeks in season (MMDD format)
#  set database filename to KBSS.db
#  set folder for season from basic path and current year
#  
#  initialize counts
#
#  create the Roster table if it does not exist
#  get the column header names and numbers as a list of tuples
#
#  for each week in the tuple
#    set the StatDate
#    open the database connection
#    set the CSV roster filename
#    read in the CSV roster file
#    set a parm string of '?,' ColumnCnt times for the VALUES feed
#    import the CSV roster file
#    commit the import changes
#    close the database connection

import Standard_Declarations as SD

#  set current year for season (CCYY format) and select the weeks tuple
SeasonCCYY = 2025
AllWeeks = SD.weeks[SeasonCCYY]

#  register a dialect for the CSV reader that removes spaces
SD.csv.register_dialect ('trimmed', skipinitialspace=True)

#  set database filename to KBSS.db
databaseFilename = SD.MainPathName + str(SeasonCCYY) + '\\Database\\KBSS.db'
# print ('DB filename:', databaseFilename)

#  set folder for season from basic path and current year
rosterPath = SD.MainPathName + str(SeasonCCYY) + '\\Database\\Rosters\\CSV Files\\'
# print ('roster pathname:', rosterPath)

#  initialize counts
CountOfFiles = 0

# SD.sys.exit()

#    open the RotoDB connection and create a cursor for it
try:
    conn = SD.sqlite3.connect(databaseFilename)
    curs = conn.cursor()

#    set the ROST<CCYYMMDD> table name and create the table
    TableName = 'Rosters_' + str(SeasonCCYY)
#    curs.execute('DROP TABLE IF EXISTS ' + TableName)
    curs.execute('CREATE TABLE IF NOT EXISTS ' + TableName +
                 '(CCYYMMDD     INTEGER,'
                 'League        TEXT,'
                 'Team          TEXT,'
                 'Status        TEXT,'
                 'Position      TEXT,'
                 'Last_Name     TEXT,'
                 'First_Name    TEXT,'
                 'RW_ID         INTEGER,'
                 'Salary        FLOAT,'
                 'Contract      TEXT)')

#    get the column header names and numbers as a list of tuples
    curs.execute('PRAGMA table_info(' + TableName + ');')
    ColumnNames = curs.fetchall()
#    print (TableName, ' column names:', ColumnNames)

    ColumnCnt = len(ColumnNames)
#    print ('column count:', ColumnCnt)

    ColumnNameList = list()
#    The column name tuples have the column's #, name, type, 0, None, 0
#      so the column name itself is in index position 1
    for hdr in ColumnNames:
        ColumnNameList.append(hdr[1])
#    print ('column name list:', ColumnNameList)
        
    Headers = ','.join(ColumnNameList)
#    print ('headers:', Headers)
    
except Error as err:
    print ('connection attempt failed with error:', err)
    conn.close()
    sys.exit()

#  for each week in the tuple
for Week in AllWeeks:

    StatDate = str(SeasonCCYY) + Week

#    set the CSV roster filename
    FileName = 'CSVP' + Week + '.txt'
    print ('filename:', FileName)

#    read in the CSV roster file
    try:
        with open(rosterPath + FileName, 'r') as CSVRFile:
            reader = SD.csv.reader(CSVRFile, 'trimmed')
            
            CSVList = list()
            for row in reader:
                strippedRow = [elt.strip() for elt in row]
#                print ('strippedRow:', strippedRow)
                CSVList.append(strippedRow)

#            print ('csvlist:', CSVList)

#    set a parm string of '?,' ColumnCnt times for the VALUES feed
            ParmStr = '?,' * ColumnCnt
            ParmStr = ParmStr[:-1]

# create the DELETE statement for the existing stats for this StatDate
            SQLDelete = 'DELETE FROM ' + TableName + ' WHERE CCYYMMDD = ' + StatDate
#            print('SQL:', SQLDelete)

# execute the DELETE statement
            curs.execute(SQLDelete)

#    import the CSV roster file
            SQLInsert = 'INSERT INTO ' + TableName + '(' + Headers + ') VALUES (' + ParmStr + ')'

# execute the INSERT statement
            curs.executemany (SQLInsert, CSVList)

#    commit the import changes
        conn.commit()
        
        CountOfFiles += 1
        
    except IOError:
        print ('Error opening file:', FileName)

#    if CountOfFiles > 0: break

#    close the RotoDB connection
conn.close()

print ('Files found:', CountOfFiles)
