#  LoadWklyStats - get NLH and NLP for each week and load them into the WklyStats table
#
#  set current year for season (CCYY format) and weeks in season (MMDD format)
#  set database filename to KBSS.db
#  set folder for season from basic path and current year
#  
#  initialize counts
#
#  if the WklyStats table does not exist create it
#  get the column header names and count of columns as a list of tuples
#
#  for each week in the tuple
#    set the StatDate
#    open the KBSS connection
#    set the hitter filename
#    read in the hitter file without the header line
#    set a parm string of '?,' ColumnCnt times for the VALUES feed
#    import the NLH<Y><MMDD>.txt file without the header line
#    commit the import changes
#    close the KBSS connection

from Standard_Declarations import *
# import sys
# import sqlite3
# from sqlite3 import Error
# import csv

#  set current year for season (CCYY format) and select the weeks tuple
SeasonCCYY = 2024
Weeks = weeks[SeasonCCYY]

#  set database filename to KBSS.db
KBSS = 'C:\\SQLite\\RotoDB\\KBSS.db'

#  set folder for season from basic path and current year
PathRW = 'C:\\RW\\RW' + str(SeasonCCYY) + '\\'

#  initialize counts
CountOfFiles = 0

#    open the KBSS connection and create a cursor for it
try:
    conn = sqlite3.connect(KBSS)
    curs = conn.cursor()

except Error as err:
    print ('connection attempt failed with error:', err)
    conn.close()
    sys.exit()

#  if the WklyStats table does not exist create it
#  during the season use the _CCYY version for speed, after the season run with the no suffix version just once
try:
    TableName = 'Weekly_Stats_' + str(SeasonCCYY)
#    TableName = 'Weekly_Stats'
#    print ('tablename:', TableName)

#    curs.execute('DROP TABLE IF EXISTS ' + TableName)
    curs.execute('CREATE TABLE IF NOT EXISTS ' + TableName +
                 '(CCYYMMDD     INTEGER,'
                 'First_Name    TEXT,'
                 'Last_Name     TEXT,'
                 'RW_ID         INTEGER,'
                 'Team          TEXT,'
                 'Games         INTEGER,'
                 'AB            INTEGER,'
                 'H_Runs        INTEGER,'
                 'H_Hits        INTEGER,'
                 'H_Doubles     INTEGER,'
                 'H_Triples     INTEGER,'
                 'H_HR          INTEGER,'
                 'H_RBI         INTEGER,'
                 'H_SB          INTEGER,'
                 'H_CS          INTEGER,'
                 'H_BB          INTEGER,'
                 'H_K           INTEGER,'
                 'H_E           INTEGER,'
                 'Games_At_C    INTEGER,'
                 'Games_At_1B   INTEGER,'
                 'Games_At_2B   INTEGER,'
                 'Games_At_3B   INTEGER,'
                 'Games_At_SS   INTEGER,'
                 'Games_At_OF   INTEGER,'
                 'P_Wins        INTEGER,'
                 'P_Losses      INTEGER,'
                 'P_Saves       INTEGER,'
                 'P_BlownSaves  INTEGER,'
                 'P_IP          REAL,'
                 'P_Hits        INTEGER,'
                 'P_HR          INTEGER,'
                 'P_BB          INTEGER,'
                 'P_HBP         INTEGER,'
                 'P_Runs        INTEGER,'
                 'P_ERuns       INTEGER,'
                 'P_K           INTEGER)')
#    print ('table created')
    
# get the column header names and numbers as a list of tuples
    curs.execute('PRAGMA table_info(' + TableName + ');')
    ColumnNames = curs.fetchall()
#    print ('column names:', ColumnNames)
    

# create a parm string of '?,' ColumnCnt times for the VALUES feed
    ColumnCnt = len(ColumnNames)
    ParmStr = '?,' * ColumnCnt
    ParmStr = ParmStr[:-1]
#    print ('column count:', ColumnCnt)
    
#    The column name tuples have the column's #, name, type, 0, None, 0
#      so the column name itself is in position 1
    ColumnNameList = list()
    for hdr in ColumnNames:
        ColumnNameList.append(hdr[1])
#    print ('column name list:', ColumnNameList)
        
    Headers = ','.join(ColumnNameList)
#    print ('headers:', Headers)

except Error as err:
    print ('table create or column header list failed with error:', err)
    conn.close()
    sys.exit()

# for each week in the tuple load the hitter then the pitcher stats
for Week in Weeks:

# set the StatDate
    StatDate = str(SeasonCCYY) + Week
    print ('Loading week:', StatDate)

# create the DELETE statement for the existing stats for this StatDate
    SQLDelete = 'DELETE FROM ' + TableName + ' WHERE CCYYMMDD = ' + StatDate
#    print ('SQL:', SQLDelete)

# execute the DELETE statement
    curs.execute(SQLDelete)

# commit the changes
    conn.commit()

# read in the reformatted hitter file
    FileName = 'NFH' + str(SeasonCCYY) [3:4] + Week + '.txt'
#    print ('H filename:', FileName)
    try:
        with open(PathRW + FileName, 'r') as NLHFile:
            reader = csv.reader(NLHFile)
            
            CSVList = list()
            for row in reader:
#                print ('row bef:', row)
                row.insert (0, StatDate)
                for pVal in range (12): row.append('0')
#                print ('row aft:', row)

#    import the NLH<Y><MMDD>.txt file without the header line
                SQLInsert = 'INSERT INTO ' + TableName + '(' + Headers + ') VALUES (' + ParmStr + ')'
#                print ('SQL:', SQLInsert)
                        
                curs.execute (SQLInsert, row)

#    commit the import changes
        conn.commit()
        
        CountOfFiles += 1
        
    except IOError:
        print ('Error opening file:', FileName)

# read in the reformatted pitcher file
    FileName = 'NFP' + str(SeasonCCYY) [3:4] + Week + '.txt'
#    print ('P filename:', FileName)
    try:
        with open(PathRW + FileName, 'r') as NLPFile:
            reader = csv.reader(NLPFile)
            
            CSVList = list()
            for row in reader:
#                print ('row bef:', row)
                row.insert (0, StatDate)
                for pVal in range (18): row.insert(6, '0')
#                print ('row aft:', row)

#    import the NLH<Y><MMDD>.txt file without the header line
                SQLInsert = 'INSERT INTO ' + TableName + '(' + Headers + ') VALUES (' + ParmStr + ')'
#                print ('SQL:', SQLInsert)
#                print ('row:', row)

                curs.execute (SQLInsert, row)

#    commit the import changes
        conn.commit()
        
        CountOfFiles += 1
        
    except IOError:
        print ('Error opening file:', FileName)

#    if CountOfFiles > 0: break

# close the KBSS connection
conn.close()

print()
print ('database is:', KBSS)
print ('path is:', PathRW)
print ('Files found:', CountOfFiles)
