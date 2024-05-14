from dotenv import load_dotenv
from src.driveBot import driveBot
from src.pagamento import Pagamento
from src.vendas import vendas
from datetime import datetime
import os
import requests 
import json

load_dotenv()
SEMESTRE = 6
ANUAL = 12
#Depois tirar daqui e colocar em uma arquivo que possa proteger os dados
ADMINS = [ 
    {
        'chat_id': "1103680702",
        'phone_number': "+5584996736660",
        'first_name': "LC Indicadores",
        'last_name': "Leopoldo Couto",
        'cargo': "CEO",
    },
    {
        'chat_id': "1227186829",
        'phone_number': "+5584999683352",
        'first_name': "LC Indicadores",
        'last_name': "Júlia Fagundes",
        'cargo': "Suporte"
    },
]

LISTA_COMANDOS = {
    '/ativar': "Adquirir estratégia (mensal / semestral / anual)",
    '/precos': "Informações de preços (mensal / semestral / anual)",
    '/status': "Informações sobre sua(s) estratégia(s)",     
    '/suporte': "Contato do suporte",
    '/teste':  "Adquirir o arquivo de testes  (7 dias)",
    '/help':   "Totas as opções de comando do bot no Telegram",
}
LISTA_ERROS = {
    '100': "Erro ao cadastrar cliente.",
    '201': "Falha no envio do arquivo TESTE.",
    '202': "Você já solicitou o arquivo de TESTE anteriormente.",
}
LISTA_PRODUTOS = [
    {
        'nome': "Indicador e Coloração - Topos e Fundos 2.0",
        'plano_mensal': float(os.getenv("PRECO_P1_M")),
        'plano_semestral': float(os.getenv("PRECO_P1_S")),
        'plano_anual': float(os.getenv("PRECO_P1_A")),
        'plataforma': "Profit",
        'link_video': "https://youtu.be/QK2vVYqkcUU",              
    },
    {
        'nome': "Indicador - Topos e Fundos 2.0",
        'plano_mensal': float(os.getenv("PRECO_P2_M")),
        'plano_semestral': float(os.getenv("PRECO_P2_S")),
        'plano_anual': float(os.getenv("PRECO_P2_A")),
        'plataforma': "Profit",
        'link_video': "https://youtu.be/QK2vVYqkcUU",              
    },
    {
        'nome': "Coloração - Topos e Fundos 2.0",
        'plano_mensal': float(os.getenv("PRECO_P3_M")),
        'plano_semestral': float(os.getenv("PRECO_P3_S")),
        'plano_anual': float(os.getenv("PRECO_P3_A")),
        'plataforma': "Profit",
        'link_video': "https://youtu.be/IGNnz7ZwKa4",              
    },
]
LISTA_TIPOS_PLANOS = [
    "Plano Mensal",
    "Plano Semestral",
    "Plano Anual",
]
class TelegramBot:
    def __init__(self):
        TOKEN = os.getenv("TOKEN_BOT_TELEGRAM")
        self.url = f"https://api.telegram.org/bot{TOKEN}/"
        self.chat_id = None
        self.nome_plano = None
        self.tipo_plano = None
        self.preco_plano = None
        self.email = None

    def start_bot(self):
        update_id = None
        vd = vendas()
        print("Inicializando bot...")
        while True:
            vd.verifica_validade_teste()
            update = self.get_message(update_id)
            messages = update['result']
            if not messages: 
                print("Aguardando Clientes...")
            for message in messages:
                try:
                    update_id = message['update_id']
                    message_text = message['message']['text']
                    self.set_chat_id(message['message']['from']['id'])
                    if(message_text == self.index_key_arr(0)):
                        self.ativar()
                    elif(message_text == self.index_key_arr(1)):
                        self.precos()                        
                    elif(message_text == self.index_key_arr(2)):
                        self.status()                        
                    elif(message_text == self.index_key_arr(3)):
                        self.send_contact()     
                    elif(message_text == self.index_key_arr(4)):
                        self.teste(message)
                    elif(message_text == self.index_key_arr(5)):
                        self.lista_help()                                                                  
                    elif(message_text == "/erros"):
                        self.lista_erros()     
                    elif(message_text == self.get_prod_lista(0,LISTA_PRODUTOS,'nome')):                       
                        self.escolha_nome_plano(self.get_prod_lista(0,LISTA_PRODUTOS,'nome'))
                    elif(message_text == self.get_prod_lista(1,LISTA_PRODUTOS,'nome')):                      
                        self.escolha_nome_plano(self.get_prod_lista(1,LISTA_PRODUTOS,'nome'))
                    elif(message_text == self.get_prod_lista(2,LISTA_PRODUTOS,'nome')):                    
                        self.escolha_nome_plano(self.get_prod_lista(2,LISTA_PRODUTOS,'nome'))
                    elif(message_text == LISTA_TIPOS_PLANOS[0]):                     
                        self.escolha_tipo_plano(LISTA_TIPOS_PLANOS[0])
                    elif(message_text == LISTA_TIPOS_PLANOS[1]):                     
                        self.escolha_tipo_plano(LISTA_TIPOS_PLANOS[1])
                    elif(message_text == LISTA_TIPOS_PLANOS[2]):                      
                        self.escolha_tipo_plano(LISTA_TIPOS_PLANOS[2]) 
                    elif(message_text == "Confirmar Compra"): 
                        self.confirmar_compra('PIX') # depois fazer um jeito de selecionar e armazenar o tipo da compra                                                                   
                except:
                    pass    
    ## ao final lembrar de colocar as funcoes set`s em particular a classe                    
    def set_chat_id(self,chat_id):
        self.chat_id = chat_id
    def set_nome_plano(self,nome_plano):
        self.nome_plano = nome_plano
    def set_tipo_plano(self,tipo_plano):
        self.tipo_plano = tipo_plano.lower().replace(" ","_")
    def set_preco_plano(self,preco_plano):
        self.preco_plano = preco_plano
    def get_message(self,update_id):
        TIMEOUT = os.getenv("TIME_OUT_REQUEST")
        link_request = f"{self.url}getUpdates?timeout={TIMEOUT}"
        if update_id:
            link_request = f"{self.url}getUpdates?timeout={TIMEOUT}&offset={update_id + 1}"   
        result = requests.get(link_request)
        return json.loads(result.content)  
    
    def index_key_arr(serlf,index):
        chaves = list(LISTA_COMANDOS.keys())
        if index < len(chaves):
            return chaves[index]
        else:
            return None   
        
    def ativar(self):
        tipos_plano = {
            "keyboard": [[self.get_prod_lista(0,LISTA_PRODUTOS,'nome')],[self.get_prod_lista(1,LISTA_PRODUTOS,'nome')],[self.get_prod_lista(2,LISTA_PRODUTOS,'nome')]],
            "resize_keyboard": True
        }
        self.send_answer(self.chat_id,"Escolha uma opção:",tipos_plano)
        return
    
    def precos(self):
        nome_p1 = self.get_prod_lista(0,LISTA_PRODUTOS,'nome')
        nome_p2 = self.get_prod_lista(1,LISTA_PRODUTOS,'nome')
        nome_p3 = self.get_prod_lista(2,LISTA_PRODUTOS,'nome')
        preco_p1_m = self.get_prod_lista(0,LISTA_PRODUTOS,'plano_mensal')
        preco_p2_m = self.get_prod_lista(1,LISTA_PRODUTOS,'plano_mensal')
        preco_p3_m = self.get_prod_lista(2,LISTA_PRODUTOS,'plano_mensal')
        preco_p1_s = self.get_prod_lista(0,LISTA_PRODUTOS,'plano_semestral')
        preco_p2_s = self.get_prod_lista(1,LISTA_PRODUTOS,'plano_semestral')
        preco_p3_s = self.get_prod_lista(2,LISTA_PRODUTOS,'plano_semestral')
        preco_p1_a = self.get_prod_lista(0,LISTA_PRODUTOS,'plano_anual')
        preco_p2_a = self.get_prod_lista(1,LISTA_PRODUTOS,'plano_anual')
        preco_p3_a = self.get_prod_lista(2,LISTA_PRODUTOS,'plano_anual')
        desc_p1_sem = ((preco_p1_s)/(preco_p1_m*SEMESTRE) - 1) * 100
        desc_p2_sem = ((preco_p2_s)/(preco_p2_m*SEMESTRE) - 1) * 100
        desc_p3_sem = ((preco_p3_s)/(preco_p3_m*SEMESTRE) - 1) * 100
        desc_p1_ano = ((preco_p1_a)/(preco_p1_m*ANUAL) - 1) * 100
        desc_p2_ano = ((preco_p2_a)/(preco_p2_m*ANUAL) - 1) * 100
        desc_p3_ano = ((preco_p3_a)/(preco_p3_m*ANUAL) - 1) * 100        
        str_p1 = f"🔹 {nome_p1}: \n- {LISTA_TIPOS_PLANOS[0]}:      R$ {preco_p1_m:.2f}\n- {LISTA_TIPOS_PLANOS[1]}: R$ {preco_p1_s:.2f} [{desc_p1_sem:.2f}%]\n- {LISTA_TIPOS_PLANOS[2]}:         R$ {preco_p1_a:.2f} [{desc_p1_ano:.2f}%]"
        str_p2 = f"🔹 {nome_p2}: \n- {LISTA_TIPOS_PLANOS[0]}:      R$ {preco_p2_m:.2f}\n- {LISTA_TIPOS_PLANOS[1]}: R$ {preco_p2_s:.2f} [{desc_p2_sem:.2f}%]\n- {LISTA_TIPOS_PLANOS[2]}:         R$ {preco_p2_a:.2f} [{desc_p2_ano:.2f}%]"
        str_p3 = f"🔹 {nome_p3}: \n- {LISTA_TIPOS_PLANOS[0]}:      R$ {preco_p3_m:.2f}\n- {LISTA_TIPOS_PLANOS[1]}: R$ {preco_p3_s:.2f}  [{desc_p3_sem:.2f}%]\n- {LISTA_TIPOS_PLANOS[2]}:        R$ {preco_p3_a:.2f} [{desc_p3_ano:.2f}%]"
        answer_bot = f"📢 ! Ofertas Especiais ! 📢\n\n🎉 Confira nossos preços para os {LISTA_TIPOS_PLANOS[0]}, {LISTA_TIPOS_PLANOS[1]} e {LISTA_TIPOS_PLANOS[2]}:\n\n{str_p1}\n\n{str_p2}\n\n{str_p3}\n\nAproveite esses preços incríveis e invista no seu trade sistem! 💰✨\n➡️➡️ /ativar ⬅️⬅️"
        self.send_answer(self.chat_id,answer_bot)     
        return answer_bot
        
    def status(self):
        return
    
    def send_contact(self):
        url = f"{self.url}sendContact"
        index_main_admin = 0
        data = {
            'chat_id': self.chat_id,
            'phone_number': ADMINS[index_main_admin]['phone_number'],
            'first_name': ADMINS[index_main_admin]['first_name']
        }
        response = requests.post(url,json=data)
        answer_bot = f"{ADMINS[index_main_admin]['last_name']} / {ADMINS[index_main_admin]['cargo']}"
        self.send_answer(self.chat_id,answer_bot)  
        return response.json() 
               
    def teste(self,message):
        dado_test = self.get_data_client_test(message)
        cadastro_cliente = self.cadastro_cliente(dado_test)

        if(cadastro_cliente == None): return
        if(cadastro_cliente == False):
            answer_admins = f"{LISTA_ERROS['100']} Dados: \n{dado_test}"
            self.send_answer_admins(answer_admins) 
            self.send_contact()
            answer_cli= f"Por favor entre em contato com o suporte. Informe Erro 100."
            self.send_answer(self.chat_id,answer_cli)  
            return
        dias_teste = os.getenv("DIAS_VALIDADE") 
        link_video = self.get_prod_lista(0,LISTA_PRODUTOS,'link_video')
        answer_bot = f"Estratégia: {self.get_prod_lista(0,LISTA_PRODUTOS,'nome')}\nTipo Arquivo: Arquivo para testes [{dias_teste} dias]\nValidade: {dado_test['validade']}\nVideo: {link_video}"
        self.send_answer(self.chat_id,answer_bot)  
        path_name = self.set_path_name("TESTE",self.get_prod_lista(0,LISTA_PRODUTOS,'nome'),dado_test['validade'])
        if(not self.send_document(path_name)): 
            self.send_answer_admins(answer_admins) 
            answer_bot = f"{LISTA_ERROS['201']} Por favor entre em contato com o suporte. Informe Erro 201"
            self.send_answer(self.chat_id,answer_bot)             
            return
        return     
    
    def lista_help(self):
        answer_bot = "LISTA DE COMANDOS:\n"
        answer_bot += "\n".join([f"{key}: {value}" for key,value in LISTA_COMANDOS.items()])
        self.send_answer(self.chat_id,answer_bot)   
        return    
      
    def lista_erros(self):
        if (not self.is_admin()): return
        answer_bot = "LISTA DE ERROS:\n"
        answer_bot += "\n".join([f"{key}: {value}" for key,value in LISTA_ERROS.items()])
        self.send_answer(self.chat_id,answer_bot)            
        return

    def escolha_nome_plano(self,nome_plano):
        tipo_plano = {
            "keyboard": LISTA_TIPOS_PLANOS,
            "resize_keyboard": True
        }
        self.set_nome_plano(nome_plano)
        #self.send_answer(self.chat_id,"Escolha uma opção para ativar o plano:", tipo_plano)
        return

    def escolha_tipo_plano(self, tipo_plano):
        confi_cance = {
            "keyboard": [["Confirmar Compra"],["Cancelar"]],
            "resize_keyboard": True
        } 
        self.set_tipo_plano(tipo_plano)
        #self.send_answer(self.chat_id,"Escolha uma opção: ", confi_cance)
        return
    
    def defini_preco_plano(self):
        for produto in LISTA_PRODUTOS:
            if produto['nome'] == self.nome_plano:
                self.set_preco_plano(produto[self.tipo_plano])
        return    
        
    def is_admin(self):
        for admin in ADMINS:
            if admin['chat_id'] == str(self.chat_id):
                return True
        return False
    
    def cadastro_cliente(self, dado_test):
        drive_bot = driveBot()
        if(drive_bot.verificar_dados(self.chat_id, 'ID')): 
            answer_bot = f"{LISTA_ERROS['202']} \nDigite /ativar para adquirir a estratégia definitiva ou /help para ver todas as opções"
            self.send_answer(self.chat_id,answer_bot) 
            return 
        dado_testlist = list(dado_test.values())
        return drive_bot.inserir_dados(dado_testlist)
    
    def get_data_client_test(self, message):
        chat_id = message['message']['from']['id']
        origem = 'Telegram'
        first_name = message['message']['from']['first_name']
        last_name = message['message']['from']['last_name']
        telefone = '055'
        nome_estrategia = self.get_prod_lista(0,LISTA_PRODUTOS,'nome')
        date = datetime.fromtimestamp(message['message']['date'])
        date = date.strftime("%d-%m-%Y")
        validade = self.get_validade(date)
        msg_vendas = False
        dado = {
            'chat_id': chat_id,
            'origem': origem,
            'first_name': first_name,
            'last_name': last_name,
            'telefone': telefone,
            'nome_estrategia': nome_estrategia,
            'date': date,
            'validade': validade,
            'msg_vendas': msg_vendas
        }   
        return dado
    
    def encontrar_posicao(self,string,array):
        for i,sublist in enumerate(array):
            if string in sublist:
                return i
        return -1  # Retorna -1 se a string não for encontrada
    
    def set_path_name(self,tipo,file_name,validade):
        extensao = ".psf"
        name_file = f"[{tipo} v{validade}] {file_name}{extensao}"
        return name_file

    def get_validade(self,date):
        qtd_dias_validade = os.getenv("DIAS_VALIDADE")
        dia_validade, mes_validade, ano_validade = map(int, date.split("-"))
        dia_validade += int(qtd_dias_validade)-1    
        mes_validade = f"0{mes_validade}" if(mes_validade < 10) else mes_validade
        sep = "-"
        validade = f"{dia_validade}{sep}{mes_validade}{sep}{ano_validade}"
        return validade

    def send_answer(self,chat_id,answer,reply_markup=None):
        url = f"{self.url}sendMessage"
        data = {
            'chat_id': chat_id,
            'text': answer
        }
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup)
        response = requests.post(url,json=data)
        return response.json()
    
    def send_answer_admins(self,answer):
        url = f"{self.url}sendMessage"
        for admins in ADMINS:
            data = {
                'chat_id': admins['chat_id'],
                'text': answer
            }
            response = requests.post(url,json=data)
        return 
    
    def send_photo_qr_code(self, arr_payment):
        url = f"{self.url}sendPhoto"
        file = {'photo': arr_payment[0]}
        data = {
            'chat_id': self.chat_id,
            'caption': arr_payment[1],
            'parse_mode': arr_payment[2]
        }
        response = requests.post(url,data=data,files=file)
        return response.json()

    def send_document(self,name_file):
        url = f"{self.url}sendDocument"
        path = '/Users/leopoldocouto/Desktop/LC Indicadores/Profit/Indicadores/TeF 2.0/Arquivos/Arquivos - Testes/' #trocar para um arquivo no drive       
        if(not os.path.isfile(f"{path}{name_file}")): 
            print(f"Arquivo não encontrado. \nArquivo: \"{name_file}\"")
            if(not os.path.exists(path)):
                print(f"Pasta não encontrada. \nCaminho: \"{path}\"")       
            return False
        file = {'document': open(f"{path}{name_file}",'rb')}
        data = {'chat_id': self.chat_id}
        response = requests.post(url,data=data,files=file)
        return response.json()      
    
    def send_msg_fim_teste(self):
        db = driveBot()
        lista = db.get_data()
        quantidade_clientes = db.quantidade_clientes()
        col1_lista = lista.iloc[:quantidade_clientes,0]  # Seleciona apenas a primeira coluna    
        msg_fim_teste = vendas.msg_fim_teste()
        for id_clientes in col1_lista: 
            self.send_answer(id_clientes, msg_fim_teste)
            db.atualizar_dados(id_clientes, 'Mensagem Vendas Enviado?', True)

    def get_prod_lista(self,index,lista,atr):
        if index < len(lista):
            return lista[index].get(atr)
        else:
            return None
        
    def confirmar_compra(self, tipo_compra):
        if(tipo_compra == 'PIX'):
            pag = Pagamento()  
            self.defini_preco_plano()
            descricao = f"{self.nome_plano} - {(self.tipo_plano).replace("_"," ").capitalize()}"
            arr_payment = pag.confirmar_compra_pix(0.01,"seusindicadores@gmail.com",descricao)
            if(len(arr_payment) == 1): 
                print("erro ao gerar pagamento: ",arr_payment) 
                return              
            self.send_photo_qr_code(arr_payment)            
'''
Coisas pra fazer

/ativar - 
/precos - Concluido
/status - Pra fazer - Se ta no test a data de validade, se expirou /ativar, se definitivo nome da estrategia tipo de plano e data de validade   
/suporte - Concluido
/teste - Parcialmente Concluido - qnd /status tiver feito colocar qnd ja tiver solicitado anteriormente
/help - Concluido

- Manual/Contrato ao adquirir o produto
'''    