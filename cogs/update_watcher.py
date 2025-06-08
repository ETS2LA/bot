from utils.update import update_repo, get_last_commit, get_url_for_hash
import utils.variables as variables
import utils.classes as classes

from discord.ext import commands, tasks
import datetime
import discord

ets2la_asset = classes.get_asset_with_name("ets2la", variables.ASSET_URLS)
class update_watcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_repo_task.start()

    @tasks.loop(minutes=1)
    async def update_repo_task(self):
        updated = await update_repo(ets2la_asset)
        print(updated)
        
        if updated:
            last_commit = get_last_commit(ets2la_asset)
            if last_commit:
                title = last_commit.summary
                if title.startswith("\n"):
                    title = title[1:]
                if title.endswith("\n"):
                    title = title[:-1]
                
                description = last_commit.message.replace(title + "\n\n", "")
                if description.startswith("\n"):
                    description = description[1:]
                if description.endswith("\n"):
                    description = description[:-1]
                    
                author = last_commit.author.name
                timestamp = int(last_commit.committed_date)
                link = get_url_for_hash(last_commit.hexsha, "ets2la")
                commit_hash = last_commit.hexsha[:9]
                added_lines = last_commit.stats.total['insertions']
                removed_lines = last_commit.stats.total['deletions']
                
                channel = self.bot.get_channel(variables.UPDATE_CHANNEL)
                if channel:
                    message = f"### Title\n"
                    message += f"{title}\n\n"
                    message += f"**Description**\n{description}\n\n"
                    message += f"**Changes**\n"
                    message += f"-# [View detailed information](<{link}>)\n"
                    message += f"```\n"
                    message += f"+ {added_lines} additions\n"
                    message += f"- {removed_lines} deletions\n"
                    message += "```\n\n"
                    message += f"-# Commit **{commit_hash}** by **{author}** on <t:{timestamp}>"
                    
                    await channel.send(message)


    @commands.command()
    async def update_watcher(self, ctx: commands.Context, member: discord.Member = None):
        last_commit = get_last_commit(ets2la_asset)
        if last_commit:
            title = last_commit.summary
            if title.startswith("\n"):
                title = title[1:]
            if title.endswith("\n"):
                title = title[:-1]
            
            description = last_commit.message.replace(title + "\n\n", "").replace(title, "").strip()
            description.replace("\\n", "\n")
            if description.startswith("\n"):
                description = description[1:]
            if description.endswith("\n"):
                description = description[:-1]
                
            has_description = description != ""
                
            author = last_commit.author.name
            timestamp = int(last_commit.committed_date)
            link = get_url_for_hash(last_commit.hexsha, "ets2la")
            added_lines = last_commit.stats.total['insertions']
            removed_lines = last_commit.stats.total['deletions']
            
            channel = self.bot.get_channel(variables.UPDATE_CHANNEL)
            if channel:
                message = f"**Title**\n"
                message += f"{title}\n\n"
                if has_description:
                    message += f"**Description**\n{description}\n\n"
                message += f"**Changes**\n"
                message += f"-# [View detailed information](<{link}>)\n"
                message += f"```\n"
                message += f"+ {added_lines} additions\n"
                message += f"- {removed_lines} deletions\n"
                message += "```\n\n"
                message += f"-# Commit by **{author}** on <t:{timestamp}>"
                
                await channel.send(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(update_watcher(bot))