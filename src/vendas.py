from src.driveBot import driveBot 
from src.data.mensagens_vendas import MSG_FIM_TESTE0
from datetime import datetime

class vendas:
    def __init__(self):
        self.msg_fim_teste = MSG_FIM_TESTE0
        self.saudacao_periodo = self.periodo_dia()
        self.uma_vez = True

    def periodo_dia(self):
        hora_atual = datetime.now().hour
        if 6 <= hora_atual < 12:
            return "Bom dia"
        elif 12 <= hora_atual < 18:
            return "Boa tarde"
        else:
            return "Boa noite"  

    def verifica_validade_teste(self) :
        hora_atual = datetime.now().hour
        min_atual = datetime.now().minute
        hora_disparo = 8
        min_disparo = 00
        if (hora_atual == hora_disparo-1): self.uma_vez = True
        if ((self.uma_vez) & (hora_atual == hora_disparo) and (min_atual == min_disparo)):   
            self.send_msg_fim_teste()
            self.uma_vez = False
        else:
            return

    def send_msg_fim_teste(self):
        print("!!!!!!")
        return 