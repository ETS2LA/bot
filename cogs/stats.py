from utils.message import success_embed, error_embed, cooldown_embed
from utils.secrets import UMAMI_LOGIN, UMAMI_PASSWORD, UMAMI_ID
from discord.ext import commands
import requests
import datetime
import discord

endpoint = "https://umami.ets2la.com/api"
website_endpoint = endpoint + "/websites/" + UMAMI_ID

class stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token = None
        self.login()

    def active_users(self):
        response = requests.get(f"{website_endpoint}/active", headers={
            "Authorization": f"Bearer {self.token}"
        })
        return response.json()["x"]

    def get_stats(self):
        url = f"{website_endpoint}/stats"
        url += "?startAt=" + str(int(datetime.datetime.now().timestamp() * 1000) - 86400000)
        url += "&endAt=" + str(int(datetime.datetime.now().timestamp() * 1000))
        url += "&unit=hour&timezone=Europe%2FHelsinki&compare=false"
        
        response = requests.get(url, 
            headers={
                "Authorization": f"Bearer {self.token}"
            }
        )
        try:
            return response.json()
        except:
            return response.text
    
    def login(self):
        if self.token is not None:
            return
        
        response = requests.post(f"{endpoint}/auth/login", data={
            "username": UMAMI_LOGIN, 
            "password": UMAMI_PASSWORD
        })
        self.token = response.json()["token"]

    @commands.command("stats")
    @commands.cooldown(1, 60, commands.BucketType.channel)
    async def stats(self, ctx: commands.Context, member: discord.Member = None):
        if member is None:
            member = ctx.author
        
        active_users = self.active_users()
        
        stats = self.get_stats()
        if type(stats) != dict:
            await ctx.send(embed=error_embed(f"Something went wrong while fetching the stats.\n```{stats}```"))
            return
        
        pageviews = stats["pageviews"]["value"]
        visitors = stats["visitors"]["value"]
        visits = stats["visits"]["value"]
        bounces = stats["bounces"]["value"]
        bounce_rate = bounces / visits * 100
        total_time = stats["totaltime"]["value"] / 60 / 60
        
        title = f"{active_users} currently active users"
        
        description = "Stats for the last 24 hours:\n"
        description += f"- Pageviews: {pageviews}\n"
        description += f"- Visitors: {visitors}\n"
        description += f"- Visits: {visits}\n"
        description += f"- Bounces: {bounces}\n"
        description += f"- Bounce rate: {bounce_rate:.2f}%\n"
        description += f"- Total time: {total_time:.0f} hours"
        
        await ctx.send(embed=success_embed(description, title))

async def setup(bot: commands.Bot):
    await bot.add_cog(stats(bot))