from dotenv import load_dotenv
from src.driveBot import driveBot
import os
import requests 
import json

load_dotenv()
SEMESTRE = 6
ANUAL = 12
class TelegramBot:
    def __init__(self):
        TOKEN = os.getenv("API_KEY")
        self.url = f"https://api.telegram.org/bot{TOKEN}/"
        self.preco_p2_m = float(os.getenv("PRECO_P2_M"))
        self.preco_p3_m = float(os.getenv("PRECO_P3_M"))
        self.preco_p1_m = self.preco_p2_m + self.preco_p3_m
        self.preco_p2_s = float(os.getenv("PRECO_P2_S"))
        self.preco_p3_s = float(os.getenv("PRECO_P3_S"))
        self.preco_p1_s = self.preco_p2_s + self.preco_p3_s
        self.preco_p2_a = float(os.getenv("PRECO_P2_A"))
        self.preco_p3_a = float(os.getenv("PRECO_P3_A"))
        self.preco_p1_a = self.preco_p2_a + self.preco_p3_a       
        self.planos = [["Indicador e Coloração - Topos e Fundos 2.0",self.preco_p1_m,self.preco_p1_s,self.preco_p1_a],["Indicador - Topos e Fundos 2.0",self.preco_p2_m,self.preco_p2_s,self.preco_p2_a],["Coloração - Topos e Fundos 2.0",self.preco_p3_m,self.preco_p3_s,self.preco_p3_a]]
        self.chat_id = None
        self.nome_plano = None
        self.tipo_plano = None

    def start_bot(self):
        update_id = None
        print("Inicializando bot...")
        while True:
            update = self.get_message(update_id)
            messages = update['result']
            if not messages: 
                print("Aguardando Clientes...")
            for message in messages:
                try:
                    update_id = message['update_id']
                    message_text = message['message']['text']
                    self.set_chat_id(message['message']['from']['id'])
                    if(message_text == "/teste"):
                        self.msg_teste(message)
                    elif(message_text == "/precos"):
                        self.send_precos()                        
                    elif(message_text == "/ativar"):
                        self.escolha_plano()
                    elif(message_text == self.planos[0][0]):  
                        self.set_nome_plano(self.planos[0][0])                      
                        self.ativacao_plano(0)
                    elif(message_text == self.planos[1][0]):  
                        self.set_nome_plano(self.planos[1][0])                      
                        self.ativacao_plano(1)
                    elif(message_text == self.planos[2][0]):  
                        self.set_nome_plano(self.planos[2][0])                      
                        self.ativacao_plano(2)                                            
                except:
                    pass    
                        
    def set_chat_id(self, chat_id):
        self.chat_id = chat_id
    def set_nome_plano(self, nome_plano):
        self.nome_plano = nome_plano
    def set_tipo_plano(self, tipo_plano):
        self.tipo_plano = tipo_plano

    def get_message(self, update_id):
        TIMEOUT = os.getenv("TIME_OUT_REQUEST")
        link_request = f"{self.url}getUpdates?timeout={TIMEOUT}"
        if update_id:
            link_request = f"{self.url}getUpdates?timeout={TIMEOUT}&offset={update_id + 1}"   
        result = requests.get(link_request)
        return json.loads(result.content)  
    
    def msg_teste(self, message):
        drive_bot = driveBot()
        if(drive_bot.verificar_dados(self.chat_id)): 
            answer_bot = "Vc já solicitou o arquivo de testes."
            self.send_answer(answer_bot) 
            return 
        dado_test = self.get_data_client_test(message)
        drive_bot.inserir_dados(dado_test)
        answer_bot = "Usuário cadastrado para testes"
        self.send_answer(answer_bot)       

    def send_precos(self):
        desc_p1_sem = ((self.preco_p1_s)/(self.preco_p1_m*SEMESTRE) - 1) * 100
        desc_p2_sem = ((self.preco_p2_s)/(self.preco_p2_m*SEMESTRE) - 1) * 100
        desc_p3_sem = ((self.preco_p3_s)/(self.preco_p3_m*SEMESTRE) - 1) * 100
        desc_p1_ano = ((self.preco_p1_a)/(self.preco_p1_m*ANUAL) - 1) * 100
        desc_p2_ano = ((self.preco_p2_a)/(self.preco_p2_m*ANUAL) - 1) * 100
        desc_p3_ano = ((self.preco_p3_a)/(self.preco_p3_m*ANUAL) - 1) * 100
        str_p1 = f"🔹 {self.planos[0][0]}: \n- Mensal:    R$ {self.planos[0][1]:.2f}\n- Semestral: R$ {self.planos[0][2]:.2f} [{desc_p1_sem:.2f}%]\n- Anual:     R$ {self.planos[0][3]:.2f} [{desc_p1_ano:.2f}%]"
        str_p2 = f"🔹 {self.planos[1][0]}: \n- Mensal:    R$ {self.planos[1][1]:.2f}\n- Semestral: R$ {self.planos[1][2]:.2f} [{desc_p2_sem:.2f}%]\n- Anual:     R$ {self.planos[1][3]:.2f} [{desc_p2_ano:.2f}%]"
        str_p3 = f"🔹 {self.planos[2][0]}: \n- Mensal:    R$ {self.planos[2][1]:.2f}\n- Semestral: R$ {self.planos[2][2]:.2f}  [{desc_p3_sem:.2f}%]\n- Anual:     R$ {self.planos[2][3]:.2f} [{desc_p3_ano:.2f}%]"
        answer_bot = f"📢 ! Ofertas Especiais ! 📢\n\n🎉 Confira nossos preços para os planos mensal, semestral e anual:\n\n{str_p1}\n\n{str_p2}\n\n{str_p3}\n\nAproveite esses preços incríveis e invista no seu trade sistem! 💰✨"
        self.send_answer(answer_bot)         

    def get_data_client_test(self, message):
        chat_id = message['message']['from']['id']
        first_name = message['message']['from']['first_name']
        last_name = message['message']['from']['last_name']
        telefone = '055'
        origem = 'Telegram'
        date = message['message']['date']
        dado = [chat_id,first_name,last_name,telefone,origem,date]   
        return dado    

    def escolha_plano(self):
        tipo_plano = {
            "keyboard": [["Indicador e Coloração - Topos e Fundos 2.0"], ["Indicador - Topos e Fundos 2.0"], ["Coloração - Topos e Fundos 2.0"]],
            "resize_keyboard": True
        }
        self.send_answer("Escolha uma opção:", tipo_plano)
        return
    
    def ativacao_plano(self, tipo_plano):
        tipo_plano = {
            "keyboard": [["Plano Mensal"], ["Plano Simestral"], ["Plano Anual"]],
            "resize_keyboard": True
        }
        
        presente = any(tipo_plano in sublist for sublist in tipo_plano["keyboard"])
        if presente:
            print("A string está presente na estrutura tipo_plano")
        else:
            print("A string não está presente na estrutura tipo_plano")
        self.send_answer("Escolha uma opção para ativar o plano:", tipo_plano)
        return

    def send_answer(self, answer, reply_markup=None):
        url = f"{self.url}sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": answer
        }
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup)
        response = requests.post(url, json=data)
        return response.json()

# ativar - Adquirir o arquivo definitivo (1 mês)
# precos - Informações de preços (mensal / semestral / anual)
# status - Informações sobre seu plano.      
# teste  - Adquirir o arquivo de testes  (7 dias) 
# help   - Ajuda  