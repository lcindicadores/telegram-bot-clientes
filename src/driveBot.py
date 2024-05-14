from dotenv import load_dotenv
import gspread
import os
import pandas as pd

load_dotenv()

NOMES_COLUNAS = ['ID', 'Origem', 'Nome', 'Sobrenome', 'Telefone', 'Estratégia Teste', 'Data Inicial Teste', 'Data Final Teste', 'Mensagem Vendas Enviado?', 'Estratégia', 'Plano', 'Preço', 'Desconto ADMIN [R$]', 'Preço Final', 'Forma Pagamento', 'Status', 'Pagamento', 'Email', 'CPF', 'Data Inicial Definitivo', 'Data Final Definitivo']

class driveBot:
    def __init__(self):
        self.worksheet = self.open_sheet().sheet1

    def get_data(self):
        dataframe = pd.DataFrame(self.worksheet.get_all_records())
        return dataframe

    def verificar_dados(self, procurado, nome_coluna):
        quantidade_linhas = self.quantidade_clientes()
        if(quantidade_linhas == 0): return False
        dataframe = self.get_data()
        if dataframe is False: return False
        setores = dataframe[nome_coluna].unique()
        if procurado in setores:
            return True
        else:
            return False
        
    def inserir_dados(self, dados):
        num_linha = self.quantidade_clientes() + 2
        json_resp = self.worksheet.insert_row(dados,num_linha)
        updated_rows = (json_resp['updates']['updatedRows'])
        if (updated_rows < 1): return False
        return True      

    def atualizar_dados(self, id_cliente, nome_coluna, dados):
        num_linha_cliente = self.get_linha_cliente(id_cliente)
        num_coluna_att = self.get_coluna_att(nome_coluna)
        letra_coluna = self.numero_para_letra(num_coluna_att)
        rg = f"{letra_coluna}{num_linha_cliente}"
        json_resp = self.worksheet.update(rg,[[dados]])
        return json_resp   
    
    def get_linha_cliente(self, id_cliente):
        coluna_id = self.worksheet.col_values(1)
        for i, id_sheets in enumerate(coluna_id):
            if str(id_cliente) == id_sheets:
                return i + 1
        return None        

    def get_coluna_att(self, nome_coluna):
        primeira_linha = self.worksheet.row_values(1)
        for i, coluna in enumerate(primeira_linha):
            if(nome_coluna == coluna):
                return i + 1
        return -1

    def numero_para_letra(self, numero_coluna):
        letra = ''
        while numero_coluna > 0:
            numero_coluna, resto = divmod(numero_coluna - 1, 26)
            letra = chr(65 + resto) + letra
        return letra                   

    def open_sheet(self):            
        try:
            gc = gspread.service_account(filename="analise-dados-clientes.json")
            link_google_sheet = os.getenv("LINK_SHEET")
            sh = gc.open_by_key(link_google_sheet)
            return sh        
        except: 
            print ("Erro ao abrir a planilha.")

    def quantidade_clientes(self):
        return len(self.worksheet.col_values(1)) - 1