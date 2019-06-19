from openpyxl import load_workbook

class ReadXls:
    def __init__(self,filename):
        #data_only=True代表連formula也是計算後的結果值
        self.wb = load_workbook(filename = filename,data_only=True) 

    def fieldTitle(self,sheetName,rowPoisition):
        """取得欄位名稱"""
        ws = self.wb[sheetName]
        rowObj = []
        for row in ws.iter_rows(min_row=rowPoisition, max_col=ws.max_column, max_row=rowPoisition): 
            rowObj = ([row[i].value for i in range(ws.max_column)])
        return rowObj

    def getSheetData(self,sheetName,startRow = 3):
        """取得指定資料表的內容"""
        ws = self.wb[sheetName]
        rows = []
        for row in ws.iter_rows(min_row=startRow, max_col=ws.max_column, max_row=ws.max_row): 
            if row[0].value == None:
                print('this row is None')
            else:
                rows.append([row[i] for i in range(ws.max_column)])
        return rows
        # for row in rows: 
        #     for cell in row:
        #         print(cell.value)

    def getSheetNames(self,NotIn = [] ):
        return [sheetName for sheetName in self.wb.sheetnames if sheetName not in NotIn]
