from utils.update import update_repo, get_last_commit, get_url_for_hash
import utils.variables as variables
import utils.classes as classes

from discord.ext import commands, tasks
import logging
import git

logger = logging.getLogger()
ets2la_asset = classes.get_asset_with_name("ETS2LA", variables.ASSET_URLS)
class update_watcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_repo_task.start()
        self.channel = self.bot.get_channel(variables.UPDATE_CHANNEL)

    async def send_update_message(self, commit : git.Commit):
        title = commit.summary
        if title.startswith("\n"):
            title = title[1:]
        if title.endswith("\n"):
            title = title[:-1]

        description = commit.message.replace(title + "\n\n", "")
        if description.startswith("\n"):
            description = description[1:]
        if description.endswith("\n"):
            description = description[:-1]
            
        author = commit.author.name
        timestamp = int(commit.committed_date)
        link = get_url_for_hash(commit.hexsha, ets2la_asset)
        commit_hash = commit.hexsha[:9]
        added_lines = commit.stats.total['insertions']
        removed_lines = commit.stats.total['deletions']

        if self.channel:
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
            
            await self.channel.send(message)

    @tasks.loop(minutes=1)
    async def update_repo_task(self):
        updated = await update_repo(ets2la_asset)
        if updated:
            last_commit = get_last_commit(ets2la_asset)
            if last_commit:
                await self.send_update_message(last_commit)

async def setup(bot: commands.Bot):
    await bot.add_cog(update_watcher(bot))