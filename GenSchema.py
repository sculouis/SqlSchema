from Library.ReadXls import ReadXls
from Library.SqlSyntax import SqlSyntax
from datetime import datetime
import os
from collections import namedtuple

xlsObj = ReadXls(filename = '/Users/louischen/Downloads/費用模組_v1.0.xlsx')

def GetRows(sheetName,titles):    
    colLen = len(titles)
    rows = xlsObj.getSheetData(sheetName,4,colLen)
    mapRows = []
    for row in rows: 
        Fields=namedtuple("Fields",titles)
        myList = [field.value for field in row]
        fields = Fields(*myList)
        mapRows.append(fields)
    return mapRows

def GenSchema(sheetName,mapRows,templateName):
    sqlObj = SqlSyntax(TableName = sheetName)
    sqlObj.GetSqlSyntax(templateName, mapRows)
    now = datetime.now()
    fileName = "docs/schema.sql"
    sqlObj.Save(fileName)

def Main():
    # Schema檔案存在就刪除
    fileName = "docs/schema.sql"
    if os.path.exists(fileName):
        os.remove(fileName)
    else:
        print("The file does not exist")
    
    sheetNames = xlsObj.getSheetNames(NotIn = ['輸出摘要','Index','AllFields','非請購','員工報支'])
    print(sheetNames)
    # 產生資料表結構Sql語法
    for sheetName in sheetNames:
        #取得資料表欄位名稱
        titles = xlsObj.fieldTitle(sheetName,3)
        # print(titles)
        #取得資料表欄位定義內
        mapRows = GetRows(sheetName,titles)
        # print(mapRows)
        #產生Sql語法
        templateName = 'SqlTemplate.mako'
        GenSchema(sheetName,mapRows,templateName)
    # 產生資料表外來鍵Sql語法
    # for sheetName in sheetNames:
    #     #取得資料表欄位名稱
    #     titles = xlsObj.fieldTitle(sheetName,3)
    #     # print(titles)
    #     #取得資料表欄位定義
    #     mapRows = GetRows(sheetName,titles)
    #     # print(mapRows)
    #     #產生Sql語法
    #     templateName = 'FKTemplate.mako'
    #     GenSchema(sheetName,mapRows,templateName)


if  __name__ == '__main__':
    Main()
