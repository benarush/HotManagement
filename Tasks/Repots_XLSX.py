from .models import *
import xlsxwriter
from django.conf import settings

class RepotExcelConfig:
    print(settings.STATIC_URL)
    pass


class Excel_Repot(RepotExcelConfig):
    pass

r = RepotExcelConfig()
#
# workbook = xlsxwriter.Workbook('outline.xlsx')
# worksheet1 = workbook.add_worksheet('Reports')
#
# tasks =
#
# # Add a general format
# bold = workbook.add_format({'bold': 1})
#
# worksheet1.write(0, 0, 'name', bold)
# worksheet1.write(0, 1, 'age', bold)
#
#
# for row, task in zip(range(1, 10), tasks):
#     for column,  task_item in zip(range(2), task.values()):
#         worksheet1.write(row, column, task_item)
#
#
#
# workbook.close()