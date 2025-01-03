import pandas as pd
import xlrd

workbook = xlrd.open_workbook('school_name.xls')
sheet = workbook.sheet_by_index(0)

schoolNameList = []

for row in range(sheet.nrows):
    if type(sheet.row_values(row)[0]) == float:
        schoolNameList.append(sheet.row_values(row)[1])

with open('school_name.txt', 'w') as f:
    for schoolName in schoolNameList:
        f.write(schoolName + '\n')