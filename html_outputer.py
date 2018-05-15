#coding=utf8
__author__ = 'zyx'
import os
import xlrd
import xlwt
from xlwt import Workbook
from xlutils.copy import copy

class HtmlOutputer(object):
    global FILENAME
    FILENAME = "soufang.xls"
    # 写入EXCEL
    def output_excel(self, new_data, house_city):
        if os.path.isfile(FILENAME) is False:
            book = Workbook(encoding='utf-8')
            sheet1 = book.add_sheet('武汉藏龙岛二手房房价')
            sheet1.write(0, 0, "名称")

            sheet1.write(0, 1, "户型")
            sheet1.write(0, 2, "面积")
            sheet1.write(0, 3, "总价")
            sheet1.write(0, 4, "单价")
            sheet1.write(0, 5, "小区地址")
            sheet1.write(0, 6, "详情链接")

            # sheet1.write(1, 0, "我是第2行第一列")
            # sheet1.write(1, 1, "我是第2行第二列")

            book.save(FILENAME)

        file = xlrd.open_workbook(FILENAME, formatting_info=True)

        # 获取已有sheet的行数
        nrow = file.sheets()[0].nrows
        # if nrow != 0:
        #     nrow = nrow+1
        # 复制原有sheet
        copy_file=copy(file)
        sheet=copy_file.get_sheet(0)
        # 插入数据
        for row, item in enumerate(new_data):
            sheet.write((row+nrow), 4, house_city)
            for i, value in enumerate(item.values()):
                sheet.write((row+nrow), i, value)
        copy_file.save(FILENAME)

