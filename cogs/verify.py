from discord.ext import commands, tasks
from utils.message import error_embed, success_embed, cooldown_embed, info_embed
import datetime
import discord
import os

verified = []
file = "assets/verified.txt"
if os.path.exists(file):
    with open(file, "r") as f:
        verified = [int(line.strip()) for line in f.readlines()]
else:
    with open(file, "w") as f:
        f.write("")
        verified = []
        
def save_verified():    
    with open(file, "w") as f:
        for user in verified:
            f.write(f"{user}\n")

class verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.save_verified_task.start()

    @tasks.loop(minutes=1)
    async def save_verified_task(self):
        save_verified()

    def has_link(self, message):
        return any(link in message.content for link in ["https://", "http://", "www.", ".com", ".net", ".org"])
    
    def has_money(self, message):
        return any(symbol in message.content for symbol in ["$", "€", "£", "¥", "₹", "dollar"])
    
    def has_steam(self, message):
        return any(steam in message.content for steam in ["steam", "steamcommunity", "steampowered"])

    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        if author.id in verified or author.bot:
            return
        
        has_money = self.has_money(message)
        has_link = self.has_link(message)
        has_steam = self.has_steam(message)
        
        if has_money or has_link or has_steam:
            text = "<@&1132519946799284315> "
            text += "Please check the user manually. "
            text += "They were flagged because of:"
            if has_money:
                text += "\n- First message contains money related terms."
            if has_link:
                text += "\n- First message contains links."
            if has_steam:
                text += "\n- First message references *Steam*."
                
            await message.reply(embed=error_embed(text, title="Possible scammer detected"))
            await author.timeout(datetime.timedelta(days=1), reason="Possible scammer detected")
        else:
            await message.reply(embed=success_embed("Your first message indicates no signs of potential scamming.", title="Verified"), delete_after=5)
            verified.append(author.id)
        

async def setup(bot: commands.Bot):
    await bot.add_cog(verify(bot))