import discord
from discord.ext import commands, tasks
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

# Создаем экземпляр бота
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="/", intents=intents)


# Функция для чтения новостей из файла
def read_news_file():
    with open("news.txt", "r", encoding="utf-8") as f:
        news_lines = f.read().splitlines()  # Читаем файл и разбиваем строки на список
    news_topics = []
    current_topic = ""

    for line in news_lines:
        if line.strip():  # Если строка не пустая
            current_topic += " " + line.strip()  # Добавляем к текущей теме
        else:
            if current_topic:
                news_topics.append(current_topic.strip())  # Добавляем текущую тему в список
                current_topic = ""  # Сбрасываем текущую тему

    if current_topic:  # Добавляем последнюю тему, если она есть
        news_topics.append(current_topic.strip())

    return news_topics


# Команда /all_news
@client.command(name="all_news")
async def all_news(ctx):
    news_list = read_news_file()
    for news in news_list:
        await ctx.send(news,silent=True)
        await asyncio.sleep(1.5)  # Задержка между сообщениями 1.5 секунды


# Функция для отправки новостей через указанный интервал времени
@tasks.loop(minutes=5)  # Указываем интервал времени в минутах
async def send_news_periodically(channel_id):
    logging.info(f"Attempting to send news to channel {channel_id}...")
    channel = client.get_channel(channel_id)
    if channel is None:
        logging.error(f"Cannot find channel with ID {channel_id}")
        return

    news_list = read_news_file()
    if not news_list:
        logging.warning("News file is empty or could not be read.")
    for news in news_list:
        await channel.send(news.strip(),silent=True)
        await asyncio.sleep(1.5)  # Задержка между сообщениями 1.5 секунды


# Команда для запуска периодической отправки новостей
@client.command(name="start_news")
async def start_news(ctx, interval: int):
    send_news_periodically.change_interval(minutes=interval)
    send_news_periodically.start(ctx.channel.id)
    await ctx.send(f"Новости будут отправляться каждые {interval} минут.")
    logging.info(f"Started sending news every {interval} minutes to channel {ctx.channel.id}")


# Команда для остановки периодической отправки новостей
@client.command(name="stop_news")
async def stop_news(ctx):
    send_news_periodically.stop()
    await ctx.send("Периодическая отправка новостей остановлена.")
    logging.info(f"Stopped sending news to channel {ctx.channel.id}")


# Discord bot setup
TOKEN = 'YOUR_TOCEN'
# Запускаем бота
client.run(TOKEN)
