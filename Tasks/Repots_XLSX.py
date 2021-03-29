import os
import re
import xlsxwriter as xw
from django.conf import settings


class ExcelReportConfig:

    def __init__(self, request):
        self.request = request
        self.file_name = self.request.user.username
        self.report_folder_path = os.path.join(settings.MEDIA_ROOT, "Reports")
        self.response_path_to_view = re.findall("(media.Reports.*)", self.full_path)[0].replace("\\", "/")

    @property
    def full_path(self):
        return os.path.join(self.report_folder_path, f"{self.file_name}.xlsx")


class ExcelReport(ExcelReportConfig):

    def __init__(self, request):
        super().__init__(request)
        self.workbook = xw.Workbook(self.full_path)
        self.reports_worksheet = self.workbook.add_worksheet('Reports')
        self.analytics_worksheet = self.workbook.add_worksheet('Analytical')
        self.headers_font_bold = self.workbook.add_format({'bold': 1})
        self.headers_font_bold.set_bg_color('#CAE3FB')
        self.headers_task_details_font = self.workbook.add_format({'bold': 1})
        self.headers_task_details_font.set_bg_color('#ff8080')
        self.report_row = 0
        self.analytic_row = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_file()

    def close_file(self):
        self.workbook.close()

    def write_task_headers(self):
        self.reports_worksheet.write(self.report_row, 0, 'Problem', self.headers_font_bold)
        self.reports_worksheet.write(self.report_row, 1, 'Description', self.headers_font_bold)
        self.reports_worksheet.write(self.report_row, 2, 'Date_Created', self.headers_font_bold)
        self.reports_worksheet.write(self.report_row, 3, 'Start Date', self.headers_font_bold)
        self.reports_worksheet.write(self.report_row, 4, 'Email attached file', self.headers_font_bold)
        self.report_move_next_row()

    def write_task_details_headers(self):
        self.reports_worksheet.write(self.report_row, 5, 'Problem', self.headers_task_details_font)
        self.reports_worksheet.write(self.report_row, 6, 'Mission', self.headers_task_details_font)
        self.reports_worksheet.write(self.report_row, 7, 'Responsibility', self.headers_task_details_font)
        self.reports_worksheet.write(self.report_row, 8, 'email', self.headers_task_details_font)
        self.reports_worksheet.write(self.report_row, 9, 'status', self.headers_task_details_font)
        self.report_move_next_row()

    def write_task(self, task):
        self.reports_worksheet.write(self.report_row, 0, task.problem)
        self.reports_worksheet.write(self.report_row, 1, task.description)
        self.reports_worksheet.write(self.report_row, 2, str(task.date_created))
        self.reports_worksheet.write(self.report_row, 3, str(task.start_date))
        self.reports_worksheet.write(self.report_row, 4, str(task.email_attached_file) if task.email_attached_file
                              else "No File Attached")
        self.report_move_next_row()
        if task.taskdetail_set.count() > 0:
            self.write_task_details(task.taskdetail_set.all())
        self.write_task_analytic(task)

    def write_analytic_headers(self):
        self.analytics_worksheet.write(self.analytic_row, 0, 'Task Problem', self.headers_font_bold)
        self.analytics_worksheet.write(self.analytic_row, 1, 'Open', self.headers_font_bold)
        self.analytics_worksheet.write(self.analytic_row, 2, 'Stuck', self.headers_font_bold)
        self.analytics_worksheet.write(self.analytic_row, 3, 'Closed', self.headers_font_bold)
        self.analytic_move_next_row()

    def write_task_details(self, task_details):
        self.write_task_details_headers()
        for td in task_details:
            self.reports_worksheet.write(self.report_row, 5, td.problem)
            self.reports_worksheet.write(self.report_row, 6, td.mission)
            self.reports_worksheet.write(self.report_row, 7, str(td.responsibility))
            self.reports_worksheet.write(self.report_row, 8, str(td.email))
            self.reports_worksheet.write(self.report_row, 9, "Open" if td.status == 1
                                  else "Stuck" if td.status == 2
                                  else "Closed"
                                  )
            self.report_move_next_row()

    def write_task_analytic(self, task):
        task_details = task.taskdetail_set.all()
        self.write_analytic_headers()
        all_task_details_count = task_details.count()
        open = len([td for td in task_details if td.status == 1])
        closed = len([td for td in task_details if td.status == 0])
        stuck = all_task_details_count - open - closed

        self.analytics_worksheet.write(self.analytic_row, 0, task.problem, self.headers_font_bold)
        self.analytics_worksheet.write(self.analytic_row, 1, open)
        self.analytics_worksheet.write(self.analytic_row, 2, stuck)
        self.analytics_worksheet.write(self.analytic_row, 3, closed)
        self.create_chart(task)
        self.analytic_move_next_task()

    def report_move_next_row(self):
        self.report_row += 1

    def analytic_move_next_row(self):
        self.analytic_row += 1

    def analytic_move_next_task(self):
        self.analytic_row += 15

    def create_chart(self, task):
        chart = self.workbook.add_chart({'type': 'pie'})
        chart.add_series({
            'name': 'tasks status pie',
            'categories': f'=Analytical!$B${self.analytic_row}:$D${self.analytic_row}',
            'values': f'=Analytical!$B${self.analytic_row+1}:$D${self.analytic_row+1}',
            'points': [
                {'fill': {'color': '#FF4500'}},
                {'fill': {'color': '#FFFF00'}},
                {'fill': {'color': '#00FF00'}},
            ],
        })
        chart.set_title({'name': f"Problem - {task.problem}"})
        self.analytics_worksheet.insert_chart(f'F{self.analytic_row}', chart, {'x_offset': 25, 'y_offset': 10})


