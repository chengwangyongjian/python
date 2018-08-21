#coding:utf-8
import xlsxwriter,time,getdata,xlrd

filename=u'监控周报'+time.strftime('%Y%m%d',time.localtime(time.time()))+'.xlsx'
workbook=xlsxwriter.Workbook(filename)
worksheet=workbook.add_worksheet()
data=getdata.get_data()
title=[u'日期',u'出勤',u'值班人员',u'基础类保障',u'应用类报障',u'IDC丢包类报障',u'重启服务器次数',u'备注',u'告警邮件总数']
date_title=data.get_date()
print date_title
duty_title=[u'早班',u'中班',u'晚班']
person_title=data.get_person()
print person_title
data=data.get_data()
print data

worksheet.set_column('D:I',15)

format1=workbook.add_format({'border':1,'font_size':10,'align':'center'})
format2=workbook.add_format({'border':1,'align':'center'})
format3=workbook.add_format({'border':1,'align':'center','bg_color':'blue','bold':True})

worksheet.merge_range('A2:A4',date_title[0],format1)
worksheet.merge_range('A5:A7',date_title[1],format1)
worksheet.merge_range('A8:A10',date_title[2],format1)
worksheet.merge_range('A11:A13',date_title[3],format1)
worksheet.merge_range('A14:A16',date_title[4],format1)
worksheet.merge_range('A17:A19',date_title[5],format1)
worksheet.merge_range('A20:A22',date_title[6],format1)

worksheet.merge_range('I2:I4',' ',format1)
worksheet.merge_range('I5:I7',' ',format1)
worksheet.merge_range('I8:I10',' ',format1)
worksheet.merge_range('I11:I13',' ',format1)
worksheet.merge_range('I14:I16',' ',format1)
worksheet.merge_range('I17:I19',' ',format1)
worksheet.merge_range('I20:I22',' ',format1)

worksheet.write_row('A1',title,format3)

worksheet.write_column('B2',duty_title,format2)
worksheet.write_column('B5',duty_title,format2)
worksheet.write_column('B8',duty_title,format2)
worksheet.write_column('B11',duty_title,format2)
worksheet.write_column('B14',duty_title,format2)
worksheet.write_column('B17',duty_title,format2)
worksheet.write_column('B20',duty_title,format2)

l1=['C2','C5','C8','C11','C14','C17','C20']
for key,value in dict(zip(l1,date_title)).items():
    worksheet.write_column(key,person_title[value],format2)

i=2
for d in date_title:
    date_dict=data[d]
    user_list=person_title[d]
    if len(user_list)==0:
        continue
    elif len(user_list)==1:
        worksheet.write_row('D' + str(i), date_dict[user_list[0]], format2)
        i+=3
    elif len(user_list)==2:
        for user in user_list:
            worksheet.write_row('D'+str(i),date_dict[user],format2)
            i+=1
        i+=1
    else:
        for user in user_list:
            worksheet.write_row('D' + str(i), date_dict[user], format2)
            i += 1

workbook.close()
