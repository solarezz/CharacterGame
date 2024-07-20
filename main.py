import telebot
from telebot import types
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
    markup = types.InlineKeyboardMarkup()
    button_profile = types.InlineKeyboardButton('📋 Профиль', callback_data='profile')
    button_pet = types.InlineKeyboardButton('🐾 Питомец', callback_data='pet')
    markup.row(button_profile, button_pet)
    bot.reply_to(message, message_, reply_markup=markup)
    try:
        database.db_table_val(user_id=message.from_user.id, user_name=message.from_user.first_name)
    except:
        pass
    
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.answer_callback_query(call.id)
    if call.data == 'profile':
        profile_function(call.message)
    elif call.data == 'pet':
        bot.send_message(call.message.chat.id, 'Вы выбрали опцию "Питомец"')

def profile_function(message):
    # Здесь можно добавить функционал для обработки выбора "Профиль"
    bot.send_message(message.chat.id, 'Вы выбрали опцию "Профиль". Выполняю действия по профилю...')
    
bot.infinity_polling()
print("bot started")