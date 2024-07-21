import telebot
from telebot import types
import database

API_TOKEN = '7006081046:AAFPbndJeFGBR4_tTQXHcItRZ0F4NJ4PsJw'

bot = telebot.TeleBot(API_TOKEN)

id = [0]
name = ['0']

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
    


def profile_function(message):
    bot.send_message(message.chat.id, f'Ваш профиль:\nИмя: {database.db_info_username(user_id=message.chat.id)[0]}\nВаш питомец: {database.db_info_pet(user_id=message.chat.id)[0]}')
    
@bot.message_handler(commands=['partner'])
def send_welcome(message):
    name[0] = message.from_user.first_name
    id[0] = message.chat.id
    bot.send_message(message.chat.id, "Введите id пользователя")

@bot.message_handler(func=lambda message: database.db_info(message.chat.id)[6] == 0)
def handle_id_input(message):
    markup = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton('Да', callback_data='yes')
    button_no = types.InlineKeyboardButton('Нет', callback_data='no')
    markup.row(button_yes, button_no)
    part = message.text
    database.request_partner_id(part, message.chat.id)
    try:
        bot.send_message(part, "Вам отправили запрос на партнерство", reply_markup=markup)
    except:
        bot.reply_to(message, "id не найден")
    
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.answer_callback_query(call.id)
    if call.data == 'profile':
        profile_function(call.message)
    elif call.data == 'pet':
        bot.send_message(call.message.chat.id, 'Вы выбрали опцию "Питомец"')
    elif call.data == 'yes':
        profile_partner(call.message)
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, 'Вам отказали в партнерстве')
        database.request_partner_id(0, call.message.chat.id)

def profile_partner(message):
    bot.send_message(message.chat.id, "Вы теперь партнеры")
    bot.send_message(id[0], "Вы теперь партнеры")
    database.db_partner(database.db_info(message.chat.id)[0], database.db_info(message.chat.id)[1], id[0])
    database.db_partner(id[0], name[0], message.chat.id)
    database.request_partner_id(0, id[0])
    
bot.infinity_polling()
print("bot started")