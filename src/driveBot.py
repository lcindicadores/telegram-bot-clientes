from dotenv import load_dotenv
import gspread
import os
import pandas as pd

load_dotenv()

class driveBot:
    def __init__(self):
        self.worksheet = self.open_sheet().sheet1

    def get_data(self):
        dataframe = pd.DataFrame(self.worksheet.get_all_records())
        return dataframe

    def verificar_dados(self, procurado):
        quantidade_linhas = len(self.worksheet.col_values(1)) - 1
        if(quantidade_linhas == 0): return False
        dataframe = self.get_data()
        if dataframe is False: return False
        setores = dataframe['ID'].unique()
        if procurado in setores:
            return True
        else:
            return False
        
    def inserir_dados(self, dados):
        json_resp = self.worksheet.append_row(dados)
        updated_rows = (json_resp['updates']['updatedRows'])
        if (updated_rows < 1): return False
        #table_range = (json_resp['updates']['updatedRange'])[-2:]
        #rg = f"A2:{table_range}"
        #self.worksheet.sort((1, 'asc'), range=rg)
        print("Dados inseridos com sucesso na planilha.") 
        return True      

    def open_sheet(self):            
        try:
            gc = gspread.service_account(filename="analise-dados-clientes.json")
            link_google_sheet = os.getenv("LINK_SHEET")
            sh = gc.open_by_key(link_google_sheet)
            return sh        
        except: 
            print ("Erro ao abrir a planilha.")