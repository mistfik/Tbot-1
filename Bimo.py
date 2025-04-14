import telebot
from telebot import types

TOKEN = ''
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = '' # айди кому приходит сообщение
ADMIN_ID2 = '' # айди кому приходит сообщение
user_data = {}


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    report_btn = types.KeyboardButton('Отчет за мероприятие')
    propose_btn = types.KeyboardButton('Предложить мероприятие')
    yes_btn = types.KeyboardButton('Готово')
    markup.add(report_btn, propose_btn, yes_btn)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['Отчет за мероприятие', 'Предложить мероприятие'])
def handle_action(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'action': message.text}
    bot.send_message(chat_id, "На любом этапе вы можете написать 'Выход' для удаления всего")
    if message.text == 'Отчет за мероприятие':
        bot.send_message(chat_id, "Введите ваше ФИО:")
        bot.register_next_step_handler(message, handle_report_fio)
    else:
        bot.send_message(chat_id, "Введите ваше ФИО:")
        bot.register_next_step_handler(message, handle_proposal_fio)


def handle_report_fio(message):
    chat_id = message.chat.id
    if message.content_type == "text":
        if message.text.lower() == 'выход':
            bot.send_message(chat_id, "Вы успешно вышли!")
            return
        user_data[chat_id]['fio'] = message.text
        bot.send_message(chat_id, "Введите название группы, которая принимала участие:")
        bot.register_next_step_handler(message, handle_report_group)
    else:
        bot.send_message(chat_id, "Введите ваше ФИО:")
        bot.register_next_step_handler(message, handle_report_fio)


def handle_report_group(message):
    chat_id = message.chat.id
    if message.content_type == "text":
        if message.text.lower() == 'выход':
            bot.send_message(chat_id, "Вы успешно вышли!")
            return
        user_data[chat_id]['group'] = message.text
        bot.send_message(chat_id, "Введите количество участников:")
        bot.register_next_step_handler(message, handle_report_participants)
    else:
        bot.send_message(chat_id, "Введите название группы, которая принимала участие:")
        bot.register_next_step_handler(message, handle_report_group)


def handle_report_participants(message):
    chat_id = message.chat.id
    if message.content_type == "text":
        if message.text.lower() == 'выход':
            bot.send_message(chat_id, "Вы успешно вышли!")
            return
        user_data[chat_id]['participants'] = message.text
        bot.send_message(chat_id, "Опишите, что было сделано:")
        bot.register_next_step_handler(message, handle_report_description)
    else:
        bot.send_message(chat_id, "Введите количество участников:")
        bot.register_next_step_handler(message, handle_report_participants)


def handle_report_description(message):
    chat_id = message.chat.id
    if message.content_type == "text":
        if message.text.lower() == 'выход':
            bot.send_message(chat_id, "Вы успешно вышли!")
            return
        user_data[chat_id]['description'] = message.text
        bot.send_message(chat_id, "Загрузите фото или видео. Уберите группировку перед отправкой. Когда закончите, "
                                  "отправьте 'Готово'.")
        bot.register_next_step_handler(message, handle_report_media)
    else:
        bot.send_message(chat_id, "Опишите, что было сделано:")
        bot.register_next_step_handler(message, handle_report_description)


def handle_report_media(message):
    chat_id = message.chat.id
    if message.content_type in ['photo', 'video']:
        media = user_data[chat_id].get('media', [])
        media.append(message)
        user_data[chat_id]['media'] = media
        bot.send_message(chat_id, "Фото/видео получено. Добавьте еще или отправьте 'Готово'.")
        bot.register_next_step_handler(message, handle_report_media)
    elif message.content_type == 'text':
        if message.text.lower() == 'готово':
            send_report(chat_id)
        if message.text.lower() == 'выход':
            bot.send_message(chat_id, "Вы успешно вышли!")
            return
    else:
        bot.send_message(chat_id, "Пожалуйста, загрузите фото или видео, либо отправьте 'Готово', когда закончите.")
        bot.register_next_step_handler(message, handle_report_media)


def handle_proposal_fio(message):
    chat_id = message.chat.id
    if message.content_type == "text":
        if message.text.lower() == 'выход':
            bot.send_message(chat_id, "Вы успешно вышли!")
            return
        user_data[chat_id]['fio'] = message.text
        bot.send_message(chat_id, "Введите дату проведения мероприятия:")
        bot.register_next_step_handler(message, handle_proposal_date)
    else:
        bot.send_message(chat_id, "Введите ваше ФИО:")
        bot.register_next_step_handler(message, handle_proposal_fio)


def handle_proposal_date(message):
    chat_id = message.chat.id
    if message.content_type == "text":
        if message.text.lower() == 'выход':
            bot.send_message(chat_id, "Вы успешно вышли!")
            return
        user_data[chat_id]['date'] = message.text
        bot.send_message(chat_id, "Опишите, что бы вы хотели сделать:")
        bot.register_next_step_handler(message, handle_proposal_description)
    else:
        bot.send_message(chat_id, "Введите дату проведения мероприятия:")
        bot.register_next_step_handler(message, handle_proposal_date)


def handle_proposal_description(message):
    chat_id = message.chat.id
    if message.content_type == "text":
        if message.text.lower() == 'выход':
            bot.send_message(chat_id, "Вы успешно вышли!")
            return
        user_data[chat_id]['description'] = message.text
        bot.send_message(chat_id, "Загрузите фото. Уберите группировку перед отправкой. Когда закончите, отправьте "
                                  "'Готово'.")
        bot.register_next_step_handler(message, handle_proposal_photo)
    else:
        bot.send_message(chat_id, "Опишите, что бы вы хотели сделать:")
        bot.register_next_step_handler(message, handle_proposal_description)


def handle_proposal_photo(message):
    chat_id = message.chat.id
    if message.content_type == 'photo':
        photos = user_data[chat_id].get('photos', [])
        photos.append(message.photo[-1].file_id)
        user_data[chat_id]['photos'] = photos
        bot.send_message(chat_id, "Фото получено. Добавьте еще или отправьте 'Готово'.")
        bot.register_next_step_handler(message, handle_proposal_photo)
    elif message.content_type == 'text':
        if message.text.lower() == 'готово':
            send_proposal(chat_id)
        if message.text.lower() == 'выход':
            bot.send_message(chat_id, "Вы успешно вышли!")
            return
    else:
        bot.send_message(chat_id, "Пожалуйста, загрузите фото или отправьте 'Готово', когда закончите.")
        bot.register_next_step_handler(message, handle_proposal_photo)


def send_report(chat_id):
    data = user_data[chat_id]
    text = (f"Отчет за мероприятие\nФИО: {data['fio']}\nГруппа: {data['group']}\nУчастники: {data['participants']}"
            f"\nОписание: {data['description']}")

    media_group = []
    for media in data.get('media', []):
        if media.content_type == 'photo':
            media_group.append(
                types.InputMediaPhoto(media.photo[-1].file_id, caption=text if len(media_group) == 0 else ""))
        elif media.content_type == 'video':
            media_group.append(
                types.InputMediaVideo(media.video.file_id, caption=text if len(media_group) == 0 else ""))

    if media_group:
        bot.send_media_group(ADMIN_ID, media_group)
        bot.send_media_group(ADMIN_ID2, media_group)
    else:
        bot.send_message(ADMIN_ID, text)
        bot.send_message(ADMIN_ID2, text)

    bot.send_message(chat_id, "Отчет отправлен!")
    user_data.pop(chat_id)


def send_proposal(chat_id):
    data = user_data[chat_id]
    text = f"Предложение мероприятия\nФИО: {data['fio']}\nДата: {data['date']}\nОписание: {data['description']}"

    media_group = [types.InputMediaPhoto(photo_id, caption=text if i == 0 else "") for i, photo_id in
                   enumerate(data.get('photos', []))]

    if media_group:
        bot.send_media_group(ADMIN_ID, media_group)
        bot.send_media_group(ADMIN_ID2, media_group)
    else:
        bot.send_message(ADMIN_ID, text)
        bot.send_message(ADMIN_ID2, text)

    bot.send_message(chat_id, "Предложение отправлено!")
    user_data.pop(chat_id)


bot.polling()
