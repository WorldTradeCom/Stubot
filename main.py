from Source.Functions import SendStub

from dublib.TelebotUtils.Cache import TeleCache
from dublib.Methods.Filesystem import ReadJSON
from dublib.TelebotUtils import UsersManager
from dublib.TelebotUtils import TeleMaster
from dublib.Engine.Configurator import Config
from dublib.Methods.System import Clear

from telebot import types, TeleBot


Settings = Config("Settings.json")

MasterBot = TeleMaster(Settings["token"])
Bot = MasterBot.bot

Manager = UsersManager("Data/Users")
Cacher = TeleCache()
Cacher.set_bot(Bot)
Cacher.set_chat_id(Settings["chat_id"])

@Bot.message_handler()
def MessageHanler(message: types.Message):
	User = Manager.auth(message.from_user)
	SendStub(Settings, Cacher, Bot, User)

@Bot.callback_query_handler()
def CallbackQueryHandler(call: types.CallbackQuery):
	User = Manager.auth(call.message.from_user)
	Bot.answer_callback_query(call.id)
	SendStub(Settings, Cacher, Bot, User)