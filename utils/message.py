from discord.ext import commands
import discord
import time

def error_embed(description: str, title: str = "Error") -> discord.Embed:
    embed = discord.Embed(title=title, description=description, color=discord.Color.red())
    return embed

def success_embed(description: str, title: str = "Success") -> discord.Embed:
    embed = discord.Embed(title=title, description=description, color=discord.Color.green())
    return embed

def info_embed(title: str, description: str) -> discord.Embed:
    embed = discord.Embed(title=title, description=description, color=discord.Color.blue())
    return embed

async def cooldown_embed(ctx: commands.Context, error: commands.CommandOnCooldown, delete_original: bool = True) -> None:
    if delete_original:
        await ctx.message.delete()
    
    actor = "You"
    if error.type == commands.BucketType.guild:
        actor = "This server"
    elif error.type == commands.BucketType.channel:
        actor = "This channel" 
    
    timestamp = time.time() + error.retry_after + 1
    embed = discord.Embed(title="Cooldown", description=f"{actor} can use `{ctx.command.name}` again after <t:{round(timestamp)}:R>.\nThis message will delete itself once the cooldown has passed.", color=discord.Color.yellow())
    await ctx.send(embed=embed, delete_after=error.retry_after)