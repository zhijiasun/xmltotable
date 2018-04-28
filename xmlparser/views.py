from django.shortcuts import render
from xmltotable import settings
from . import apps
from django.http import HttpResponse

# Create your views here.

import xmltodict
import json
import os, shutil


def index(request):   
    context = {"tableField":apps.XmlparserConfig.tableFieldNameDict["AppliqueRelayInfo.xml"],
    "tableData":apps.XmlparserConfig.tableContentDict["AppliqueRelayData.xml"],
    "tableNameList":apps.XmlparserConfig.tableNameList}

    return render(request,'xmlparser/index.html',context)


def showtable(request,tableName):
    infoFile = tableName + "Info.xml"
    dataFile = tableName + "Data.xml"
    
    foreignKeyTable = apps.XmlparserConfig.foreignKeyTableDict
    ReferenceTableName = ""
    ReferenceFieldName = ""
    DisplayFieldName = ""
    DisplayFieldValue = ""
    isForeignKey = False

    if (len(request.GET) == 0):
        print("len is 0")
        context = {"tableField":apps.XmlparserConfig.tableFieldNameDict[infoFile],
                    "tableData":apps.XmlparserConfig.tableContentDict[dataFile],
                    "tableNameList":apps.XmlparserConfig.tableNameList}
        return render(request,'xmlparser/index.html',context)
    else:
        index = request.GET.get("index")
        value = request.GET.get("value")
        fieldName = apps.XmlparserConfig.tableFieldNameDict[infoFile][int(index)]
        

        print("tableName is:"+tableName+",index is:"+str(index)+",value is:"+value)
        print("fieldName is:"+fieldName)

        if (infoFile in foreignKeyTable.keys()):
            print("=========has foreign keys==========")
            print(foreignKeyTable[infoFile]["name"])
            print(fieldName)
            print(foreignKeyTable[infoFile])
            if (fieldName == foreignKeyTable[infoFile]["name"]):
                isForeignKey = True
                ReferenceTableName = foreignKeyTable[infoFile]["reference"]["table"]
                ReferenceFieldName = foreignKeyTable[infoFile]["reference"]["field"]
                DisplayFieldName = foreignKeyTable[infoFile]["reference"]["display"]
                print("dddddddddddddd")
                print(ReferenceTableName)
                print(ReferenceFieldName)
                print(DisplayFieldName)

                i = 0
                print(apps.XmlparserConfig.tableFieldNameDict[ReferenceTableName])
                while (i < len(apps.XmlparserConfig.tableFieldNameDict[ReferenceTableName])):
                    if (DisplayFieldName == apps.XmlparserConfig.tableFieldNameDict[ReferenceTableName][i]):
                        print("i is:"+str(i))
                        break
                    else:
                        i=i+1
                print("00000000000000000000000000000:"+str(i))
                for row in apps.XmlparserConfig.tableContentDict[ReferenceTableName.replace("Info","Data")]:
                    if (row[int(index)] == value):
                        print(row)
                        DisplayFieldValue = row[i]
                print()
                 
               
                print(DisplayFieldValue)
            else:
                isForeignKey= False
        else:
            print("tableName is:"+tableName+",has no foreignKey.")
        
        context = {
        "isForeignKey":isForeignKey,"ReferenceTable":ReferenceTableName,
        "ReferenceFieldName":ReferenceFieldName,"DisplayFieldName":DisplayFieldName,
        "DisplayFieldValue":DisplayFieldValue}
        return HttpResponse(json.dumps(context),content_type='application/json')

      
    
    
    if (infoFile in apps.XmlparserConfig.foreignKeyTableDict.keys()):
        #print(apps.XmlparserConfig.foreignKeyTableDict[infoFile])
        pass


    