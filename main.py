import ptbot
import os
from dotenv import load_dotenv
from pytimeparse import parse


load_dotenv()
BOT = ptbot.Bot(os.getenv('TG_TOKEN'))


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify(chat_id):
    BOT.send_message(chat_id, 'Время вышло')


def notify_progress(secs_left, chat_id, message_id, timer_time):
    progress_message = f'Осталось {secs_left} секунд\n' + render_progressbar(timer_time, timer_time - secs_left)
    BOT.update_message(chat_id, message_id, progress_message)


def reply(chat_id, user_message):
    message_id = BOT.send_message(chat_id, f'Запускаю таймер:')
    BOT.create_countdown(
        parse(user_message), notify_progress, chat_id=chat_id,
        message_id=message_id, timer_time=parse(user_message)
    )
    BOT.create_timer(parse(user_message), notify, chat_id=chat_id)


def main():
    BOT.reply_on_message(reply)
    BOT.run_bot()


if __name__ == '__main__':
    main()