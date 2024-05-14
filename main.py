from src.telegramBot import TelegramBot
from src.driveBot import driveBot

if (__name__ == "__main__"):
    try:
        bot = TelegramBot()
        bot.start_bot()
    except:
        print("O bot está sendo encerrado.")