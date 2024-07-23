import telebot
from telebot import types
import database

API_TOKEN = '7006081046:AAFPbndJeFGBR4_tTQXHcItRZ0F4NJ4PsJw'

bot = telebot.TeleBot(API_TOKEN)

id = [0]
name = ['0']
username = ['0']

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
    button_partner = types.InlineKeyboardButton('👩🏻‍❤️‍👨🏻 Партнёр', callback_data='partner')
    button_pet = types.InlineKeyboardButton('🐾 Питомец', callback_data='pet')
    markup.row(button_profile, button_pet, button_partner)
    bot.reply_to(message, message_, reply_markup=markup)
    try:
        database.db_table_val(user_id=message.from_user.id, user_name=message.from_user.first_name, user_nameid=message.from_user.username)
    except:
        pass

@bot.message_handler(func=lambda message: database.db_info(message.chat.id)[4] == 0)
def handle_id_input(message):
    markup = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton('✔️ Да', callback_data='yes')
    button_no = types.InlineKeyboardButton('❌ Нет', callback_data='no')
    markup.row(button_yes, button_no)
    part = message.text
    name[0] = message.from_user.first_name
    id[0] = message.chat.id
    username[0] = message.from_user.username
    database.request_partner_id(part, message.chat.id)
    try:
        bot.send_message(part, "📨 Вам отправили запрос на партнерство", reply_markup=markup)
    except:
        bot.reply_to(message, "⚠️ id не найден")
    
@bot.message_handler(func=lambda message: database.db_info(message.chat.id)[4] > 0 and database.db_info(message.chat.id)[3] != "Питомец не выбран" and database.db_info(message.chat.id)[3] == 'Питомца нет')
def handle_petname_input(message):
    database.petname_update(message.text, message.chat.id)
    database.petname_update(message.text, database.db_info(message.chat.id)[4])
    bot.send_message(message.chat.id, f'❤️ Вы присвоили питомцу имя - "{database.db_info(message.chat.id)[3]}"')
    bot.send_message(database.db_info(message.chat.id)[4], f'❤️ Партнёр присвоил имя питомцу - "{database.db_info(message.chat.id)[3]}"')
    
def choice_pet(message):
    markup = types.InlineKeyboardMarkup()
    button_dog = types.InlineKeyboardButton('🐶 Собака', callback_data='dog')
    button_cat = types.InlineKeyboardButton('🐱 Кот', callback_data='cat')
    button_squirrel = types.InlineKeyboardButton('🐿️ Белка', callback_data='squirrel')
    button_hamster = types.InlineKeyboardButton('🐹 Хомяк', callback_data='hamster')
    button_turtle = types.InlineKeyboardButton('🐢 Черепаха', callback_data='turtle')
    button_parrot = types.InlineKeyboardButton('🦜 Попугай', callback_data='parrot')
    markup.add(button_dog, button_cat, button_squirrel)
    markup.add(button_hamster, button_turtle, button_parrot)
    bot.send_message(message.chat.id, "Выберите питомца: ", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.answer_callback_query(call.id)
    if call.data == 'profile':
        profile_function(call.message)
    elif call.data == 'pet':
        if database.db_info(call.message.chat.id)[4] == 0:
            bot.send_message(call.message.chat.id, "❌ У вас нет партнёра!")
        else:
            choice_pet(call.message)
    elif call.data == 'partner':
        if database.db_info(call.message.chat.id)[4] > 0:
            bot.send_message(call.message.chat.id, f"Информация по партнёру:\nВаш партнёр: {database.db_info(call.message.chat.id)[8]} ")
        else:
            bot.send_message(call.message.chat.id, "⌨️ Введите [ID] пользователя: ")
    elif call.data == 'yes':
        profile_partner(call.message)
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, '🚫 Вам отказали в партнерстве')
        database.request_partner_id(0, call.message.chat.id)
    elif call.data == 'dog':
        markup = types.InlineKeyboardMarkup()
        button_yesdog = types.InlineKeyboardButton('✔️ Одобряю', callback_data='yesdog')
        button_nodog = types.InlineKeyboardButton('❌ Не одобряю', callback_data='notapprove')
        markup.row(button_yesdog, button_nodog)
        bot.send_message(call.message.chat.id, '⚠️ Ваш партнёр должен одобрить Ваш выбор. Ожидаем одобрения...')
        bot.send_message(database.db_info(call.message.chat.id)[4], '⚠️ Ваш партнёр выбрал питомца "🐶 Собака". Нажмите на кнопку в связи с вашим решением.', reply_markup=markup)
    elif call.data == 'cat':
        markup = types.InlineKeyboardMarkup()
        button_yescat = types.InlineKeyboardButton('✔️ Одобряю', callback_data='yescat')
        button_nocat = types.InlineKeyboardButton('❌ Не одобряю', callback_data='notapprove')
        markup.row(button_yescat, button_nocat)
        bot.send_message(call.message.chat.id, '⚠️ Ваш партнёр должен одобрить Ваш выбор. Ожидаем одобрения...')
        bot.send_message(database.db_info(call.message.chat.id)[4], '⚠️ Ваш партнёр выбрал питомца "🐱 Кот". Нажмите на кнопку в связи с вашим решением.', reply_markup=markup)
    elif call.data == 'squirrel':
        markup = types.InlineKeyboardMarkup()
        button_yesbelka = types.InlineKeyboardButton('✔️ Одобряю', callback_data='yesbelka')
        button_nobelka = types.InlineKeyboardButton('❌ Не одобряю', callback_data='notapprove')
        markup.row(button_yesbelka, button_nobelka)
        bot.send_message(call.message.chat.id, '⚠️ Ваш партнёр должен одобрить Ваш выбор. Ожидаем одобрения...')
        bot.send_message(database.db_info(call.message.chat.id)[4], '⚠️ Ваш партнёр выбрал питомца "🐿️ Белка". Нажмите на кнопку в связи с вашим решением.', reply_markup=markup)
    elif call.data == 'hamster':
        markup = types.InlineKeyboardMarkup()
        button_yeshamster = types.InlineKeyboardButton('✔️ Одобряю', callback_data='yeshamster')
        button_nohamster = types.InlineKeyboardButton('❌ Не одобряю', callback_data='notapprove')
        markup.row(button_yeshamster, button_nohamster)
        bot.send_message(call.message.chat.id, '⚠️ Ваш партнёр должен одобрить Ваш выбор. Ожидаем одобрения...')
        bot.send_message(database.db_info(call.message.chat.id)[4], '⚠️ Ваш партнёр выбрал питомца "🐹 Хомяк". Нажмите на кнопку в связи с вашим решением.', reply_markup=markup)
    elif call.data == 'turtle':
        markup = types.InlineKeyboardMarkup()
        button_yesturtle = types.InlineKeyboardButton('✔️ Одобряю', callback_data='yesturtle')
        button_noturtle = types.InlineKeyboardButton('❌ Не одобряю', callback_data='notapprove')
        markup.row(button_yesturtle, button_noturtle)
        bot.send_message(call.message.chat.id, '⚠️ Ваш партнёр должен одобрить Ваш выбор. Ожидаем одобрения...')
        bot.send_message(database.db_info(call.message.chat.id)[4], '⚠️ Ваш партнёр выбрал питомца "🐢 Черепаха". Нажмите на кнопку в связи с вашим решением.', reply_markup=markup)
    elif call.data == 'parrot':
        markup = types.InlineKeyboardMarkup()
        button_yesparrot = types.InlineKeyboardButton('✔️ Одобряю', callback_data='yesparrot')
        button_noparrot = types.InlineKeyboardButton('❌ Не одобряю', callback_data='notapprove')
        markup.row(button_yesparrot, button_noparrot)
        bot.send_message(call.message.chat.id, '⚠️ Ваш партнёр должен одобрить Ваш выбор. Ожидаем одобрения...')
        bot.send_message(database.db_info(call.message.chat.id)[4], '⚠️ Ваш партнёр выбрал питомца "🦜 Попугай". Нажмите на кнопку в связи с вашим решением.', reply_markup=markup)
    elif call.data == 'yesdog':
        database.pet_update("🐶 Собака", call.message.chat.id)
        database.pet_update("🐶 Собака", database.db_info(call.message.chat.id)[4])
        bot.send_message(database.db_info(call.message.chat.id)[4], f'👩🏻‍❤️‍👨🏻 Партнёр одобрил Ваш выбор. Теперь у вас есть питомец {database.db_info(call.message.chat.id)[2]}.\nТеперь напишите имя питомца, перед тем как написать обязательно хорошо посоветуйтесь с партнёром! Имя:')
        bot.send_message(call.message.chat.id, f'👩🏻‍❤️‍👨🏻 Вы одобрили выбор. Теперь у вас есть питомец {database.db_info(call.message.chat.id)[2]}')
    elif call.data == 'yescat':
        database.pet_update("🐱 Кот", call.message.chat.id)
        database.pet_update("🐱 Кот", database.db_info(call.message.chat.id)[4])
        bot.send_message(database.db_info(call.message.chat.id)[4], f'👩🏻‍❤️‍👨🏻 Партнёр одобрил Ваш выбор. Теперь у вас есть питомец {database.db_info(call.message.chat.id)[2]}.\nТеперь напишите имя питомца, перед тем как написать обязательно хорошо посоветуйтесь с партнёром! Имя:')
        bot.send_message(call.message.chat.id, f'👩🏻‍❤️‍👨🏻 Вы одобрили выбор. Теперь у вас есть питомец {database.db_info(call.message.chat.id)[2]}')
    elif call.data == 'yesbelka':
        database.pet_update("🐿️ Белка", call.message.chat.id)
        database.pet_update("🐿️ Белка", database.db_info(call.message.chat.id)[4])
        bot.send_message(database.db_info(call.message.chat.id)[4], f'👩🏻‍❤️‍👨🏻 Партнёр одобрил Ваш выбор. Теперь у вас есть питомец {database.db_info(call.message.chat.id)[2]}.\nТеперь напишите имя питомца, перед тем как написать обязательно хорошо посоветуйтесь с партнёром! Имя:')
        bot.send_message(call.message.chat.id, f'👩🏻‍❤️‍👨🏻 Вы одобрили выбор. Теперь у вас есть питомец {database.db_info(call.message.chat.id)[2]}')
    elif call.data == 'yeshamster':
        database.pet_update("🐹 Хомяк", call.message.chat.id)
        database.pet_update("🐹 Хомяк", database.db_info(call.message.chat.id)[4])
        bot.send_message(database.db_info(call.message.chat.id)[4], f'👩🏻‍❤️‍👨🏻 Партнёр одобрил Ваш выбор. Теперь у вас есть питомец {database.db_info(call.message.chat.id)[2]}.\nТеперь напишите имя питомца, перед тем как написать обязательно хорошо посоветуйтесь с партнёром! Имя:')
        bot.send_message(call.message.chat.id, f'👩🏻‍❤️‍👨🏻 Вы одобрили выбор. Теперь у вас есть питомец {database.db_info(call.message.chat.id)[2]}')
    elif call.data == 'yesturtle':
        database.pet_update("🐢 Черепаха", call.message.chat.id)
        database.pet_update("🐢 Черепаха", database.db_info(call.message.chat.id)[4])
        bot.send_message(database.db_info(call.message.chat.id)[4], f'👩🏻‍❤️‍👨🏻 Партнёр одобрил Ваш выбор. Теперь у вас есть питомец {database.db_info(call.message.chat.id)[2]}.\nТеперь напишите имя питомца, перед тем как написать обязательно хорошо посоветуйтесь с партнёром! Имя:')
        bot.send_message(call.message.chat.id, f'👩🏻‍❤️‍👨🏻 Вы одобрили выбор. Теперь у вас есть питомец {database.db_info(call.message.chat.id)[2]}')
    elif call.data == 'yesparrot':
        database.pet_update("🦜 Попугай", call.message.chat.id)
        database.pet_update("🦜 Попугай", database.db_info(call.message.chat.id)[4])
        bot.send_message(database.db_info(call.message.chat.id)[4], f'👩🏻‍❤️‍👨🏻 Партнёр одобрил Ваш выбор. Теперь у вас есть питомец {database.db_info(call.message.chat.id)[2]}.\nТеперь напишите имя питомца, перед тем как написать обязательно хорошо посоветуйтесь с партнёром! Имя:')
        bot.send_message(call.message.cht.id, f'👩🏻‍❤️‍👨🏻 Вы одобрили выбор. Теперь у вас есть питомец {database.db_info(call.message.chat.id)[2]}')
    elif call.data == 'notapprove':
        bot.send_message(call.message.chat.id, "❌ Ваш партнёр не одобрил Ваш выбор.")
        
def profile_partner(message):
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text= "🤝🏻 Вы теперь партнеры")
    bot.send_message(id[0], "🤝🏻 Вы теперь партнеры")
    database.db_partner(database.db_info(message.chat.id)[0], database.db_info(message.chat.id)[1], id[0], database.db_info(message.chat.id)[7])
    database.db_partner(id[0], name[0], message.chat.id, username[0])
    database.request_partner_id(0, id[0])
    
def profile_function(message):
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=
'╭────»»❀❀❀»»\n'\
f'| 📋 Ваш профиль:\n'\
f'| 👤 Имя - {database.db_info(message.chat.id)[1]}\n'\
f'| 👩🏻‍❤️‍👨🏻 Партнер - {database.db_info(message.chat.id)[5]}\n'\
f'| 🐾 Питомец - {database.db_info(message.chat.id)[3]}\n'\
'|───────────────\n'\
'| 📌 Информация по питомцу:\n'\
f'| 🔠 Имя питомца - \n'\
f'| 🌍 Месторасположение - \n'\
f'| 🩺 Здоровье -  \n'\
f'| 🍽️ Еда - \n'\
f'| 💦 Вода - \n'\
'╰────»»❀❀❀»»')


bot.infinity_polling()
print("bot started")