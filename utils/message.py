from discord.ext import commands
import discord
import time

def error_embed(description: str, title: str = "Error"):
    embed = discord.Embed(title=title, description=description, color=discord.Color.red())
    return embed

def success_embed(description: str, title: str = "Success"):
    embed = discord.Embed(title=title, description=description, color=discord.Color.green())
    return embed

def info_embed(title: str, description: str):
    embed = discord.Embed(title=title, description=description, color=discord.Color.blue())
    return embed

async def cooldown_embed(ctx: commands.Context, retry_after: float, delete_original: bool = True):
    if delete_original:
        await ctx.message.delete()
    
    timestamp = time.time() + retry_after + 1
    embed = discord.Embed(title="Cooldown", description=f"You can use the command again <t:{round(timestamp)}:R>.\nThis message will delete itself once the cooldown has passed.", color=discord.Color.yellow())
    await ctx.send(embed=embed, delete_after=retry_after)