from django.apps import AppConfig
import xmltodict
import json
import os, shutil
from xmltotable import settings
import threading


def parseXML(**kwargs):
    pass

    
class XmlparserConfig(AppConfig):
    name = 'xmlparser'
    tableNameList = []
    """
    tableFieldNameDict = {
        "table1":["field1","field2",...],
        "table2":["field1","field2",...],
        ...
    }
    """
    tableFieldNameDict = {}
    """
    tableFieldNameDict = {
        "table1":
        [
            ["r1_c1_data1","r1_c2_data2",...],
            ["r2_c1_data1","r2_c2_data2",...]
        ],
        "table2":
        [
            ["r1_c1_data1","r1_c2_data2",...],
            ["r2_c1_data1","r2_c2_data2",...]
        ],
        ...
    }
    """
    tableContentDict = {}

    threads = []
   

    def parseInfoXML(self,infoTableName):
        fieldName = []
        fieldDBName = []
        xmlInfoFile = open(infoTableName,"r").read()
        xmlInfoContent = xmltodict.parse(xmlInfoFile)
        xmlInfoFieldList = xmlInfoContent["root"]["Configuration"]["Subsystem"]["TableList"]["table"]["structure"]["fieldList"]


        for row in xmlInfoFieldList["field"]:
            try:
                fieldName.append(row["name"])
                fieldDBName.append(row["dbName"])
            except TypeError as identifier:
                fieldName.append(row[0])
                fieldDBName.append(row[1])              
            
        self.tableFieldNameDict[os.path.basename(infoTableName)] = fieldName



    def parseDataXML(self,dataTableName):
        table = []
        tableRow = []

        xmlfile = open(dataTableName,"r")
        xmlcontent= xmlfile.read()
        document = xmltodict.parse(xmlcontent)
        jsonData = document["root"]["Data"]["Subsystem"]
        recordList = jsonData["TableList"]["table"]["recordList"]

        """
        print the whole table data, tableRow stores one row data
        """
        try:
            if (len(recordList["record"]) == 1):
                for field in recordList["record"]["field"]:
                    tableRow.append(field["value"])
                table.append(tableRow)
            else:
                for row in recordList["record"]:
                    for field in row["field"]:
                        tableRow.append(field["value"])
                    
                    
                    table.append(tableRow)
                    tableRow = []
        except Exception:
            print("==================="+dataTableName)
            print(recordList)

        self.tableContentDict[os.path.basename(dataTableName)] = table





    def traverseFile(self,path):
        for f in os.listdir(path):
            dataFile = path + "\\" + f
            if os.path.isfile(dataFile) and f.find("Data.xml") != -1:
                tableName = f[0:f.find("Data.xml")]
                self.tableNameList.append(tableName)
                infoFile = path+"\\"+tableName + "Info.xml"
                dataFile = path+"\\"+tableName + "Data.xml"

                th = threading.Thread(target=parseXML,args=[infoFile,dataFile])
                self.threads.append(th)

                self.parseInfoXML(infoFile)
                self.parseDataXML(dataFile)


    def ready(self):
        self.traverseFile(settings.XML_FILE_PATH)


    