

First_2017_1 = open(r"D:\NoCUT\Review\2017_1_20.csv", "r")

Second_2017_10 = open(r"D:\NoCUT\Review\2017_10_18.csv", "r")

Third_2018_8 = open(r"D:\NoCUT\Review\2018_8_15.csv", "r")
Fourth_2019 = open(r"D:\NoCUT\Review\2019_7_5.csv", "r")
FirstSet = set()
SecondSet = set()
ThirdSet = set()
FourthSet = set()

lines1 = First_2017_1.readlines()
lines2 = Second_2017_10.readlines()
lines3 = Third_2018_8.readlines()
lines4 = Fourth_2019.readlines()



for line in lines1:
    FirstSet.add((line.split(',')[0],line.split(',')[1]))

for line in lines2:
    SecondSet.add((line.split(',')[0],line.split(',')[1]))

for line in lines3:
    ThirdSet.add((line.split(',')[0],line.split(',')[1]))

for line in lines4:
    FourthSet.add((line.split(',')[0],line.split(',')[1]))


for i in SecondSet:
    if i in FirstSet:
        FirstSet.discard(i)

for i in ThirdSet:
    if i in FirstSet:
        FirstSet.discard(i)

for i in ThirdSet:
    if i in SecondSet:
        SecondSet.discard(i)

for i in FourthSet:
    if i in ThirdSet:
        ThirdSet.discard(i)
        

writeFile = open(r"D:\NoCUT\Review\NoCutUpdates.txt","w")

for line in lines1:
    if (line.split(',')[0], line.split(',')[1]) in FirstSet:
        writeFile.write(line)

for line in lines2:
    if (line.split(',')[0], line.split(',')[1]) in SecondSet:
        writeFile.write(line)

for line in lines3:
    if (line.split(',')[0], line.split(',')[1]) in ThirdSet:
        writeFile.write(line)

writeFile.close()


    
writeFile.close()

First_2017_1.close()
Second_2017_10.close()
Third_2018_8.close()
