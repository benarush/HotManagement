from .models import *
import xlsxwriter as xw
from django.conf import settings
import os


class RepotExcelConfig:

    def __init__(self, request):
        self.request = request
        self.file_name = self.request.user.username
        self.report_folder_path = os.path.join(settings.MEDIA_ROOT, "Reports")

    @property
    def full_path(self):
        return os.path.join(self.report_folder_path, f"{self.file_name}.xlsx")


class Excel_Repot(RepotExcelConfig):

    def __init__(self, request):
        super().__init__(request)
        self.workbook = xw.Workbook(self.full_path)
        self.worksheet1 = self.workbook.add_worksheet('Reports')

    def __enter__(self, request):
        self.__init__(request)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("File closed!!")
        self.workbook.close()

    def close_file(self):
        self.workbook.close()
#
# workbook = xlsxwriter.Workbook('outline.xlsx')
#
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