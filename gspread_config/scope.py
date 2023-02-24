from google.oauth2.service_account import Credentials
import gspread as gs
from gspread_dataframe import get_as_dataframe, set_with_dataframe

import pandas as pd

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'gspread_config/autenticador.json',
    scopes = scopes
)

autoriza_google = gs.authorize(credentials)


def atualiza_planilha(planilha: str, worksheet: str, dados: str) -> None:
    abre_planilha = gs.open(planilha)
    seleciona_worksheet = abre_planilha.worksheet(worksheet)
    dados_dataframe = pd.DataFrame(dados)
    
    set_with_dataframe(seleciona_worksheet, dados_dataframe)
    