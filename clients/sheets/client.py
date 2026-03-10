import datetime

import gspread
from django.conf import settings
from google.oauth2.service_account import Credentials

from clients.sheets.dto import NewProductData


class SpreadsheetClient:
    def __init__(self):
        self.service_account_file = settings.SERVICE_ACCOUNT_FILE
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        credentials = Credentials.from_service_account_file(self.service_account_file, scopes=scopes)
        self.client = gspread.authorize(credentials)
        self._init_spreadsheets_id()

    def _init_spreadsheets_id(self):
        self.product_id = settings.SPREADSHEET_PRODUCT_ID

    def create_product_row(self, data: NewProductData):
        sheet = self.client.open_by_key(self.product_id).worksheet("Лист1")
        sheet.append_row(
            [
                f"{datetime.datetime.now()}",
                f"{data.full_name}",
                f"{data.telegram}",
                f"{data.phone}",
                f"{data.source}",
                f"{data.mri_experience} {data.mri_experience_other}",
                f"{data.specialization}",
                f"{data.mri_description_experience} {data.mri_description_experience_details}",
                f"{data.city}",
                f"{data.income_rub}",
                f"{data.difficult_sections}",
                f"{data.can_plan_mri}",
                f"{data.work_schedule}",
                f"{data.convenient_time}",
            ]
        )
