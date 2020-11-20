import asyncio

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN, PROXY, admin_id, uc_chat_id
from crl import *


DELAY = 24*3600

loop = asyncio.get_event_loop()
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage, loop=loop)


async def schedule(wait_time):
	while True:
		answer = await crl_to_tlgrm()
		for crl in answer.values():
			if 'ALERT' in crl:
				await bot.send_message(chat_id=uc_chat_id, text=f'<b>{crl}</b>', parse_mode='HTML')
			elif crl == '':
				await bot.send_message(chat_id=uc_chat_id, text=f'404 файл не найден!!!', parse_mode='HTML')
			else:
				await bot.send_message(chat_id=uc_chat_id, text=f'<b>{crl}</b>', parse_mode='HTML')
		await asyncio.sleep(wait_time)

	
if __name__ == '__main__':
	from handlers import *
	loop.create_task(schedule(DELAY)) # в идеале 3600
	executor.start_polling(dp, on_startup=send_to_admin, loop=loop)
	
