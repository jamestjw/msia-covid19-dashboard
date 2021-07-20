import pandas as pd
import pdb


def load_data_from_sheet(
        sheets,
        spreadsheet_id: str,
        sheet_name: str,
        start_col: str,
        end_col: str):
    '''
    Requires a google sheet service object and spreadsheet ID
    '''
    result = sheets.values().get(spreadsheetId=spreadsheet_id,
                                 range=f"{sheet_name}!{start_col}:{end_col}").execute()
    values = result.get('values', [])
    return pd.DataFrame(values[1:], columns=values[0])
