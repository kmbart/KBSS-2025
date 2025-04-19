#  ReformatNLH - Fix NLH<MMDD> file to put one player on each line
#  define weeks in calendar as a tuple
#  
#  initialize counts
#  
#  for each week in the tuple
#    open the NL?<mmdd> file
# REFORMATNLH - read in NLH file and reformat it: strip off header line and put one player on each line

import Standard_Declarations as SD
from Standard_Declarations import MainPathName

# define a good line as 2 (<word>,<,>) pairs, a 4-to-7 digit number and comma, a 2-to-3
#   character string and a comma, then 18 (<decimals>,<,>) pairs, then a newline
GoodLine   = SD.re.compile(r'([\w| |\'|\.|\-]+),([\w| |\'|\.|\-]+),(\d){1,7},(\w){2,3},(\d+,){18}\d+\n')

# set year parm and select the appropriate year's tuple
StatCCYY = 2025
WeekMMDD = SD.weeks[StatCCYY]
FilesOpened = 0
PreLine     = ''

#  for each week in the tuple
for CountOfFiles, Week in enumerate(WeekMMDD):

    if Week == '0000': break

#    FileName = 'C:\\RW\\RW' + str(StatCCYY) + '\\NLH' + str(StatCCYY)[3:4] + Week + '.txt'
    FileName = SD.MainPathName + str(StatCCYY) + '\\Database\\Player Stats\\NLH' \
               + str(StatCCYY)[3:4] + Week + '.txt'
    print ('filename:', FileName)

    try:
        with open(FileName) as NLHFile:
            FilesOpened += 1
            LinesRead   = 0
            
            LineList = NLHFile.readlines()

            WriteLines = []

# for each line in the file
            for CountOfLines, NextLine in enumerate(LineList):
#                print (CountOfLines, ':(', len(NextLine), ')=', NextLine)
                if CountOfLines == 0: continue    #skip the header line
#                if CountOfLines > 66: break

                LinesRead  += 1
                
# if there is nothing leftover from the previous line check this line
                if PreLine == '':
# check this line and if it is good then write it to the output list and continue
                    moGoodLine = GoodLine.match(NextLine)
                    if moGoodLine != None:
#                        print ('good line:', NextLine)
                        WriteLines.append(NextLine)
                        continue

# the line is not good as-is, so try to split it on a blank; replace blanks in the name with underscore
#                print('Pre:', PreLine, ',Next:', NextLine)
                NextLine = NextLine[0:44].replace(' ', '_') + NextLine[44:]
#                print ('replaced=', NextLine)                    
                LineTails = NextLine.split(' ')
                CountTails = len(LineTails)
#                print ('count tails:', CountTails)
#                print ('linetails:', LineTails)
                
# if the line is split then check each tail
                if CountTails > 1:
                    for ix, Tail in enumerate(LineTails):
                        TailStr = str(Tail)
# undo the replace blanks with underscore from above
                        TailStr = TailStr[0:44].replace('_', ' ') + TailStr[44:]

# append a newline to the first tail
                        if ix == 0:
                            TailStr = TailStr + '\n'

#                        print ('tail', ix, ':', TailStr)

                        if PreLine != '':
                            TailStr = PreLine + TailStr
#                            print ('pre in tail@', PreLine, '+', TailStr)
                            
# test the tail and if it is good then write it to the output list
                        moGoodLine = GoodLine.match(TailStr)
                        if moGoodLine != None:
#                            print ('good tail#', ix, TailStr)
                            WriteLines.append(TailStr)
                            PreLine  = ''
                            NextLine = ''
                            
# the tail was not good so make it the next thing to check
                        else:
                            NextLine = TailStr
#                            print ('tail hangover', NextLine)

                print('if next:', NextLine)
# if the line is null then get the next line
                if NextLine == '': continue

# if the line is abbreviated the put it in PreLine
                if len(NextLine) < 45:
                    PreLine = NextLine[0:len(NextLine) - 1] + ' '
                    continue
                    
# else concatenate PreLine with this line to make a good line
                else:                      # the line is a trailer w/o an overhang
# undo the replace blanks with underscore from above
                    NextLine = NextLine[0:44].replace('_', ' ') + NextLine[44:]
                    NextLine = PreLine + NextLine
                    print ('next:', NextLine, ',pre:', PreLine)
                    PreLine = ''
                    moGoodLine = GoodLine.match(NextLine)
                    if moGoodLine != None:
#                        print ('good trailer>', NextLine)
                        WriteLines.append(NextLine)
                        continue
         
                print ('unknown:', NextLine)
                   
#            for Liner in WriteLines:
#                print (''.join(Liner))
#            print ('lines read:', LinesRead)

        FileName = SD.MainPathName + str(StatCCYY) + '\\Database\\Player Stats\\NFH' \
                   + str(StatCCYY)[3:4] + Week + '.txt'
        print ('Created formatted file:', FileName)
        with open(FileName,'w') as OutFile:
            for Line in WriteLines:
                OutFile.write(Line)
    #            print ('writing:', Line)

    except IOError:
        print('Error opening file:', FileName)

print ('files found:', FilesOpened)
