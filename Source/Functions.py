from typing import TYPE_CHECKING

from telebot import TeleBot, types

if TYPE_CHECKING:
	from dublib.TelebotUtils import TeleCache, UserData
	from dublib.Engine.Configurator import Config

def SendStub(config: "Config", cacher: "TeleCache", bot: "TeleBot", user: "UserData") -> int | None:
	"""
	Отправляет сообщение заглушку.

	:param config: Глоабльные настройки.
	:type config: Config
	:param cacher: Менеджер кэша.
	:type cacher: TeleCache
	:param bot: Бот Telegram.
	:type bot: TeleBot
	:param user: Данные пользователя.
	:type user: UserData
	:return: ID отправленного сообщения или `None` в случае ошибки.
	:rtype: int | None
	"""

	MessageID = None

	if config["message"]["animation"]:
		bot.send_animation(
			chat_id = user.id,
			animation = cacher.get_real_cached_file(config["message"]["animation"], types.InputMediaAnimation).file_id,
			caption = "\n".join(config["message"]["text"]),
			parse_mode = "HTML"
		)

	else:
		bot.send_message(
			chat_id = user.id,
			text = "\n".join(config["message"]["text"]),
			parse_mode = "HTML"
		)

	return MessageID
