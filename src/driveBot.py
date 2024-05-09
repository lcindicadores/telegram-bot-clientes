from dotenv import load_dotenv
import gspread
import os
import json
import pandas as pd

load_dotenv()

class driveBot:
    def __init__(self):
        self.gc = gspread.service_account(filename="analise-dados-clientes.json")

    def get_data(self):
        link_google_sheet = os.getenv("LINK_SHEET")
        sh = self.gc.open_by_key(link_google_sheet)
        worksheet = sh.sheet1
        dataframe = pd.DataFrame(worksheet.get_all_records())
        return dataframe
    
    def verificar_dados(self, procurado):
        link_google_sheet = os.getenv("LINK_SHEET")
        sh = self.gc.open_by_key(link_google_sheet)
        worksheet = sh.sheet1
        quantidade_linhas = len(worksheet.col_values(1)) - 1
        if(quantidade_linhas == 0): return False
        dataframe = self.get_data()
        setores = dataframe['ID'].unique()
        if procurado in setores:
            return True
        else:
            return False
        
    def inserir_dados(self, dados):
        link_google_sheet = os.getenv("LINK_SHEET")
        sh = self.gc.open_by_key(link_google_sheet)
        worksheet = sh.sheet1
        # Adiciona os dados à próxima linha vazia na planilha
        worksheet.append_row(dados)
        quantidade_linhas = len(worksheet.col_values(1))
        rg = f"A2:H{quantidade_linhas}"
        worksheet.sort((1, 'asc'), range=rg)
        print("Dados inseridos com sucesso na planilha.") 
        return True      
