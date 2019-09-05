from mako.template import Template
from mako.lookup import TemplateLookup

class VueHandler:

    def __init__(self,templateDir = 'templates',Boxs=""):
        """設定template的目錄"""
        self.Boxs = Boxs
        self.mylookup = TemplateLookup(directories=[templateDir], input_encoding='utf-8', encoding_errors='replace')
        self.VueResult = ""

    def GetVueFile(self,tempFileName = "VueTemplate.mako",data=[]):
        """產生Vue檔案
            設定template的檔案 
           設定寫入版型的變數 
        """
        mytemplate = self.mylookup.get_template(tempFileName)
        self.VueResult = mytemplate.render(Boxs = self.Boxs)

    def Save(self,fileName = "docs/result.txt"):
        """設定存檔的檔名"""
        f= open(fileName,"a+")
        f.write(self.VueResult)
        f.close()