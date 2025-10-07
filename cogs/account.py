from utils.message import success_embed, error_embed
from discord.ext import commands
import matplotlib.pyplot as plt
import datetime
import requests
import discord
import logging
import os

logger = logging.getLogger()
tracking_url = "https://api.ets2la.com/tracking/time/{}"
sessions_url = "https://api.ets2la.com/tracking/sessions/{}"

class Session:
    start = None
    end = None
    def __init__(self, start: datetime.datetime, end: datetime.datetime):
        self.start = start
        self.end = end

class account(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def format_timedelta(self, td: datetime.timedelta, display_seconds=False) -> str:
        hours, remainder = divmod(td.seconds, 3600)
        hours += td.days * 24
        minutes, seconds = divmod(remainder, 60)
        parts = []
        if hours > 0:
            parts.append(f"{hours} hours")
        if minutes > 0:
            parts.append(f"{minutes} minutes")
        if seconds > 0 and display_seconds:
            parts.append(f"{seconds} seconds")
        return " and ".join(parts) if parts else "0 seconds"

    def get_response(self, url: str):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching data from {url}: {e}")
            return None

    @commands.command()
    async def account(self, ctx: commands.Context, member: discord.Member = None):
        """
        Display user account information.
        """
        if member is None:
            member = ctx.author
            
        try:
            tracking_data = self.get_response(tracking_url.format(member.id))
            sessions_data = self.get_response(sessions_url.format(member.id))
        except requests.RequestException as e:
            await ctx.send(embed=error_embed(f"Failed to fetch account information. Please try again later.\n> {e}"))
            logger.error(f"Error fetching account info for {member.id}: {e}")
            return

        time = tracking_data.get("data", {}).get("time_used", 0)
        text = self.format_timedelta(datetime.timedelta(seconds=time))
        if not text:
            text = "No information / account not found."
            
        sessions_count = tracking_data.get("data", {}).get("sessions", 0)
        if sessions_count <= 0:
            sessions_count = 1
            
        avg_time = time / sessions_count
        avg_text = self.format_timedelta(datetime.timedelta(seconds=avg_time), display_seconds=True)
        
        sessions = []
        for session in sessions_data.get("data", {}).get("sessions", []):
            start = float(session.get("start"))
            end = float(session.get("end"))
            if start and end:
                sessions.append(Session(
                    datetime.datetime.fromtimestamp(start),
                    datetime.datetime.fromtimestamp(end),
                ))
                
        longest_session = max(sessions, key=lambda s: (s.end - s.start).total_seconds(), default=None)
        if not longest_session:
            longest_text = "N/A"
        else:
            longest_duration = longest_session.end - longest_session.start
            longest_text = self.format_timedelta(longest_duration, display_seconds=True)
                
        await ctx.send(embed=success_embed(
            f"That is spread over {sessions_count} sessions, averaging {avg_text} per session. Your longest session was {longest_text} starting on {longest_session.start.strftime('%Y-%m-%d %H:%M:%S') if longest_session else 'N/A'}.",
            text
        ))
                
        if sessions:
            plt.figure(figsize=(10, 5), dpi=100)
            ax = plt.gca()
            plt.xlabel("Date", color="white")
            plt.ylabel("Hours", color="white")
            
            accumulated_time = 0
            session_dates = []
            accumulated_times = []

            for session in sessions:
                session_duration = (session.end - session.start).total_seconds()
                accumulated_time += session_duration
                session_dates.append(session.start)
                accumulated_times.append(accumulated_time / 3600)  # Convert to hours

            plt.plot(session_dates, accumulated_times, color="#5865F2", linewidth=2)
            plt.grid(True, color="#4f545c", alpha=0.3)
            
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            for spine in ax.spines.values():
                spine.set_color("#23272a")
            
            plot_filename = f"plot_{member.id}.png"
            plt.savefig(plot_filename, bbox_inches='tight', transparent=True)
            plt.close()
            
            with open(plot_filename, 'rb') as f:
                picture = discord.File(f)
                await ctx.send(file=picture)
                
            os.remove(plot_filename)



async def setup(bot: commands.Bot):
    await bot.add_cog(account(bot))