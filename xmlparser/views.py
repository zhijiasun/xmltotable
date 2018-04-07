from django.shortcuts import render
from xmltotable import settings

# Create your views here.

import xmltodict
import json
import os, shutil

fieldName = [] # the complete name of the field
fieldDBName = [] # the DB name of the field which is a shortcut of the fieldName


def parseInfoXML(infoTableName):
    global fieldName
    global fieldDBName

    fieldName = []
    fieldDBName = []
    xmlInfoFile = open(infoTableName,"r").read()
    xmlInfoContent = xmltodict.parse(xmlInfoFile)
    xmlInfoFieldList = xmlInfoContent["root"]["Configuration"]["Subsystem"]["TableList"]["table"]["structure"]["fieldList"]
    #tableFieldNumber = len(xmlInfoFieldList["field"])


    for row in xmlInfoFieldList["field"]:
        fieldName.append(row["name"])
        fieldDBName.append(row["dbName"])



table = []
tableRow = []

def parseDataXML(dataTableName):
    global table
    global tableRow

    table = []
    tableRow = []

    xmlfile = open(dataTableName,"r")
    xmlcontent= xmlfile.read()
    document = xmltodict.parse(xmlcontent)
    jsonData = document["root"]["Data"]["Subsystem"]
    #subsystemName = jsonData["name"]
    #dbName = jsonData["TableList"]["table"]["dbName"]
    recordList = jsonData["TableList"]["table"]["recordList"]
    #fieldList = recordList["record"]



    """
    print the whole table data, tableRow stores one row data
    """
   
    if (len(recordList["record"]) == 1):
        print("----------------------##############")
        print(len(recordList))
        print(recordList["record"])
        for field in recordList["record"]["field"]:
            tableRow.append(field["value"])
        table.append(tableRow)
    else:
        for row in recordList["record"]:
            print("-------------")
            print(row)
            for field in row["field"]:
                tableRow.append(field["value"])

            table.append(tableRow)
            tableRow = []
    

    print(table)


tableNameList = []

"""
traverse all the files under the path.
find the info file name, data file name and table name.
"""
def traverseFile(path):
    global tableNameList
    tableNameList = []

    for f in os.listdir(path):
        dataFile = path + "\\" + f
        if os.path.isfile(dataFile) and f.find("Data.xml") != -1:
            tableName = f[0:f.find("Data.xml")]
            #tableNameDict = {"text":tableName}
            tableNameList.append(tableName)


def index(request):
    print(settings.XML_FILE_PATH)
    traverseFile(settings.XML_FILE_PATH)
    indexXMLInfoFile = settings.XML_FILE_PATH + "\\" + "AppliqueRelay" + "Info.xml"
    indexXMLDataFile = settings.XML_FILE_PATH + "\\" + "AppliqueRelay" + "Data.xml"
    parseInfoXML(indexXMLInfoFile)
    parseDataXML(indexXMLDataFile)

    print(tableNameList)
   
    context = {"content":"hello world","tableField":fieldName,"tableData":table,"tableNameList":tableNameList}
    return render(request,'xmlparser/index.html',context)


def showtable(request,tableName):
    print(tableName)
    infoFile = settings.XML_FILE_PATH + "\\" + tableName + "Info.xml"
    dataFile = settings.XML_FILE_PATH + "\\" + tableName + "Data.xml"
    traverseFile(settings.XML_FILE_PATH)
    parseInfoXML(infoFile)
    parseDataXML(dataFile)
    context = {"content":"hello world","tableField":fieldName,"tableData":table,"tableNameList":tableNameList}
    return render(request,'xmlparser/index.html',context)