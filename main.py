from src.telegramBot import TelegramBot
from src.driveBot import driveBot

if (__name__ == "__main__"):
    try:
        bot = TelegramBot()
        bot.start_bot()
        drive_bot = driveBot()
        get_data = drive_bot.get_data()
    except:
        print("O bot está sendo encerrado.")