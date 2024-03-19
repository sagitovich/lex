import csv
from telethon.sync import TelegramClient  # подключаться к клиенту мессенджера и работать с ним
from telethon.tl.types import InputPeerEmpty
from telethon.tl.functions.messages import GetDialogsRequest  # функция, позволяющая работать с сообщениями в чате

