from Source.TeleBotAdminPanel import Panel, Modules
from Source.Functions import SendStub

from dublib.Methods.System import CheckPythonMinimalVersion
from dublib.TelebotUtils.Cache import TeleCache
from dublib.Engine.Configurator import Config
from dublib.TelebotUtils import UsersManager
from dublib.TelebotUtils import TeleMaster
from dublib.Methods.Data import Zerotify

from telebot import types

#==========================================================================================#
# >>>>> ИНИЦИАЛИЗАЦИЯ <<<<< #
#==========================================================================================#

CheckPythonMinimalVersion(3, 10)

Settings = Config("Settings.json")
Settings.load()
MasterBot = TeleMaster(Settings["bot_token"])
Bot = MasterBot.bot
Manager = UsersManager("Data/Users", threads = Settings["users_manager_threads"])
Cacher = TeleCache()
Cacher.set_bot(Bot)
Cacher.set_chat_id(Settings["cacher_chat_id"])

#==========================================================================================#
# >>>>> НАСТРОЙКА ПАНЕЛИ УПРАВЛЕНИЯ <<<<< #
#==========================================================================================#

AdminPanel = Panel(Bot, Manager, Settings["password"])

TBAP_TREE = {
	"📊 Статистика": Modules.SM_Statistics,
	"✉️ Рассылка": Modules.SM_Mailing,
	"❌ Закрыть": Modules.SM_Close
}

AdminPanel.set_tree(TBAP_TREE)

#==========================================================================================#
# >>>>> ОБРАБОТКА СОБЫТИЙ <<<<< #
#==========================================================================================#

@Bot.message_handler(commands = ["admin"])
def Command(Message: types.Message):
	User = Manager.auth(Message.from_user)
	Password = Message.text.split(" ")[1:]
	Password = " ".join(Password).strip()
	Password = Zerotify(Password)

	if not AdminPanel.login(User, Password): Bot.send_message(User.id, "Доступ запрещён.")
	else: Bot.send_message(User.id, "Панель управления открыта.", reply_markup = AdminPanel.open(User))

@Bot.message_handler(content_types = ["text"])
def TextHandler(message: types.Message):
	User = Manager.auth(message.from_user)
	if AdminPanel.procedures.text(message): return
	SendStub(Settings, Cacher, Bot, User)

AdminPanel.decorators.inline_keyboards()

@Bot.callback_query_handler()
def CallbackHandler(call: types.CallbackQuery):
	User = Manager.auth(call.message.from_user)
	Bot.answer_callback_query(call.id)
	SendStub(Settings, Cacher, Bot, User)

@Bot.message_handler(content_types = ["animation", "audio", "document", "photo", "video"])
def AttachmentHandler(Message: types.Message):
	User = Manager.auth(Message.from_user)
	if AdminPanel.procedures.attachments(Message): return
	SendStub(Settings, Cacher, Bot, User)

Bot.infinity_polling()