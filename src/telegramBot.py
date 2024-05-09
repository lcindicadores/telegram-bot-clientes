from dotenv import load_dotenv
from src.driveBot import driveBot
import os
import requests 
import json

load_dotenv()

class TelegramBot:
    def __init__(self):
        TOKEN = os.getenv("API_KEY")
        self.url = f"https://api.telegram.org/bot{TOKEN}/"

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
                    chat_id = message['message']['from']['id']
                    if(message_text == "/teste"):
                        drive_bot = driveBot()
                        if(drive_bot.verificar_dados(chat_id)): 
                            answer_bot = "Vc já solicitou o arquivo de testes."
                            self.send_answer(chat_id,answer_bot) 
                            continue 
                        dado_test = self.get_data_client_test(message)
                        drive_bot.inserir_dados(dado_test)
                        answer_bot = "Usuário cadastrado para testes"
                        self.send_answer(chat_id,answer_bot)
                        continue
                    elif(message_text == "/ativar"):
                        #perguntar se quer mensal, simestral ou anual
                        self.ativacao_mes()
                        
                    answer_bot = self.create_answer(message_text)
                    self.send_answer(chat_id,answer_bot)
                except:
                    pass            


    def get_message(self, update_id):
        TIMEOUT = os.getenv("TIME_OUT_REQUEST")
        link_request = f"{self.url}getUpdates?timeout={TIMEOUT}"
        if update_id:
            link_request = f"{self.url}getUpdates?timeout={TIMEOUT}&offset={update_id + 1}"   
        result = requests.get(link_request)
        return json.loads(result.content)  
    
    def get_data_client_test(self, message):
        chat_id = message['message']['from']['id']
        first_name = message['message']['from']['first_name']
        last_name = message['message']['from']['last_name']
        telefone = '055'
        origem = 'Telegram'
        date = message['message']['date']
        dado = [chat_id,first_name,last_name,telefone,origem,date]   
        return dado    

    def ativacao_mes(self):
        return
    
    def create_answer(self, messsage_text):
        return "Olá, tudo bem?"

    def send_answer(self, chat_id, answer):
        link_to_send = f"{self.url}sendMessage?chat_id={chat_id}&text={answer}"
        requests.get(link_to_send)
        return

# ativar - Adquirir o arquivo definitivo (1 mês)
# precos - Informações de preços (mensal / semestral / anual)
# status - Informações sobre seu plano.      
# teste  - Adquirir o arquivo de testes  (7 dias) 
# help   - Ajuda  