from discord.ext import *
import discord

INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.presences = True
INTENTS.members = True