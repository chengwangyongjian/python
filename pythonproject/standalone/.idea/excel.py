#coding:utf-8
import xlsxwriter

workbook=xlsxwriter.Workbook('text.xlsx')
worksheet=workbook.add_worksheet()
title=[u'日期',u'出勤',u'值班人员',u'基础类保障',u'应用类报障',u'IDC丢包类报障',u'重启服务器次数',u'备注',u'告警邮件总数']
date_title=[u'10月30日',u'10月31日']
duty_title=[u'早班',u'中班',u'晚班']
person_title=['cheng','wang','yong']
data=[
    [10,9,0,0,' '],
    [8,6,0,1,' '],
    [9,1,0,0,' '],
    [18,9,10,2,' '],
    [19,9,0,0,' '],
]
worksheet.set_column('D:I',15)

format1=workbook.add_format({'border':1,'font_size':10,'align':'center'})
format2=workbook.add_format({'border':1,'align':'center'})
format3=workbook.add_format({'border':1,'align':'center','bg_color':'blue','bold':True})

worksheet.merge_range('A2:A4',date_title[0],format1)
worksheet.merge_range('A5:A7',date_title[1],format1)
worksheet.merge_range('I2:I4',' ',format1)
worksheet.merge_range('I5:I7',' ',format1)

worksheet.write_row('A1',title,format3)
worksheet.write_column('B2',duty_title,format2)
worksheet.write_column('B5',duty_title,format2)
worksheet.write_column('C2',person_title,format2)
worksheet.write_column('C5',person_title,format2)
worksheet.write_row('D2',data[0],format2)
worksheet.write_row('D3',data[1],format2)
worksheet.write_row('D4',data[2],format2)

workbook.close()