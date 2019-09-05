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
        print(titles)
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
    GenVue(boxs)

def Main():
    # Vue檔案存在就刪除
    fileName = "/home/pi/WorkSpace/TestBoostrap3/src/pages/CodeGen.vue"
    deleteFile(fileName)
    sheetNames = xlsObj.getSheetNames(NotIn = ['Index'])
    print(sheetNames)
    IterSheets(sheetNames)

if  __name__ == '__main__':
    Main()