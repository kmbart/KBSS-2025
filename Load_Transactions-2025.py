#  Load_Transactions - insert a CSV transaction file into the Transactions table
#
#  set current year for season (CCYY format)
#  set database filename to KBSS.db
#  set filename for transaction file from basic path and current year
#  
#  initialize counts
#
#  Set the Transaction table name
#  Create the Transactions table if it does not exist
#  Get the column header names and numbers as a list of tuples
#
#  Open the database connection
#
#  Clear out the current year's transactions
#
#  Read in the CSV transactions file
#  Set a parm string of '?,' ColumnCnt times for the VALUES feed
#  Import the CSV transactions file
#  Commit the import changes
#  Close the database connection

import Standard_Declarations as SD

#  register a dialect for the CSV reader that removes spaces
SD.csv.register_dialect ('trimmed', skipinitialspace=True)

#  set current year for season (CCYY format)
SeasonCCYY = 2024

#  set database filename to RotoDB.db
DBName = SD.MainPathName + str(SeasonCCYY + 1) + '\\Database\\KBSS.db'
print ('database is:', DBName)

#  set folder for season from basic path and current year
FileName = SD.MainPathName + str(SeasonCCYY + 1) + \
           '\\Metadata\\DSLT - 2024.csv'
print ('filename is:', FileName)

#  initialize counts
CountOfTransactions = 0

# Open the RotoDB connection and create a cursor for it
try:
    conn = SD.sqlite3.connect(DBName)
    curs = conn.cursor()

#  Set the Transaction table name
    TableName = 'Transactions'

#  Create the Transactions table if it does not exist
#  !!!  curs.execute('DROP TABLE IF EXISTS ' + TableName)
    curs.execute('CREATE TABLE IF NOT EXISTS ' + TableName +
                 '(CCYYMMDD     INTEGER,'
                 'Player        TEXT,'
                 'TransType     TEXT,'
                 'OldTeam       TEXT,'
                 'NewTeam       TEXT,'
                 'Amount        FLOAT)')

#  Get the column header names and numbers as a list of tuples
    curs.execute('PRAGMA table_info(' + TableName + ');')
    ColumnNames = curs.fetchall()
    print (TableName, ' column names:', ColumnNames)

    ColumnCnt = len(ColumnNames)
    print ('column count:', ColumnCnt)

    ColumnNameList = list()
#  The column name tuples have the column's #, name, type, 0, None, 0
#    so the column name itself is in index position 1
    for hdr in ColumnNames:
        ColumnNameList.append(hdr[1])
    print ('column name list:', ColumnNameList)
        
    Headers = ','.join(ColumnNameList)
    print ('headers:', Headers)

#  Clear out the current year's transactions
    SQLDelete = 'DELETE FROM ' + TableName + ' WHERE CCYYMMDD > ' + str(SeasonCCYY - 1) + \
        '1010' ' AND  CCYYMMDD < ' + str(SeasonCCYY) + '9999'
    print('SQL:', SQLDelete)

#  Execute the DELETE statement
    curs.execute(SQLDelete)

    #  Read in the CSV transactions file
    try:
        with open(FileName, 'r') as TransFile:
            reader = SD.csv.reader(TransFile, 'trimmed')

            TransList = list()
            for row in reader:
#                print ('row:', row)
                if row[0] == 'Date':
                    print('skipping header')
                    continue

                if row[0] == '':
                    print('reached blanks')
                    break

                if row[4] == 'DSL':
                    print('found league note:', row[2])
                    continue

                StrippedRow = [elt.strip() for elt in row]
#                print ('StrippedRow:', StrippedRow)
                StrippedRow[0] = SD.datetime.strptime(StrippedRow[0],"%m/%d/%Y")
#                print ('CCYY-MM-DD:', StrippedRow[0])
                StrippedRow[0] = SD.datetime.strftime(StrippedRow[0],"%Y%m%d")
#                print ('CCYYMMDD:', StrippedRow[0])
                CompressedRow = [StrippedRow[0],StrippedRow[2],StrippedRow[4],StrippedRow[6],StrippedRow[8],StrippedRow[10]]
#                print ('CompressedRow:', CompressedRow)
                TransList.append(CompressedRow)

#                print ('Translist:', TransList)

#  Set a parm string of '?,' ColumnCnt times for the VALUES feed
            ParmStr = '?,' * ColumnCnt
            ParmStr = ParmStr[:-1]

#  Import the CSV transactions file
            SQLInsert = 'INSERT INTO ' + TableName + '(' + Headers + ') VALUES (' + ParmStr + ')'

#  Execute the INSERT statement
            curs.executemany(SQLInsert, TransList)

            CountOfTransactions =+ 1

#  Commit the import changes
        conn.commit()

    except IOError:
        print('Error opening file:', FileName)

except OSError as err:
    print ('connection attempt failed with error:', err)
    conn.close()
    SD.sys.exit()

SD.sys.exit()


#    close the RotoDB connection
conn.close()

print()
print ('Transactions added:', CountOfTransactions)
