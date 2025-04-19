#  GeneratePool - produce the Auction Day player pool from the NL Rosters left-joined to the Keepers

#  set the SeasonCCYY
#  set the database name
#  set the roster filename
#  set the player pool tablename

#  try to open the database connection and create a cursor for it

#  DROP the Pool table if it exists
#  CREATE the Pool table
#  SELECT from NL Rosters LEFT JOIN Keepers ON RW_ID where player is active/reserved/minors

#  commit the  changes
#  close the RWDB connection

import Standard_Declarations as SD

#  set the SeasonCCYY
SeasonCCYY = '2025'
AuctionDay = '0408'

#  set the database name
DBName = SD.MainPathName + str(SeasonCCYY) + '\\Database\\KBSS.db'
print ('database is:', DBName)

#  set the NL_Rosters file name
RosterFileName = 'NL_Rosters_' + SeasonCCYY
print('NL roster filename:', RosterFileName)

#  set the Player Pool table name
TableName = 'Player_Pool_' + SeasonCCYY
print('pool tbl name:', TableName)

#  try to open the database connection and create a cursor for it
try:
    conn = SD.sqlite3.connect(DBName)
    curs = conn.cursor()
    
except Error as err:
    print ('connection attempt failed with error:', err)
    conn.close()
    SD.sys.exit()

#  DROP the Pool table if it exists
curs.execute('DROP TABLE IF EXISTS ' + TableName)
print('drop tbl:', TableName)

#  CREATE the Pool table
curs.execute('CREATE TABLE IF NOT EXISTS ' + TableName +
             '(CCYY         INTEGER,'
             'RW_ID         INTEGER,'
             'Full_Name     TEXT,'
             'Team          TEXT,'
             'Position      TEXT,'
             'Status        TEXT)')
print('create tbl:', TableName)

#  SELECT from NL Rosters LEFT JOIN Keepers ON RW_ID where player is active/reserved/minors
SQLInsert = 'INSERT INTO ' + TableName + ' (CCYY, RW_ID, Full_Name, Team, Position, Status) ' + \
    'SELECT ' + SeasonCCYY + ', NL.RW_ID, NL.Full_Name, NL.Team, NL.Position, NL.Status FROM ' + \
    RosterFileName + ' as NL LEFT JOIN (SELECT * FROM Rosters_' + SeasonCCYY + \
    ' WHERE CCYYMMDD = ' +  SeasonCCYY + AuctionDay + \
    ') AS K ON NL.RW_ID = K.RW_ID WHERE K.RW_ID is NULL'
#    'SELECT ' + SeasonCCYY + ', NL.RW_ID, NL.Full_Name, NL.Team, NL.Position, NL.Status FROM NL_Rosters as NL ' + \
#    'LEFT JOIN Rosters_' + SeasonCCYY + ' as K ON NL.RW_ID = K.RW_ID WHERE K.RW_ID is NULL'
print ('sql:', SQLInsert)
curs.execute(SQLInsert)

#  commit the  changes
conn.commit()

#  close the RWDB connection
conn.close()

print ('END OF PROGRAM')
