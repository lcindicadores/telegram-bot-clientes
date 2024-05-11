from src.telegramBot import TelegramBot
from src.pagamento import Pagamento
import requests
import os

n1 = "Indicador e Coloração - Topos e Fundos 2.0"
n2 = "Indicador - Topos e Fundos 2.0"
n3 = "Coloração - Topos e Fundos 2.0"

p1 = "Plano Mensal"
p2 = "Plano Simestral"
p3 = "Plano Anual"

pg = Pagamento()
bot = TelegramBot()

bot.set_chat_id("1103680702")
bot.escolha_nome_plano(n1)
bot.escolha_tipo_plano(p3)
bot.defini_preco_plano()

print(bot.index_key_dic(0))
'''dia_validade = 14
mes_validade = 5
mes_validade = f"0{mes_validade}" if(mes_validade < 10) else mes_validade
ano_validade = 2024
sep = "-"
validade = f"v{dia_validade}{sep}{mes_validade}{sep}{ano_validade}"
extensao = ".psf"
name_file = f"{n1} {validade}{extensao}"
bot.send_document(name_file)'''