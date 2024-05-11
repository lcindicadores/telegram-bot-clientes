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
bot.escolha_tipo_plano(p1)
bot.defini_preco_plano()

bot.defini_preco_plano()              
#print(bot.send_photo())
id_ = "1805752457"
#pg.confirmar_compra_pix(bot.preco_plano,bot.nome_plano,bot.tipo_plano,bot.email)
pg.obter_pagamento(id_)

'''
bot = TelegramBot()
bot.set_nome_plano(n1)
bot.tipo_plano_selec(p1)

bot.set_nome_plano(n1)
bot.tipo_plano_selec(p2)

bot.set_nome_plano(n1)
bot.tipo_plano_selec(p3)

bot.set_nome_plano(n2)
bot.tipo_plano_selec(p1)

bot.set_nome_plano(n2)
bot.tipo_plano_selec(p2)

bot.set_nome_plano(n2)
bot.tipo_plano_selec(p3)

bot.set_nome_plano(n3)
bot.tipo_plano_selec(p1)

bot.set_nome_plano(n3)
bot.tipo_plano_selec(p2)

bot.set_nome_plano(n3)
bot.tipo_plano_selec(p3)

a1 = (bot.encontrar_posicao(n1,bot.planos))
a2 = (bot.encontrar_posicao(n2,bot.planos))
a3 = (bot.encontrar_posicao(n3,bot.planos))

b1 = (bot.encontrar_posicao(p1,bot.periodo)) + 1
b2 = (bot.encontrar_posicao(p2,bot.periodo)) + 1
b3 = (bot.encontrar_posicao(p3,bot.periodo)) + 1

print(bot.planos[a1][b1])
print(bot.planos[a1][b2])
print(bot.planos[a1][b3])'''

