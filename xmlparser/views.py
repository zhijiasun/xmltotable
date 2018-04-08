from django.shortcuts import render
from xmltotable import settings
from . import apps

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

    context = {"tableField":apps.XmlparserConfig.tableFieldNameDict[infoFile],
    "tableData":apps.XmlparserConfig.tableContentDict[dataFile],
    "tableNameList":apps.XmlparserConfig.tableNameList}
    
    return render(request,'xmlparser/index.html',context)