from .models import *
import xlsxwriter as xw
from django.conf import settings
import os


class ReportExcelConfig:

    def __init__(self, request):
        self.request = request
        self.file_name = self.request.user.username
        self.report_folder_path = os.path.join(settings.MEDIA_ROOT, "Reports")

    @property
    def full_path(self):
        return os.path.join(self.report_folder_path, f"{self.file_name}.xlsx")


class ExcelReport(ReportExcelConfig):

    def __init__(self, request):
        super().__init__(request)
        self.workbook = xw.Workbook(self.full_path)
        self.worksheet1 = self.workbook.add_worksheet('Reports')
        self.headers_font_bold = self.workbook.add_format({'bold': 1})
        self.headers_font_bold.set_bg_color('#CAE3FB')
        self.headers_task_details_font = self.workbook.add_format({'bold': 1})
        self.headers_task_details_font.set_bg_color('#ff8080')
        self.row = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_file()

    def close_file(self):
        self.workbook.close()

    def write_task_headers(self):
        self.worksheet1.write(self.row, 0, 'Problem', self.headers_font_bold)
        self.worksheet1.write(self.row, 1, 'Description', self.headers_font_bold)
        self.worksheet1.write(self.row, 2, 'Date_Created', self.headers_font_bold)
        self.worksheet1.write(self.row, 3, 'Start Date', self.headers_font_bold)
        self.worksheet1.write(self.row, 4, 'Email attached file', self.headers_font_bold)
        self.move_next_row()

    def write_task_details_headers(self):
        self.worksheet1.write(self.row, 5, 'Problem', self.headers_task_details_font)
        self.worksheet1.write(self.row, 6, 'Mission', self.headers_task_details_font)
        self.worksheet1.write(self.row, 7, 'Responsibility', self.headers_task_details_font)
        self.worksheet1.write(self.row, 8, 'email', self.headers_task_details_font)
        self.worksheet1.write(self.row, 9, 'status', self.headers_task_details_font)
        self.move_next_row()

    def write_task(self, task):
        self.worksheet1.write(self.row, 0, task.problem)
        self.worksheet1.write(self.row, 1, task.description)
        self.worksheet1.write(self.row, 2, str(task.date_created))
        self.worksheet1.write(self.row, 3, str(task.start_date))
        self.worksheet1.write(self.row, 4, str(task.email_attached_file) if task.email_attached_file
                              else "No File Attached")
        self.move_next_row()
        if task.taskdetail_set.count() > 0:
            self.write_task_details(task.taskdetail_set.all())
        # if len(task.)

    def write_task_details(self, task_details):
        self.write_task_details_headers()
        for td in task_details:
            self.worksheet1.write(self.row, 5, td.problem)
            self.worksheet1.write(self.row, 6, td.mission)
            self.worksheet1.write(self.row, 7, str(td.responsibility))
            self.worksheet1.write(self.row, 8, str(td.email))
            self.worksheet1.write(self.row, 9, "Open" if td.status == 1
                                  else "Stuck" if td.status == 2
                                  else "Closed"
                                  )
            self.move_next_row()

    def move_next_row(self):
        self.row += 1


