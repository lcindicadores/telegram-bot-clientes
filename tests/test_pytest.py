from src.telegramBot import TelegramBot
from src.telegramBot import LISTA_ERROS,LISTA_COMANDOS,LISTA_PRODUTOS,LISTA_TIPOS_PLANOS
from src.driveBot import driveBot
import os
'''
  string name_test = "Deve calculateRideular o valor de uma corrida de taxi em dias normais";
  // given (dado quem, cenário) Arrange
  double distance = 1000;
  datetime date = D'2021.07.10 10:00:00'; 
  //when (quando algo acontecer) Act       
  double expect = example1.calculateRide(distance,date);
  double toBe = 2100;                         
  //then (então algo deve ser verificado) Assert
  test.expectToBe(name_test,expect,toBe);
'''

def test_deve_verificar_conexao():
    drive_bot = driveBot()
    get_data = drive_bot.get_data()
    assert get_data is not False

def test_deve_conferir_preco_p1_mensal():
    bot = TelegramBot()
    n1 = "Indicador e Coloração - Topos e Fundos 2.0"
    t1 = "Plano Mensal"    
    p1_m = float(os.getenv("PRECO_P1_M"))
    bot.escolha_nome_plano(n1)
    bot.escolha_tipo_plano(t1)
    bot.defini_preco_plano()
    assert bot.preco_plano == p1_m

def test_deve_conferir_preco_p1_semestral():
    bot = TelegramBot()
    n1 = "Indicador e Coloração - Topos e Fundos 2.0"
    t2 = "Plano Semestral" 
    p1_s = float(os.getenv("PRECO_P1_S"))    
    bot.escolha_nome_plano(n1)
    bot.escolha_tipo_plano(t2)
    bot.defini_preco_plano()
    assert bot.preco_plano == p1_s

def test_deve_conferir_preco_p1_anual():
    bot = TelegramBot()
    n1 = "Indicador e Coloração - Topos e Fundos 2.0"
    t3 = "Plano Anual" 
    p1_a = float(os.getenv("PRECO_P1_A"))    
    bot.escolha_nome_plano(n1)
    bot.escolha_tipo_plano(t3)
    bot.defini_preco_plano()
    assert bot.preco_plano == p1_a

def test_deve_conferir_preco_p2_mensal():
    bot = TelegramBot()
    n2 = "Indicador - Topos e Fundos 2.0"
    t1 = "Plano Mensal" 
    p2_m = float(os.getenv("PRECO_P2_M"))    
    bot.escolha_nome_plano(n2)
    bot.escolha_tipo_plano(t1)
    bot.defini_preco_plano()
    assert bot.preco_plano == p2_m

def test_deve_conferir_preco_p2_semestral():
    bot = TelegramBot()
    n2 = "Indicador - Topos e Fundos 2.0"
    t2 = "Plano Semestral"    
    p2_s = float(os.getenv("PRECO_P2_S"))    
    bot.escolha_nome_plano(n2)
    bot.escolha_tipo_plano(t2)
    bot.defini_preco_plano()
    assert bot.preco_plano == p2_s

def test_deve_conferir_preco_p2_anual():
    bot = TelegramBot()
    n2 = "Indicador - Topos e Fundos 2.0"
    t3 = "Plano Anual"   
    p2_a = float(os.getenv("PRECO_P2_A"))    
    bot.escolha_nome_plano(n2)
    bot.escolha_tipo_plano(t3)
    bot.defini_preco_plano()
    assert bot.preco_plano == p2_a

def test_deve_conferir_preco_p3_mensal():
    bot = TelegramBot()
    n3 = "Coloração - Topos e Fundos 2.0"
    t1 = "Plano Mensal"    
    p3_m = float(os.getenv("PRECO_P3_M"))    
    bot.escolha_nome_plano(n3)
    bot.escolha_tipo_plano(t1)
    bot.defini_preco_plano()
    assert bot.preco_plano == p3_m

def test_deve_conferir_preco_p3_semestral():
    bot = TelegramBot()
    n3 = "Coloração - Topos e Fundos 2.0"
    t2 = "Plano Semestral"  
    p3_s = float(os.getenv("PRECO_P3_S"))    
    bot.escolha_nome_plano(n3)
    bot.escolha_tipo_plano(t2)
    bot.defini_preco_plano()
    assert bot.preco_plano == p3_s

def test_deve_conferir_preco_p3_anual():
    bot = TelegramBot()
    n3 = "Coloração - Topos e Fundos 2.0"
    t3 = "Plano Anual"    
    p3_a = float(os.getenv("PRECO_P3_A"))    
    bot.escolha_nome_plano(n3)
    bot.escolha_tipo_plano(t3)
    bot.defini_preco_plano()
    assert bot.preco_plano == p3_a

def test_deve_conferir_texto_precos():
    texto_ofertas = "📢 ! Ofertas Especiais ! 📢\n\n🎉 Confira nossos preços para os Plano Mensal, Plano Semestral e Plano Anual:\n\n🔹 Indicador e Coloração - Topos e Fundos 2.0: \n- Plano Mensal:      R$ 49.80\n- Plano Semestral: R$ 249.80 [-16.40%]\n- Plano Anual:         R$ 499.80 [-16.37%]\n\n🔹 Indicador - Topos e Fundos 2.0: \n- Plano Mensal:      R$ 29.90\n- Plano Semestral: R$ 149.90 [-16.44%]\n- Plano Anual:         R$ 299.90 [-16.42%]\n\n🔹 Coloração - Topos e Fundos 2.0: \n- Plano Mensal:      R$ 19.90\n- Plano Semestral: R$ 99.90  [-16.33%]\n- Plano Anual:        R$ 199.90 [-16.29%]\n\nAproveite esses preços incríveis e invista no seu trade sistem! 💰✨\n➡️➡️ /ativar ⬅️⬅️"
    bot = TelegramBot()
    assert bot.precos() == texto_ofertas 