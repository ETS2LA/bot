from utils.message import cooldown_embed
from discord.ext import commands
import datetime
import discord

class xdd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def xdd(self, ctx: commands.Context, member: discord.Member = None):
        if member is None:
            member = ctx.author
        
        await ctx.send(f"<:xdx:1195115294696415352>")

async def setup(bot: commands.Bot):
    await bot.add_cog(xdd(bot))