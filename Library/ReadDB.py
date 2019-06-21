import pymssql
import os

class ReadDB:
    def __init__(self):
        self.password  = "<YourStrong!Passw0rd>"
        self.server = "127.0.0.1"
        self.user = "SA"
        self.dbname = "CodeGenDB"

    def GetTableNamesAndSchema(self):
        with pymssql.connect(self.server, self.user, self.password,self.dbname) as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.execute('Select * From sys.tables')
                tableNames = [row['name'] for row in cursor]
                cursor.execute('exec ERP.usp_GetTableSchemas')
                rows = [row for row in cursor]
                return (tableNames,rows)