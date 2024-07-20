import telebot
import sqlite3
import database

API_TOKEN = '7006081046:AAFPbndJeFGBR4_tTQXHcItRZ0F4NJ4PsJw'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    message_ =  f'╭────────»»❀❀❀««────────╮\n'\
                f'      Привет, {message.from_user.first_name} \n'\
                f'      Бот был создан для: \n'\
                f'      @solarezzov и @klovedzz\n'\
                f'\n'\
                f'      Разработчик: @solarezzov \n'\
                f'╰────────»»❀❀❀««────────╯'
    #bot.reply_to(message, f'Привет, {message.from_user.first_name}')
    bot.reply_to(message, message_)
    
    database.db_table_val(user_id=message.from_user.id, user_name=message.from_user.first_name)
    
bot.infinity_polling()