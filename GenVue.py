from Library.ReadXls import ReadXls
from Library.SqlSyntax import SqlSyntax
from Library.VueHandler import VueHandler
import os
from itertools import groupby
from collections import namedtuple
xlsObj = ReadXls(filename = 'templates/PurchaseOrder.xlsx')

def deleteFile(fileName):
    """刪除已經存在的codegen檔"""
    if os.path.exists(fileName):
        os.remove(fileName)
    else:
        print("The file does not exist")

def GenVue(boxs,templateName = "VueTemplate.mako"):
    """產生Vue檔"""
    vueObj = VueHandler(Boxs = boxs)
    vueObj.GetVueFile(templateName)
    fileName = "/home/pi/WorkSpace/TestBoostrap3/src/pages/CodeGen.vue"
    vueObj.Save(fileName)

def IterSheets(sheetNames):
    """逐個Sheet產生Vue檔內容"""
    boxs = list()
    for sheetName in sheetNames:
        #取得欄位名稱
        titles = xlsObj.fieldTitle(sheetName,1)
        print(f'資料表名稱：{sheetName}')
        print(f'欄位名稱：{titles}')
        #取得資料列內容
        Rows = xlsObj.GetRows(sheetName,titles,2)
        # Group By 列號 Field
        Rows.sort(key=lambda d : d.列號)
        mapRows = [(key, list(groups)) for key, groups in groupby(Rows, lambda d : d.列號)]
        Box = namedtuple('Box', ['BoxName', 'Datas'])
        box = Box(sheetName,mapRows)
        boxs.append(box)
        for item in mapRows:
            print(item[0])
            print(item[1])
            for gitem in item[1]:
                print(gitem.寬度)
            print('-----')
    return boxs

def GenJson(sheetNames):
    jsonStr = '{'
    for sheetName in (sheetName for sheetName in sheetNames if 'table_' not in sheetName):
        #取得欄位表頭名稱
        titles = xlsObj.fieldTitle(sheetName,1)
        #取得資料列內容
        Rows = xlsObj.GetRows(sheetName,titles,2)
        for fields in Rows:
            jsonStr += f'"{fields.欄位名稱}":"",'
            print(f'欄位名稱：{fields.欄位名稱}')
    jsonStr = jsonStr[0:len(jsonStr) - 1]
    jsonStr += '}'
    print(jsonStr)
    fileName = "/home/pi/WorkSpace/TestBoostrap3/src/data/codegen.json"
    f = open(fileName,'w')
    f.write(jsonStr)

def GenTableJson(sheetNames):
    jsonStr = '{'
    for sheetName in (sheetName for sheetName in sheetNames if 'table_' in sheetName):
        #取得欄位表頭名稱
        titles = xlsObj.fieldTitle(sheetName,1)
        #取得資料列內容
        Rows = xlsObj.GetRows(sheetName,titles,2)
        for fields in Rows:
            jsonStr += f'"{fields.欄位名稱}":"",'
            print(f'欄位名稱：{fields.欄位名稱}')
    jsonStr = jsonStr[0:len(jsonStr) - 1]
    jsonStr += '}'
    print(jsonStr)
    fileName = "/home/pi/WorkSpace/TestBoostrap3/src/data/codegentable.json"
    f = open(fileName,'w')
    f.write(jsonStr)

def prevGenVue():
    """產生Vue檔的前置處理"""
    fileName = "/home/pi/WorkSpace/TestBoostrap3/src/pages/CodeGen.vue"
    deleteFile(fileName)
    sheetNames = xlsObj.getSheetNames(NotIn = ['Index'])
    boxs = IterSheets(sheetNames)
    #產生vue檔案
    GenVue(boxs)

def Main():
    prevGenVue()
    #產生Json file
    sheetNames = xlsObj.getSheetNames(NotIn = ['Index'])
    GenJson(sheetNames)
    GenTableJson(sheetNames)

if  __name__ == '__main__':
    Main()