import pymssql
from Library.SqlSyntax import SqlSyntax
from Library.ReadDB import ReadDB
import os

def DelFile(fileName=''):            
    fileName = f"csclass/{fileName}.cs"
    if os.path.exists(fileName):
        os.remove(fileName)

def GenCSFile(name,myrows):
    sqlObj = SqlSyntax(TableName = name)
    for row in myrows:
        row['fieldType'] = "string" if (row['fieldType'] == 'varchar' or row['fieldType'] == 'nvarchar') else row['fieldType']
        row['fieldType'] = "Guid" if (row['fieldType'] == 'uniqueidentifier') else row['fieldType']
        row['fieldType'] = "bool" if (row['fieldType'] == 'bit') else row['fieldType']
        row['fieldType'] = "int64" if (row['fieldType'] == 'bigint') else row['fieldType']
    sqlObj.GetClassCS("ClassTemplate.mako", myrows)
    fileName = f"csclass/{name}.cs"
    sqlObj.Save(fileName)

def Main():
    dbObj = ReadDB()
    (tableNames,rows) = dbObj.GetTableNamesAndSchema()
    for name in tableNames:
        print(name)
        # Cs檔案存在就刪除
        DelFile(name)
        #查回只屬於這個Table的資料欄位結構
        myrows = list(filter(lambda row: row['tableName'] == name,rows))
        GenCSFile(name,myrows)

if __name__ == '__main__':
    Main()
