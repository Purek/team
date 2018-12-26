import xlrd
from xlutils.copy import copy

path_excel = '..\config\c4mconfig.xlsx'
workbook = xlrd.open_workbook(path_excel)
sheet = workbook.sheet_by_index(0)
rows = sheet.nrows
print(rows)
submit={}
# for i in range(9):
i=-1
    # submit['name'] = ng.gen_one_word_digit(lowercase=False)
submit['pwd'] = sheet.cell(i+1,1).value
submit['email'] = sheet.cell(i+1,2).value
submit['email_pwd'] = sheet.cell(i+1,3).value
submit['email_assist'] = sheet.cell(i+1,4).value
submit['ua'] = sheet.cell(i+1,5).value
submit['status'] = ''
print(submit)
print('12333333')