from discord.ext import commands
import datetime
import discord

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context, member: discord.Member = None):
        if member is None:
            member = ctx.author
        
        time = datetime.datetime.now() - ctx.message.created_at.replace(tzinfo=None)
        await ctx.send(f"pong!\n-# in {time.microseconds / 1000:.0f}ms")

async def setup(bot: commands.Bot):
    await bot.add_cog(ping(bot))