# encoding=utf-8

import xlrd, xlwt
def read_excel(path):
    # data = xlrd.open_workbook("baidu/baidu-reputationinfo-NoveAndDece.xlsx")
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    rowValues= table.row_values(0)
    print rowValues
    yield rowValues
    for i in xrange(1,3):
        rowValues= table.row_values(i) #某一行数据 
        yield rowValues
        #for item in rowValues:
        #    yield item

def WriteSheetRow(sheet,rowValueList,rowIndex,isBold):
    i = 0
    style = xlwt.easyxf('font: bold 1')
    #style = xlwt.easyxf('font: bold 0, color red;')#红色字体
    #style2 = xlwt.easyxf('pattern: pattern solid, fore_colour yellow; font: bold on;') # 设置Excel单元格的背景色为黄色，字体为粗体
    for svalue in rowValueList:
        strValue = unicode(str(svalue),'utf-8')
        if isBold:
            sheet.write(rowIndex,i,strValue,style)
        else:
            sheet.write(rowIndex,i,strValue)
        i = i + 1

'''写excel文件'''
def write_excel(strFile, head, values):
    excelFile = unicode(strFile, "utf8")
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet1',cell_overwrite_ok=True)
    headList = head
    rowIndex = 0
    WriteSheetRow(sheet,headList,rowIndex,True)
    for value in values:
        rowIndex = rowIndex + 1
        valueList = value 
        WriteSheetRow(sheet,valueList,rowIndex,False)
    wbk.save(excelFile)

if __name__=="__main__":
    write_xcel("test.csv",["1","2"],[[x,x+1] for x in range(20)])
