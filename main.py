import ptbot
import os
from dotenv import load_dotenv
from pytimeparse import parse


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify(chat_id, bot):
    bot.send_message(chat_id, 'Время вышло')


def notify_progress(secs_left, chat_id, message_id, timer_time, bot):
    progress_message = f'Осталось {secs_left} секунд\n' + render_progressbar(timer_time, timer_time - secs_left)
    bot.update_message(chat_id, message_id, progress_message)


def reply(chat_id, user_message, bot):
    message_id = bot.send_message(chat_id, f'Запускаю таймер:')
    bot.create_countdown(
        parse(user_message), notify_progress, chat_id=chat_id,
        message_id=message_id, timer_time=parse(user_message), bot=bot
    )
    bot.create_timer(parse(user_message), notify, chat_id=chat_id, bot=bot)


def main():
    load_dotenv()
    bot = ptbot.Bot(os.getenv('TG_TOKEN'))
    bot.reply_on_message(reply, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()