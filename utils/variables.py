from types import SimpleNamespace
from utils.classes import Asset
from discord import Intents
import os

_env_data = open(".env", "r").readlines()
_env_data = [x.strip() for x in _env_data]

_env_dictionary = {}
for i in _env_data:
    key = i.split("=")[0]
    value = i.replace(i.split("=")[0] + "=", "")
    if "," in value: # Support lists
        value = [x.strip() for x in value.split(",")]
        for i, val in enumerate(value):
            try: # Try to convert to int
                value[i] = int(val)
            except ValueError:
                pass
    
    try: # Try to convert to int
        if type(value) == str:
            value = int(value)
    except ValueError:
        pass
    
    _env_dictionary[key] = value

ENV = SimpleNamespace(**_env_dictionary)
"""Enviroment variables."""
ENV.ADMINS = [ENV.ADMINS] if isinstance(ENV.ADMINS, int) else ENV.ADMINS
"""Explicitly ensure that ENV.ADMINS is a list."""

# General constants
PREFIX: str = "!"
"""The prefix for commands."""
LOGGER_NAME: str = "bot"
"""The name of the logging instance."""
UMAMI_API = "https://umami.ets2la.com/api"
"""Unami stats API endpoint"""
#TRANSLATION_UPDATE_CHANNEL = 1381627489574453258
TRANSLATION_UPDATE_CHANNEL = 1272294263874654240
"""The channel to send translation updates to."""
#UPDATE_CHANNEL = 1076428588523466813
UPDATE_CHANNEL = 1120734880133820537
"""The channel to send updates to."""

# Paths
PATH = os.path.dirname(os.path.dirname(__file__))
"""Root of the filesystem"""
LOG_FILE = os.path.join(PATH, "bot.log")
"""The path to the log file."""
ASSETS_FOLDER = os.path.join(PATH, "Assets")
"""The path where assets are stored."""
VERIFIED_USERS_FILE = os.path.join(PATH, "Assets", "verified.txt")
ASSET_URLS : list[Asset] = [
    Asset(
        "ETS2LA", 
        "https://github.com/ETS2LA/Euro-Truck-Simulator-2-Lane-Assist", 
        ASSETS_FOLDER,
        "--depth=20 --single-branch"
    ),
    Asset(
        "Translations", 
        "https://github.com/ETS2LA/translations", 
        ASSETS_FOLDER
    )
]
"""Defintion of assets and their URLs."""

# Discord config
INTENTS = Intents.default()
INTENTS.message_content = True
INTENTS.presences = True
INTENTS.members = True
"""Intent config for discordpy bot."""