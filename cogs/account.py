from utils.message import success_embed, error_embed
from discord.ext import commands
import datetime
import requests
import discord
import logging

logger = logging.getLogger()
url = "https://api.ets2la.com/tracking/time/{}"

class account(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def account(self, ctx: commands.Context, member: discord.Member = None):
        """
        Display user account information.
        """
        if member is None:
            member = ctx.author
            
        target = url.format(member.id)
        try:
            response = requests.get(target, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            await ctx.send(embed=error_embed(f"Failed to fetch account information. Please try again later.\n> {e}"))
            logger.error(f"Error fetching account info for {member.id}: {e}")
            return
        
        logging.info(f"Fetched account info for {member.id}: {data}")
        time = data.get("data", {}).get("time_used", 0)
        hours = time // 3600
        minutes = (time % 3600) // 60
        
        text = ""
        if hours > 0:
            text += f"{round(hours)} hours"
        if minutes > 0:
            if text:
                text += " and "
            text += f"{round(minutes)} minutes"
            
        if not text:
            text = "No information / account not found."
            
        await ctx.send(embed=success_embed(
            "This is how long you've used ETS2LA for.",
            text
        ))


async def setup(bot: commands.Bot):
    await bot.add_cog(account(bot))