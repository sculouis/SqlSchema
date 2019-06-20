import pymssql
from Library.SqlSyntax import SqlSyntax
import os

password  = "<YourStrong!Passw0rd>"
server = "127.0.0.1"
user = "SA"
dbname = "CodeGenDB"

def GetTableNames():
    with pymssql.connect(server, user, password,dbname) as conn:
        with conn.cursor(as_dict=True) as cursor:
            cursor.execute('Select * From sys.tables')
            tableNames = [row['name'] for row in cursor]
            return tableNames

def GetTableSchema():
    with pymssql.connect(server, user, password,dbname) as conn:
        with conn.cursor(as_dict=True) as cursor:
            cursor.execute('exec ERP.usp_GetTableSchemas')
            rows = [row for row in cursor]
            return rows

if __name__ == '__main__':
    rows = GetTableSchema()
    for name in GetTableNames():
        print(name)
        # Cs檔案存在就刪除
        fileName = f"csclass/{name}.cs"
        if os.path.exists(fileName):
            os.remove(fileName)
        else:
            print("The file does not exist")

        myrows = [row for row in rows if row['tableName'] == name]
        sqlObj = SqlSyntax(TableName = name)
        for row in myrows:
            row['fieldType'] = "string" if (row['fieldType'] == 'varchar' or row['fieldType'] == 'nvarchar') else row['fieldType']
            row['fieldType'] = "Guid" if (row['fieldType'] == 'uniqueidentifier') else row['fieldType']
            row['fieldType'] = "bool" if (row['fieldType'] == 'bit') else row['fieldType']
            row['fieldType'] = "int64" if (row['fieldType'] == 'bigint') else row['fieldType']
        sqlObj.GetClassCS("ClassTemplate.mako", myrows)
        fileName = f"csclass/{name}.cs"
        sqlObj.Save(fileName)