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
        self.headers_font_bold = self.workbook.add_format({'bold': 1})
        self.row = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.workbook.close()

    def close_file(self):
        self.workbook.close()

    def write_task_headers(self):
        self.worksheet1.write(self.row, 0, 'Problem', self.headers_font_bold)
        self.worksheet1.write(self.row, 1, 'Description', self.headers_font_bold)
        self.worksheet1.write(self.row, 2, 'Date_Created', self.headers_font_bold)
        self.worksheet1.write(self.row, 3, 'Start Date', self.headers_font_bold)
        self.worksheet1.write(self.row, 4, 'Email attached file', self.headers_font_bold)
        self.move_next_row()

    def write_task(self, task):
        self.worksheet1.write(self.row, 0, task.problem)
        self.worksheet1.write(self.row, 1, task.description)
        self.worksheet1.write(self.row, 2, str(task.date_created))
        self.worksheet1.write(self.row, 3, str(task.start_date))
        self.worksheet1.write(self.row, 4, str(task.email_attached_file) if task.email_attached_file
                              else "No File Attached")
        self.move_next_row()
        # if len(task.)

    def move_next_row(self):
        self.row += 1

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
