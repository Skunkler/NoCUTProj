import arcpy, os, shutil

sdeFile = r"C:\Users\kunklerw\AppData\Roaming\ESRI\Desktop10.7\ArcCatalog\sde@ops.sde\\"


readFile = open(r"D:\NoCUT\2017-1-20_No_Cut_Street_Update_1.csv", 'r')

lines = readFile.readlines()
count = 0


def checkStreetNames(inputAtt):
    StreetsDict = {'Boulevard':'Blvd', 'Road':'Rd', 'Street':'St', 'Court':'Ct', 'Circle':'Cir', 'Place':'Pl', 'Drive':'Dr',\
                   'Highway':'Hwy', 'Lane':'Ln', 'Parkway':'Pkwy', 'Dr':'Dr', 'Avenue':'Ave', 'Circus':'Circus'}

    OutTupleList = []
    for i in inputAtt:
        try:
            if len(i.split(' ')) > 4:
                OutTupleList.append((i.split(' ')[0],i.split(' ')[1], StreetsDict[i.split(' ')[-2]]))
            elif len(i.split(' '))== 4:
                OutTupleList.append((i.split(' ')[0],StreetsDict[i.split(' ')[-1]]))
            elif len(i.split(' ')) == 3:
                OutTupleList.append((i.split(' ')[0], i.split(' ')[1], StreetsDict[i.split(' ')[-1]]))
            elif len(i.split(' ')) == 2:
                OutTupleList.append((i.split(' ')[0], StreetsDict[i.split(' ')[-1]]))
        except:
            print "failed for " + i
    print OutTupleList
    


streetList=[]
for line in lines:
    if count > 0:
        #print line.split(',')[1]
        streetList.append(line.split(',')[1])
    else:
        count += 1
streetList.sort()
checkStreetNames(streetList)
#NoCutLayer = sdeFile + "LVVWDGIS.NOCUTSCL"

#arcpy.MakeFeatureLayer_management(NoCutLayer, 'NoCut')


