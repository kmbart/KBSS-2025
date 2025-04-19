#  Rank_By_Position - use the Player_Pool, Player_Positions, and Projections tables
#    to rank the players
#
#  set current year for season (CCYY format)
#  set pathname for rankings
#  set database filename to KBSS.db
#  initialize counts
#  open output file for pitcher rankings
#  open the database connection
#
#  SELECT the pitchers then JOIN and ORDER them by the rankings
#  set filename for pitcher rankings
#  separate the pitchers in to Colorado, Starters, Relievers, IL based on team, status, and position
#  open file for pitcher rankings
#  write pitcher rankings
#
#  for each position
#    SELECT the hitters eligible at that position, then JOIN and ORDER them by the rankings
#
#  set filename for multi-positionals
#  open file for multi-positionals
#  SELECT the multi-positionals, then write them to a file
#
#  COMMIT the changes
#  close the database connection

import Standard_Declarations as SD

#  set current year for season (CCYY format)
SeasonCCYY = 2025
ProjectionService = 'Steamer'

#  set database filename to RotoDB.db
DBName = SD.MainPathName + str(SeasonCCYY) + '\\Database\\KBSS.db'
# print ('DB filename:', DBName)

#  initialize counts
CountOfPlayersRead = 0
CountOfPlayersWrit = 0

#  open the RotoDB connection and create a cursor for it
try:
    conn = SD.sqlite3.connect(DBName)
    curs = conn.cursor()

#  SELECT the pitchers then JOIN and ORDER them by the rankings
    SQLSelect = 'SELECT Rank, POOL.Full_Name, POOL.Team, Position, Status FROM Player_Pool_' + \
        str(SeasonCCYY) + ' as POOL JOIN Projections_' + ProjectionService + '_' + \
        str(SeasonCCYY) + '_Pitchers as PROJ ON POOL.RW_ID = PROJ.RW_ID ' + \
        'WHERE POOL.CCYY = ' + str(SeasonCCYY) + \
        ' AND (POOL.Position = "RP" OR POOL.Position = "SP")' + \
        ' ORDER BY PROJ.Rank'

#    print('sql:', SQLSelect)

    curs.execute(SQLSelect)
    PitcherList = curs.fetchall()
    PitcherListCnt = len(PitcherList)
    print('Pitchers ranked:', PitcherListCnt)
#    print('players:', PitcherList)

#  separate the pitchers in to Colorado, Starters, Relievers, IL based on team, status, and position
    COPitcherList = []
    IRPitcherList = []
    ISPitcherList = []
    REPitcherList = []
    STPitcherList = []

    for aPitcher in PitcherList:
#        print('aPit=', aPitcher)
        if aPitcher[2] == 'COL':
            COPitcherList.append(aPitcher)
        elif aPitcher[4] == 'IL':
            if aPitcher[3] == 'RP':
                IRPitcherList.append(aPitcher)
            else:
                ISPitcherList.append(aPitcher)
        elif aPitcher[3] == 'RP':
            REPitcherList.append(aPitcher)
        else:
            STPitcherList.append(aPitcher)

    COPitcherListCnt = len(COPitcherList)
    IRPitcherListCnt = len(IRPitcherList)
    ISPitcherListCnt = len(ISPitcherList)
    REPitcherListCnt = len(REPitcherList)
    STPitcherListCnt = len(STPitcherList)
#    print('CPs found=', COPitcherListCnt, ':', COPitcherList)
#    print('IRs found=', IRPitcherListCnt, ':', IRPitcherList)
#    print('ISs found=', ISPitcherListCnt, ':', ISPitcherList)
#    print('RPs found=', REPitcherListCnt, ':', REPitcherList)
#    print('SPs found=', STPitcherListCnt, ':', STPitcherList)

#  set filename for pitcher rankings
    PitcherFileName = SD.MainPathName + str(SeasonCCYY) + \
        '\\Metadata\\DSL\\Auction\\Miscellaneous\\Pitcher Rankings.txt'

#  open file for pitcher rankings
    PitcherFile = open(PitcherFileName, 'w')
#    print ('p filename:', PitcherFileName)

#  write pitcher rankings
    PitcherRows = max(STPitcherListCnt, REPitcherListCnt / 2, IRPitcherListCnt, ISPitcherListCnt, COPitcherListCnt)
    PitcherRows = int (PitcherRows + 0.5)
    print ('max pitcher rows=', PitcherRows, end="")
    if PitcherRows > 55: print ('   !!! Pitcher Page Overflow !!!')
    else: print()

    print('STARTERS'.ljust(20, ' '), 'STARTERS-IL'.ljust(20, ' '), 'RELIEVERS #1'.ljust(20, ' '),
          'RELIEVERS #2'.ljust(20, ' '), 'RELIEVERS-IL'.ljust(20, ' '), 'COLORADO'.ljust(20, ' '),
          file=PitcherFile)

    for ix in range(PitcherRows):
        sp = isp = rp = rp2 = irp = cp = ' '
        if ix < STPitcherListCnt: sp  = STPitcherList[ix][1]
        if ix < REPitcherListCnt: rp  = REPitcherList[ix][1]
        if ix < (REPitcherListCnt - PitcherRows): rp2 = REPitcherList[ix + PitcherRows][1]
        if ix < IRPitcherListCnt: irp = IRPitcherList[ix][1]
        if ix < ISPitcherListCnt: isp = ISPitcherList[ix][1]
        if ix < COPitcherListCnt: cp  = COPitcherList[ix][1]
        print(sp.ljust(20, ' '), isp.ljust(20, ' '), rp.ljust(20, ' '), rp2.ljust(20, ' '),
            irp.ljust(20, ' '), cp.ljust(20, ' '),
            file=PitcherFile)

#  set filename for hitter rankings
    HitterFileName = SD.MainPathName + str(SeasonCCYY) + \
        '\\Metadata\\DSL\\Auction\\Miscellaneous\\Hitter Rankings.txt'

#  open file for hitter rankings
    HitterFile = open(HitterFileName, 'w')
#    print ('h filename:', HitterFileName)

    HitterCnt  = 0
    HitterRows = 0
#  for each position
    for pos in SD.hitterPositions:
#        if pos != 'C': break
        colName = 'Elig_' + pos
#        print('column:', colName)

#  SELECT the hitters eligible at that position, then JOIN and ORDER them by the rankings
        if pos == 'DH':
            SQLSelect = 'SELECT DISTINCT Rank, POOL.Full_Name, "' + pos + \
                    '" FROM Player_Positions_By_Elig as POS ' + \
                    'JOIN Player_Pool_' + str(SeasonCCYY) + ' as POOL on POOL.RW_ID = POS.RW_ID ' + \
                    'JOIN Projections_' + ProjectionService + '_' + str(SeasonCCYY) + \
                    '_Hitters as PROJ ON POOL.RW_ID = PROJ.RW_ID ' + \
                    ' WHERE POS.CCYY = ' + str(SeasonCCYY - 1) + ' AND POS.' + colName + ' = "X" ' + \
                    'AND POS.Elig_C = "" AND POS.Elig_1B = "" AND POS.Elig_2B = "" AND POS.Elig_3B = "" ' + \
                    'AND POS.Elig_SS = "" AND POS.Elig_OF = "" ' + \
                    'ORDER BY PROJ.Rank'
        else:
            SQLSelect = 'SELECT DISTINCT Rank, POOL.Full_Name, "' + pos + \
                                    '" FROM Player_Positions_By_Elig as POS' + \
                    ' JOIN Player_Pool_' + str(SeasonCCYY) + \
                    ' as POOL on POOL.RW_ID = POS.RW_ID' + \
                    ' JOIN Projections_' + ProjectionService + '_' + str(SeasonCCYY) + \
                    '_Hitters as PROJ ON POOL.RW_ID = PROJ.RW_ID ' + \
                    ' WHERE POS.CCYY = ' + str(SeasonCCYY - 1) + \
                    ' AND POS.' + colName + ' = "X"' + \
                    ' ORDER BY PROJ.Rank'
#        print('sql:', SQLSelect)

        curs.execute(SQLSelect)
        PositionList = curs.fetchall()
        if pos == 'C': PositionListC = PositionList
        elif pos == '1B': PositionList1B = PositionList
        elif pos == '2B': PositionList2B = PositionList
        elif pos == '3B': PositionList3B = PositionList
        elif pos == 'SS': PositionListSS = PositionList
        elif pos == 'OF': PositionListOF = PositionList
        elif pos == 'DH': PositionListDH = PositionList

        HitterCnt = HitterCnt + len(PositionList)
#        print(pos, 'hitters ranked:', len(PositionList))
#        print ('hitters:', PositionList)

    print('Hitters ranked:', HitterCnt)

    #  write hitter rankings
    HitterRows = max(len(PositionListC), len(PositionList1B), len(PositionList2B), len(PositionList3B),
                     len(PositionListSS), len(PositionListOF), len(PositionListDH))
    HitterRows = int (HitterRows + 0.5)
    print ('max hitter rows=', HitterRows, end="")
    if HitterRows > 55: print ('   !!! Hitter Page Overflow !!!')
    else: print ()

    print('CATCHERS'.ljust(20, ' '), 'FIRSTBASEMEN'.ljust(20, ' '), 'SECONDBASEMEN'.ljust(20, ' '),
          'SHORTSTOPS'.ljust(20, ' '), 'THIRDBASEMEN'.ljust(20, ' '), 'OUTFIELDERS'.ljust(20, ' '),
          'DH-ONLY'.ljust(20, ' '),
          file=HitterFile)

    for ix in range(HitterRows):
        ca = fb = sb = tb = ss = of = dh = ' '
        if ix < len(PositionListC):  ca  = PositionListC[ix][1]
        if ix < len(PositionList1B): fb  = PositionList1B[ix][1]
        if ix < len(PositionList2B): sb  = PositionList2B[ix][1]
        if ix < len(PositionListSS): ss  = PositionListSS[ix][1]
        if ix < len(PositionList3B): tb  = PositionList3B[ix][1]
        if ix < len(PositionListOF): of = PositionListOF[ix][1]
        if ix < len(PositionListDH): dh  = PositionListDH[ix][1]
        print (ca.ljust(20,' '), fb.ljust(20,' '), sb.ljust(20, ' '), ss.ljust(20, ' '), tb.ljust(20, ' '),
               of.ljust(20, ' '), dh.ljust(20, ' '),
               file=HitterFile)

#  set filename for multi-positionals
    MultiFileName = SD.MainPathName + str(SeasonCCYY) + \
        '\\Metadata\\DSL\\Auction\\Miscellaneous\\Multi-Positionals.txt'

#  open file for multi-positionals
    MultiFile = open(MultiFileName, 'w')
#    print ('m filename:', MultiFileName)

#  SELECT the multi-positionals
    SQLSelect = 'SELECT POS.* FROM Player_Pool_' + str(SeasonCCYY) + ' as POOL ' + \
                'JOIN Player_Positions_By_Elig as POS ON POOL.RW_ID = POS.RW_ID ' + \
                'WHERE POOL.CCYY = ' + str(SeasonCCYY) + \
                ' AND POS.CCYY = ' + str(SeasonCCYY - 1)
#    print('sel:', SQLSelect)
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

except OSError as err:
    print('connection attempt failed with error:', err)
    conn.close()
    SD.sys.exit()

#  commit the import changes
conn.commit()

#  close the database connection
conn.close()

# sys.exit()