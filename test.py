from Library.ReadXls import ReadXls
from Library.SqlSyntax import SqlSyntax
from datetime import datetime
import os

xlsObj = ReadXls(filename = '/Users/louischen/Downloads/費用模組_v1.0.xlsx')

def getRows(sheetName,titles):
    rows = xlsObj.getSheetData(sheetName,4)
    mapRows = []
    for row in rows: 
        rowmap = {}
        for index in range(len(row)):
            rowmap[titles[index]] = row[index].value
        mapRows.append(rowmap)    
    return mapRows

def genSchema(sheetName,mapRows,templateName):
    sqlObj = SqlSyntax(TableName = sheetName)
    sqlObj.GetSqlSyntax(templateName, mapRows)
    now = datetime.now()
    fileName = "docs/schema.sql"
    sqlObj.Save(fileName)

def main():
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
        #取得資料表欄位定義
        mapRows = getRows(sheetName,titles)
        # print(mapRows)
        #產生Sql語法
        templateName = 'SqlTemplate.mako'
        genSchema(sheetName,mapRows,templateName)
    
    # 產生資料表外來鍵Sql語法
    for sheetName in sheetNames:
        #取得資料表欄位名稱
        titles = xlsObj.fieldTitle(sheetName,3)
        # print(titles)
        #取得資料表欄位定義
        mapRows = getRows(sheetName,titles)
        # print(mapRows)
        #產生Sql語法
        templateName = 'FKTemplate.mako'
        genSchema(sheetName,mapRows,templateName)


if  __name__ == '__main__':
    main()
