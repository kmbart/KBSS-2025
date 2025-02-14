#  Load_ID_Lookup - get NLH and NLP for a date and add any new players to the ID_Lookup table
#
#  set current year and week for import
#  set database filename to KBSS.db
#  set folder for season from basic path and current year
#  
#  initialize counts
#
#  open the KBSS connection
#
#  set the hitter filename
#  read in the hitter file
#  for each line in the hitter file
#    look for the hitter in the ID_Lookup table
#    if not found
#      add the hitter to the table
#
#  set the pitcher filename
#  read in the pitcher file
#  for each line in the pitcher file
#    look for the pitcher in the ID_Lookup table
#    if not found
#      add the pitcher to the table
#
#    commit the import changes
#    close the KBSS connection

import Standard_Declarations
import sys
import sqlite3
from sqlite3 import Error
import csv

#  set current year and week for import
#  set current year for season (CCYY format) and select the weeks tuple
SeasonCCYY = '2024'
SeasonWeek = '1001'

#  set database filename to KBSS.db
KBSS = 'C:\\SQLite\\RotoDB\\KBSS.db'

#  set folder for season from basic path and current year
PathRW = 'C:\\RW\\RW' + SeasonCCYY + '\\'

#  initialize counts
Cnt_Hitters_All  = 0
Cnt_Hitters_New  = 0
Cnt_Pitchers_All = 0
Cnt_Pitchers_New = 0

#  open the KBSS connection and create a cursor for it
try:
    conn = sqlite3.connect(KBSS)
    curs = conn.cursor()

except Error as err:
    print ('connection attempt failed with error:', err)
    conn.close()
    sys.exit()

#  set the hitter filename
FileName = 'NFH' + SeasonCCYY [3:4] + SeasonWeek + '.txt'
print ('H filename:', FileName)

#  read in the hitter file without the header line
try:
    with open(PathRW + FileName, 'r') as NLHFile:
        reader = csv.reader(NLHFile)

        for row in reader:
#            print ('row bef:', row)
            Cnt_Hitters_All += 1
# look for the hitter in the ID_Lookup table
            SQLSelect = 'SELECT RW_ID FROM ID_Lookup WHERE RW_ID = ' + row[2]
#            print ('SQL:', SQLSelect)
            curs.execute (SQLSelect)
#            ID_Found = str(curs.fetchone())
            ID_Found = curs.fetchone()
#            print('id found:', ID_Found)

#  if not found add the hitter to the table
            if ID_Found is None:
                Cnt_Hitters_New += 1
                fname = row[0]
                lname = row[1]
                flname = '"' + fname + ' ' + lname  + '"'
                lfname = '"' + lname + ', ' + fname + '"'
                fname = '"' + fname + '"'
                lname = '"' + lname + '"'
                rwid  = row[2]
                SQLInsert = 'INSERT INTO ID_Lookup (' + \
                            'Name_First_Last, Name_Last_First, First_Name, Last_Name, RW_ID) ' + \
                            'VALUES (' + flname + ', ' + lfname + ', ' + fname + ', ' + \
                            lname + ', ' + rwid + ')'
                print ('ins:', SQLInsert)
                curs.execute (SQLInsert)

except IOError:
    print ('Error opening file:', FileName)


#  set the pitcher filename
FileName = 'NFP' + SeasonCCYY [3:4] + SeasonWeek + '.txt'
print ('P filename:', FileName)

#  read in the pitcher file without the header line
try:
    with open(PathRW + FileName, 'r') as NLPFile:
        reader = csv.reader(NLPFile)

        for row in reader:
#            print ('row bef:', row)
            Cnt_Pitchers_All += 1
# look for the pitcher in the ID_Lookup table
            SQLSelect = 'SELECT RW_ID FROM ID_Lookup WHERE RW_ID = ' + row[2]
#            print ('SQL:', SQLSelect)
            curs.execute (SQLSelect)
#            ID_Found = str(curs.fetchone())
            ID_Found = curs.fetchone()
#            print('id found:', ID_Found)

#  if not found add the pitcher to the table
            if ID_Found is None:
                Cnt_Pitchers_New += 1
                fname = row[0]
                lname = row[1]
                flname = '"' + fname + ' ' + lname  + '"'
                lfname = '"' + lname + ', ' + fname + '"'
                fname = '"' + fname + '"'
                lname = '"' + lname + '"'
                rwid  = row[2]
                SQLInsert = 'INSERT INTO ID_Lookup (' + \
                            'Name_First_Last, Name_Last_First, First_Name, Last_Name, RW_ID) ' + \
                            'VALUES (' + flname + ', ' + lfname + ', ' + fname + ', ' + \
                            lname + ', ' + rwid + ')'
                print ('ins:', SQLInsert)
                curs.execute (SQLInsert)

#  commit the import changes
        conn.commit()

except IOError:
    print ('Error opening file:', FileName)

# close the KBSS connection
conn.close()

print()
print ('database is:', KBSS)
print ('path is:', PathRW)
print ('all hitters found: ', Cnt_Hitters_All)
print ('new hitters found: ', Cnt_Hitters_New, ' - see list above')
print ('all pitchers found:', Cnt_Pitchers_All)
print ('new pitchers found:', Cnt_Pitchers_New, ' - see list above')
