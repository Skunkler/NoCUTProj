#This tool was written by Warren Kunkler to automate the updates to the No Cut street layer within SDE

import arcpy
from arcpy import env
from datetime import date

fcs = arcpy.ListFeatureClasses()



#get_roads class takes the cleaned up incoming data from the csv file and checks the nocut layer if the road already exists, if it does it simply updates the status, otherwise
#part or of all of the selected SCL line segments will copied into no cut
class get_roads():
    outReport = open(r'D:\NoCUT\NewTool\exceptionList.txt', 'a')
    def __init__(self):
        
        self.todaysDate = str(date.today())

    #checks for existing roadways within NoCUT layer
    def __checkNoCut(self, sclLine, NoCUT, queryPackage):
        domainDict = {"current no cut":1,"in construction":2, "advertising":3, "expired no cut":4}
        arcpy.SelectLayerByLocation_management(NoCUT, "ARE_IDENTICAL_TO", sclLine)
        dateForm = self.todaysDate.split('-')
        DATETIME = dateForm[1]+'/'+dateForm[2]+'/'+dateForm[0]
        #match, change no cut status
        if int(arcpy.GetCount_management(sclLine)[0]) == int(arcpy.GetCount_management(NoCUT)[0]) and int(arcpy.GetCount_management(NoCUT)[0]) != 0:
            arcpy.CalculateField_management(NoCUT, "WHO", "'"+ queryPackage[5] + "'", "PYTHON_9.3")
            arcpy.CalculateField_management(NoCUT, "LASTUPDT", "'" + DATETIME + "'", "PYTHON_9.3")
            try:
                
                arcpy.CalculateField_management(NoCUT, "NOCUT_STAT", domainDict[queryPackage[3]], "PYTHON_9.3")
            except:
                print "could not change Nocut status for " + NoCUT
            arcpy.CalculateField_management(NoCUT, "CMPLTDT", queryPackage[4], "PYTHON_9.3")
            
            return 1
            
                                            
        #partial match, add segment and update status
        elif int(arcpy.GetCount_management(NoCUT)[0]) != 0:
            arcpy.SelectLayerByLocation_management(sclLine, "SHARE_A_LINE_SEGMENT_WITH", NoCUT, "", "REMOVE_FROM_SELECTION")
            arcpy.SelectLayerByAttribute_management(NoCUT, "CLEAR_SELECTION")
            arcpy.CopyFeatures_management(sclLine, NoCUT)
            return 2
        #new street, copy roads from no cut and update no cut status
        else:
            arcpy.SelectLayerByAttribute_management(NoCUT, "CLEAR_SELECTION")
            arcpy.CopyFeatures_management(sclLine, NoCUT)
            return 3



    #grab the selected line segment from SCL Lines based on the relationship with the intersections, if no relationship can be established, this outputs it to a log file
    #notifies the user of roads that need to be added manually
    def queryInt(self, queryPackage):
        ws=r"D:\NoCUT\NewTool\NoCutTesting.gdb"

        env.workspace = ws
        env.overwriteOutput = True
        #establish an sde connection and point to the appropriate layers if you are doing this in Oracle
        #sdeConnect = 
        IntIntersections = "\\Int_Intersections"
        noCutLyr = "\\NOCUT_SCL"
        arcpy.MakeFeatureLayer_management(ws + noCutLyr, 'NoCut')

        arcpy.MakeFeatureLayer_management(ws + '\\SCL_LINE', 'SCL_lineLyr')

        arcpy.MakeFeatureLayer_management(ws + IntIntersections, "Int_lyr1", "(INTERSECTION_TEXT LIKE '%{}%{}%'".format(queryPackage[0].upper(), queryPackage[1].upper()) + " or INTERSECTION_TEXT LIKE '%{}%{}%') AND INTERSECTION_TEXT NOT LIKE '% INT %'".format(queryPackage[1].upper(), queryPackage[0].upper()) )

        arcpy.MakeFeatureLayer_management(ws + IntIntersections, "Int_lyr2", "(INTERSECTION_TEXT LIKE '%{}%{}%'".format(queryPackage[0].upper(), queryPackage[2].upper()) + " or INTERSECTION_TEXT LIKE '%{}%{}%') AND INTERSECTION_TEXT NOT LIKE '% INT %'".format(queryPackage[2].upper(), queryPackage[0].upper()) )

        if int(arcpy.GetCount_management("Int_lyr1")[0]) != 1:
            get_roads.outReport.write("INTERSECTION_TEXT LIKE '%{}%{}%'".format(queryPackage[0].upper(), queryPackage[1].upper()) + " or INTERSECTION_TEXT LIKE '%{}%{}%'\n".format(queryPackage[1].upper(), queryPackage[0].upper()))
        elif int(arcpy.GetCount_management("Int_lyr2")[0]) != 1:
            get_roads.outReport.write("INTERSECTION_TEXT LIKE '%{}%{}%'".format(queryPackage[0].upper(), queryPackage[2].upper()) + " or INTERSECTION_TEXT LIKE '%{}%{}%'\n".format(queryPackage[2].upper(), queryPackage[0].upper()))

        elif int(arcpy.GetCount_management("Int_lyr1")[0]) == 1 and int(arcpy.GetCount_management("Int_lyr2")[0]) == 1:
            arcpy.MakeFeatureLayer_management(ws + IntIntersections, "Int_lyr3", "((INTERSECTION_TEXT LIKE '%{}%{}%'".format(queryPackage[0].upper(), queryPackage[1].upper()) + " or INTERSECTION_TEXT LIKE '%{}%{}%') AND INTERSECTION_TEXT NOT LIKE '% INT %')".format(queryPackage[1].upper(), queryPackage[0].upper())
                                              + " or ((INTERSECTION_TEXT LIKE '%{}%{}%'".format(queryPackage[0].upper(), queryPackage[2].upper()) + " or INTERSECTION_TEXT LIKE '%{}%{}%') AND INTERSECTION_TEXT NOT LIKE '% INT %')".format(queryPackage[2].upper(), queryPackage[0].upper()))

            arcpy.PointsToLine_management("Int_lyr3", ws + '\\outputLine')
            arcpy.MinimumBoundingGeometry_management(ws + '\\outputLine', ws + '\\outputCircle', "CIRCLE")
            arcpy.MakeFeatureLayer_management(ws + '\\outputCircle', 'CirLyr')
            arcpy.SelectLayerByLocation_management("SCL_lineLyr", "HAVE_THEIR_CENTER_IN", "CirLyr")
            self.__checkNoCut("SCL_lineLyr", "NoCUT", queryPackage)#, "(INTERSECTION_TEXT LIKE '%{}%{}%'".format(queryPackage[0].upper(), queryPackage[1].upper()) #+ " or INTERSECTION_TEXT LIKE '%{}%{}%') AND INTERSECTION_TEXT NOT LIKE '% INT %'".format(queryPackage[1].upper(), queryPackage[0].upper()),
                  #"(INTERSECTION_TEXT LIKE '%{}%{}%'".format(queryPackage[0].upper(), queryPackage[2].upper()) + " or INTERSECTION_TEXT LIKE '%{}%{}%') AND INTERSECTION_TEXT NOT LIKE '% INT %'".format(queryPackage[2].upper(), queryPackage[0].upper())










#reads the input csv file, queries out the road, intersection, and status information
class ReadFile():
    getRoad_obj = get_roads()
    def __init__(self,ws):
        self.ws = ws
    #grabs the street info from the csv file and packages it as a tuple, note you must pass in a value for Name
    def __GrabStreet(self, selectStr, startStr, EndStr, status, Name):
        Complete_Date = None
        statString = ""
        if status[0].isdigit():
            Complete_Date = status
        else:
            statString = status




        querySelectStr = " ".join(selectStr.split(" ")[:-1])
        queryStartStr = " ".join(startStr.split(" ")[:-1])
        queryEndStr = " ".join(EndStr.split(" ")[:-1])

        QueryPackage = (querySelectStr, queryStartStr, queryEndStr, statString, Complete_Date, Name)

        return QueryPackage


    

    def setInput(self):
        Csv_File = open(self.ws, "r")

        lines = Csv_File.readlines()

        for line in lines:
            selectStreet = line.split(',')[0]
            startStreet = line.split(',')[1]
            endStreet = line.split(',')[2]
            status = line.split(',')[3]
            #self.__GrabStreet(selectStreet, startStreet, endStreet, status)
            ReadFile.getRoad_obj.queryInt(self.__GrabStreet(selectStreet, startStreet, endStreet, status, "KUNKLERW"))




r = ReadFile(r"D:\NoCUT\NewTool\NoCutUpdateTest.csv")
r.setInput()
