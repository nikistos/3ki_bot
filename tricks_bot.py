import telebot
import db


TELEGRAM_API_KEY = '1913559958:AAH-BJrimcFszfxVYfInR1vttLdrPOWEzTY'
COMMAND_START = "/start"
COMMAND_LEADER_BOARD = "/leader_board"
COMMAND_ENABLE_BOT = "/start_suka"
COMMAND_DISABLE_BOT = "/stop_suka"

bot = telebot.TeleBot(TELEGRAM_API_KEY)
admins = [326664376, 959111044]


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(message)
    handle_message(message)


bot_enabled = True


def handle_message(message):
    global bot_enabled
    if message.text == COMMAND_START:
        register_user(
            username=message.from_user.username,
            user_id=message.from_user.id
        )

    elif message.text == COMMAND_ENABLE_BOT and message.from_user.id in admins:
        bot_enabled = True
        bot.send_message(chat_id=message.from_user.id, text="Да, босс, по коням!")

    elif message.text == COMMAND_DISABLE_BOT and message.from_user.id in admins:
        bot_enabled = False
        bot.send_message(chat_id=message.from_user.id, text="Отдыхаем мужики!")

    elif message.text == COMMAND_LEADER_BOARD:
        send_leader_board(user_id=message.from_user.id, sender_nick=message.from_user.username)

    elif not bot_enabled:
        bot.send_message(chat_id=message.from_user.id, text="Отдыхаем мужики!")

    else:
        register_code(
            username=message.from_user.username,
            code=message.text,
            user_id=message.from_user.id)


def send_leader_board(user_id, sender_nick):
    leaders = db.get_leader_board()
    print(leaders)
    message_to_send = '*Рейтинг игроков\n*'
    for score_record in leaders:
        is_current_user = score_record[0] == sender_nick
        username = f'@{score_record[0]}' if not score_record[0] == 'None' else 'Неизвестный гендер'
        scores = score_record[1]
        message_to_send = message_to_send + f'\n\n{username} - *{scores} qr*\n' \
            if is_current_user \
            else message_to_send + f'\n{username} - *{scores} qr*'
    print(message_to_send)
    bot.send_message(chat_id=user_id, text=message_to_send, parse_mode='Markdown')


def register_user(username, user_id):
    is_new_user = db.insert_user_if_not_exists(username, user_id)
    if is_new_user:
        bot.send_message(chat_id=user_id, text="Добрейший вечерочек! Салам пополам!", parse_mode='Markdown')
    else:
        bot.send_message(chat_id=user_id, text="Салам! Уже знакомы!", parse_mode='Markdown')


def register_code(username, code, user_id):
    if not db.check_code_is_valid(code):
        bot.send_message(chat_id=user_id, text="*Брат, нельзя так, нет такого кода, э!*", parse_mode='Markdown')
        return
    if db.has_user_code(user_id, code):
        bot.send_message(chat_id=user_id, text="Брат, куда шлешь, не видишь добавлен уже код!?", parse_mode='Markdown')
        return
    register = db.register_user_code(user_id, code)
    bot.send_message(chat_id=user_id, text=f'Класс!\nТвой результат: *{register}*', parse_mode='Markdown')


