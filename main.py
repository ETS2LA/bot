from utils.message import error_embed, success_embed
from utils.ets2la import update_ets2la
from utils.secrets import CLIENT_TOKEN
from utils.config import INTENTS

from discord.ext import commands
import discord

import traceback
import asyncio

bot = commands.Bot(command_prefix="!", intents=INTENTS)

cogs = [
    "ping",
    "version",
    "xdd"
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    for cog in cogs:
        await bot.load_extension(f"cogs.{cog}")
        print(f"Loaded {cog}")
        
    bot.loop.create_task(update_ets2la_task())
    
@bot.event
async def on_command_error(ctx, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed=error_embed("The specified command was not found."))
    else:
        await ctx.send(embed=error_embed(f"The command ran into an error.\n```{error}```"))
    
async def update_ets2la_task():
    await bot.wait_until_ready()
    print("Started ETS2LA update task")
    while not bot.is_closed():
        await update_ets2la()
        await asyncio.sleep(300) # 5 minutes
    
@bot.command("reload")
async def reload(ctx):
    i = 0
    for cog in cogs:
        try:
            await bot.reload_extension(f"cogs.{cog}")
            await ctx.send(embed=success_embed(f"Reloaded `{cog}` ({i+1}/{len(cogs)})"))
        except:
            await ctx.send(embed=error_embed(f"Failed to reload `{cog}` ({i+1}/{len(cogs)})\n```{traceback.format_exc()}```"))
            
        i += 1

bot.run(CLIENT_TOKEN)