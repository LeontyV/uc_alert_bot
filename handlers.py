from main import bot, dp
from aiogram import types
from config import admin_id, accepted_chats, accepted_users
from crl import *
from time import sleep


# global


async def send_to_admin(*args):
	await bot.send_message(chat_id=admin_id, text="Бот запущен: " + bot._me.username)


"""
Тут часть обработчиков чата бота
"""


@dp.message_handler(regexp='/[Hh]elp')
async def help_commands(message: types.Message):
	print(message['from'].id)
	username = message.chat.username
	if (message.chat.username in accepted_users):
		answer = 'Список доступных команд:\n/crl - выводит список CRL УЦ ГАУ РК "ЦИТ"\n/Test - выводит Ваш ник и чат ID'
		#chat = bot.get_chat(message.chat.id)
		#await bot.send_message(chat_id=chat.id, text=str(chat.id))
		await message.answer(answer)
	print('Запрос делал user={} id={}, через чат={}'.format(username, message['from'].id, message['chat'].id))


@dp.message_handler(regexp='/[Tt]est')
async def echo_message(message: types.Message):
	username = message.chat.username
	if (message.chat.username in accepted_users):
		answer = 'Ваш ник: ' + message['from'].username + '\nЧат ID: ' + str(message.chat.id)
	#chat = bot.get_chat(message.chat.id)
	#await bot.send_message(chat_id=chat.id, text=str(chat.id))
	await message.answer(answer)
	print('Запрос делал user={} id={}, через чат={}'.format(username, message['from'].id, message['chat'].id))


@dp.message_handler(regexp='/crl')
async def print_crl(message: types.Message):
	username = message.chat.username
	if (message.chat.username in accepted_users):
		answer = await crl_to_tlgrm()
	for crl in answer.values():
		if 'ALERT' in crl:
			await message.answer(f'<b>{crl}</b>', parse_mode='HTML')
		elif crl == '':
			await message.answer(f'404 файл не найден!!!', parse_mode='HTML')
		else:
			await message.answer(f'<i>{crl}</i>', parse_mode='HTML')
		
	print('Запрос делал user={} id={}, через чат={}'.format(username, message['from'].id, message['chat'].id))
	

"""
Тут часть обработчиков канала чата
"""

@dp.channel_post_handler(regexp='/[Tt]est')
async def echo_message(message: types.Message):
	username = message.chat.username
	if (message.chat.title in accepted_chats):
		answer = 'Ваш ник: ' + message.author_signature + '\nЧат ID: ' + str(message.chat)
		await message.answer(answer)
	print('Запрос делал user={} id={}, через чат={}'.format(username, message['from'].id, message['chat'].id))
