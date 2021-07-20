from googleapiclient.discovery import build
from google.oauth2 import service_account
import sys
import os
import json

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def initialise_sheets():
    if 'COVID_DASHBOARD_GOOGLE_SERVICE_ACCOUNT_TOKEN' not in os.environ:
        print(
            "The google service account token should be set in the 'COVID_DASHBOARD_GOOGLE_SERVICE_ACCOUNT_TOKEN' environment variable",
            file=sys.stderr)
        sys.exit(1)
    raw_token_str = os.environ['COVID_DASHBOARD_GOOGLE_SERVICE_ACCOUNT_TOKEN']
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(raw_token_str), scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    sheets = service.spreadsheets()
    return sheets


sheets = initialise_sheets()
