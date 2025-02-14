#  ReformatNLP - Fix NLP<MMDD> file to put one player on each line
#  define weeks in calendar as a tuple
#  
#  initialize counts
#  
#  for each week in the tuple
#    open the NLP<mmdd> file


from  Standard_Declarations import *
# import sys

# define a good line as 22 sets of <word>,<,> pairs, then a newline
# GoodLine   = re.compile('([\w| |\'|\.]+,){22}\d+\n')
GoodLine   = re.compile('([\w| |\'|\.|\-]+,){2}(\d){4,7},(\w){2,3},((\d+\.?\d*),){12}\d+\n')

# set year parm and select the appropriate year's tuple
StatCCYY = 2024
WeekMMDD = weeks[StatCCYY]

FilesOpened = 0
PreLine     = ''

#  for each week in the tuple
for CountOfFiles, Week in enumerate(WeekMMDD):

    FileName = 'C:\\RW\\RW' + str(StatCCYY) + '\\NLP' + str(StatCCYY)[3:4] + Week + '.txt'
#    print ('filename:', FileName)

    try:
        with open(FileName) as NLPFile:
            FilesOpened += 1
            LinesRead   = 0
            
            LineList = NLPFile.readlines()

            WriteLines = []

# for each line in the file
            for CountOfLines, NextLine in enumerate(LineList):
                if CountOfLines == 0: continue    #skip the header line
#                if CountOfLines > 66: break
#                print (CountOfLines, ':(', len(NextLine), ')=', NextLine)
                                
                LinesRead  += 1
                
# if there is nothing leftover from the previous line check this line
                if PreLine == '':
# check this line and if it is good then write it to the output list and continue
                    moGoodLine = GoodLine.match(NextLine)
                    if moGoodLine != None:
#                        print ('good line:', NextLine)
                        WriteLines.append(NextLine)
                        continue

# the line is not good as-is, so try to split it on blank; replace blanks in the name with underscore
                NextLine = NextLine[0:44].replace(' ', '_') + NextLine[44:]
#                print ('replaced=', NextLine)                    
                LineTails = NextLine.split(' ')
#                print ('linetails after split:', LineTails)
                CountTails = len(LineTails)
                if CountTails > 2:
                    CopyTails  = [LineTails[0]]
#                    print ('linetails after [0]:', LineTails)
#                    print ('copytails after [0]:', CopyTails)
                    TrailerStr = ''
                    for Trailer in LineTails[1:CountTails + 1]:
                        TrailerStr = TrailerStr + str(Trailer) + ' '
#                    print ('trailstr:', TrailerStr)
                    CopyTails.append(TrailerStr.strip(' '))
#                    print ('copytails final:', CopyTails)
                    LineTails = CopyTails
                    CountTails = len(LineTails)
#                print ('count tails:', CountTails)
#                print ('linetails final:', LineTails)
                
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
                        
# if the line is null then get the next line
                if NextLine == '': continue

# if the line is abbreviated the put it in PreLine
                if len(NextLine) < 45:
                    PreLine = NextLine[0:len(NextLine) - 1] + ' '
#                    print ('preline:', PreLine)
                    continue
                    
# else concatenate PreLine with this line to make a good line
                else:                      # the line is a trailer w/o an overhang
# undo the replace blanks with underscore from above
                    NextLine = NextLine[0:44].replace('_', ' ') + NextLine[44:]
                    NextLine = PreLine + NextLine
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

        FileName = 'C:\\RW\\RW' + str(StatCCYY) + '\\NFP' + str(StatCCYY)[3:4] + Week + '.txt'
        print ('writefile:', FileName)
        with open(FileName,'w') as OutFile:
            for Line in WriteLines:
                OutFile.write(Line)
#            print ('writing:', Line)

    except IOError:
        print ('Error opening file:', FileName)

print ('files found:', FilesOpened)
