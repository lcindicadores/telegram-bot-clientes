from src.driveBot import driveBot

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

def test_verifica_conexao():
    drive_bot = driveBot()
    get_data = drive_bot.get_data()
    assert get_data is not False

def test_meuprimeirotest():
    assert True