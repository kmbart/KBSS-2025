#  FindMultiPos - find ALL the multi-positional players, including the keepers
#
#  set current year for season (CCYY format)
#  set pathname for rankings
#  set database filename to KBSS.db
#  initialize counts
#  open the database connection
#
#  set filename for multi-positionals
#  open file for multi-positionals
#  SELECT the multi-positionals, then write them to a file
#
#  COMMIT the changes
#  close the database connection

import Standard_Declarations as SD

#  set current date (CCYYMMDD format)
SeasonCCYY = '2025'
SeasonMMDD = '0408'

# set pathname for rankings
PathName = 'C:\\Users\\keith\\OneDrive\\Documents\\DSL History\\Auction\\Previous Years\\Auction-' + SeasonCCYY

#  set database filename to RotoDB.db
DBName = SD.MainPathName + str(SeasonCCYY) + '\\Database\\KBSS.db'
print ('DBname:', DBName)

#  initialize counts
CountOfPlayersRead     = 0
CountOfPlayersWrit     = 0

#  open the RotoDB connection and create a cursor for it
try:
    conn = SD.sqlite3.connect(DBName)
    curs = conn.cursor()

#  set filename for multi-positionals
    MultiFileName = PathName + '\\All-Multi-Positionals.txt'

#  open file for multi-positionals
    MultiFile = open(MultiFileName, 'w')
#    print ('m filename:', MultiFileName)

#  SELECT the possible players
    SQLSelect = 'SELECT POS.* FROM Rosters_2023 as KEEPS ' + \
                'JOIN Player_Positions_By_Elig as POS ON KEEPS.RW_ID = POS.RW_ID ' + \
                'WHERE KEEPS.CCYYMMDD = ' + SeasonCCYY + SeasonMMDD + \
                ' AND POS.CCYY = ' + str(int(SeasonCCYY) - 1)
    print('sel:', SQLSelect)
    curs.execute(SQLSelect)
    MultiList = curs.fetchall()
#    print('multi:', MultiList)

#  for each player in the multi list find the ones with more than one position
    MultiCnt = 0
    for mp in range(len(MultiList)):
        PosCnt = MultiList[mp].count('X')
        mpos = MultiList[mp]
#        if PosCnt == 0: print('no positions for:', mpos[2])    -- no hits on SELECT
#        print('poscnt:', PosCnt, '=', MultiList[mp])
        if mpos[10] == 'X': PosCnt -= 1
        if PosCnt > 1:
            MultiCnt += 1
            poslist = []
            if mpos[4]  == 'X': poslist.append('C')
            if mpos[5]  == 'X': poslist.append('1B')
            if mpos[6]  == 'X': poslist.append('2B')
            if mpos[8]  == 'X': poslist.append('SS')
            if mpos[7]  == 'X': poslist.append('3B')
            if mpos[9]  == 'X': poslist.append('OF')
#            print('mp:', PosCnt, '=', poslist)

#  write the multipositionals to a file
#            print((mpos[2] + ' ' + mpos[3]).ljust(25, ' '), poslist)
            print((mpos[2] + ' ' + mpos[3]).ljust(25, ' '), poslist,file=MultiFile)

    print('multipos cnt:', MultiCnt)

except Error as err:
    print('connection attempt failed with error:', err)
    conn.close()
    sys.exit()

#  commit the import changes
conn.commit()

#  close the database connection
conn.close()

# sys.exit()