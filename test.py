from Library.ReadXls import ReadXls
from Library.SqlSyntax import SqlSyntax
from datetime import datetime

xlsObj = ReadXls(filename = '/Users/louischen/Downloads/上課.xlsx')
titles = xlsObj.fieldTitle('ClassMaster',3)
print(titles)

rows = xlsObj.getSheetData('ClassMaster',4)
mapRows = []
for row in rows: 
    rowmap = {}
    for index in range(len(row)):
        rowmap[titles[index]] = row[index].value
    mapRows.append(rowmap)    
print(mapRows)
sqlObj = SqlSyntax()
sqlObj.GetSqlSyntax(data = mapRows)
now = datetime.now()
fileName = "docs/result" + now.strftime("%Y%m%d%H%M%S") + ".sql"
sqlObj.Save(fileName)