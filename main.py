from src.telegramBot import TelegramBot
from src.driveBot import driveBot

if (__name__ == "__main__"):
    #bot = TelegramBot()
    #bot.start_bot()
    driveBot = driveBot()
    print(driveBot.get_data())