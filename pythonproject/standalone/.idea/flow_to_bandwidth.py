#coding:utf-8
import xlsxwriter,xlrd,time

filename=u't33e004流量转换带宽'+'.xlsx'
workbook=xlsxwriter.Workbook(filename)
worksheet=workbook.add_worksheet()

title=[u'时刻',u'平均入流量kbps',u'平均出流量Mbps',u'最大入流量kbps',u'最大出流量Mbps']

log_file=r'C:\Users\admin\Desktop\log.txt'                   #mrtg的日志文件
data_list=open(log_file,'r').readlines()[1:600]             #取日数据
data_list.reverse()

worksheet.set_column('A:E',18)
format1=workbook.add_format({'border':1,'align':'center'})

worksheet.write_row('A1',title, format1)

i=2
for l in (line.split(' ') for line in data_list):
    l=[int(j) for j in l]
    l[0]=time.localtime(l[0]).tm_hour
    l[1]=l[1]*8/1000
    l[3]=l[3]*8/1000
    l[2]=l[2]*8/1000000
    l[4]=l[4]*8/1000000
    worksheet.write_row('A'+str(i),l, format1)
    i+=1

workbook.close()
