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
    foreignKeyTableDict = {}

    threads = []
   

    def parseInfoXML(self,infoTableName):
        fieldName = []
        fieldDBName = []
        xmlInfoFile = open(infoTableName,"r").read()
        xmlInfoContent = xmltodict.parse(xmlInfoFile)
        xmlInfoCOntentStructure = xmlInfoContent["root"]["Configuration"]["Subsystem"]["TableList"]["table"]["structure"]
        xmlInfoFieldList = xmlInfoCOntentStructure["fieldList"]

        if "foreignKeyList" in xmlInfoCOntentStructure.keys():
            #the value of foreignKeyTableDict maybe List or OrderDict
            #foreignKeyTableDict[os.path.basename(infoTableName)]=xmlInfoCOntentStructure["foreignKeyList"]["foreignKey"] 

            if (isinstance(xmlInfoCOntentStructure["foreignKeyList"]["foreignKey"],dict)):
                self.foreignKeyTableDict[os.path.basename(infoTableName)] = xmlInfoCOntentStructure["foreignKeyList"]["foreignKey"]
            elif (isinstance(xmlInfoCOntentStructure["foreignKeyList"]["foreignKey"],list)):
                pass
            else:
                pass
                    

        """
        parse the info file and construct the table structure
        """        
        if (isinstance(xmlInfoFieldList["field"],list)):
            #multiple columns
            for row in xmlInfoFieldList["field"]:
                if (isinstance(row,dict)):
                    fieldName.append(row["name"])
                    fieldDBName.append(row["dbName"])
                elif(isinstance(row,list)):
                    fieldName.append(row[0])
                    fieldDBName.append(row[1])
                else:
                    print("tableName is:",os.path.basename(infoTableName),type(row),xmlInfoFieldList["field"])
        elif(isinstance(xmlInfoFieldList["field"],dict)):
            #only one column
            fieldName.append(xmlInfoFieldList["field"]["name"])
            fieldDBName.append(xmlInfoFieldList["field"]["dbName"])       
                              
            
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
        case 1. mutltiple rows and multiple columns
        case 2. only one row but multiple columns
        case 3. multiple rows but only one columns
        """
        if (isinstance(recordList,dict)):
            if (isinstance(recordList["record"],list)):
                #multiple rows in this table
                for row in recordList["record"]:
                    if (isinstance(row["field"],list)):
                        # case 1. multiple columns 
                        for field in row["field"]:
                            tableRow.append(field["value"])
                    elif(isinstance(row["field"],dict)):
                        # case 3. only one columns
                        tableRow.append(row["field"]["value"])
                    else:
                        #exception
                        print("tableName is:"+os.path.basename(dataTableName),row["field"])
                   
                    table.append(tableRow)
                    tableRow = []
            elif (isinstance(recordList["record"],dict)):
                #case 2. only one row in this table
                for field in recordList["record"]["field"]:
                    tableRow.append(field["value"])
                table.append(tableRow)
            else:
                print("tableName is:"+dataTableName,type(recordList["record"]))
        else:
            print("tableName is:"+os.path.basename(dataTableName)+" has no record.")

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


    