from utils.update import update_repo, get_last_commit, get_url_for_hash, get_commit_by_hash
from utils.message import error_embed, success_embed
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
        description = description.replace(title + "\n", "")
        if description.startswith("\n"):
            description = description[1:]
        if description.endswith("\n"):
            description = description[:-1]
            
        author = commit.author.name
        timestamp = int(commit.committed_date)
        link = get_url_for_hash(commit.hexsha, ets2la_asset)
        commit_hash = commit.hexsha[:9]
        changed_files = commit.stats.files

        if self.channel:
            message = f"### Title\n"
            message += f"{title}\n\n"
            if description:
                message += f"**Description**\n{description}\n\n"
            message += f"**Changes**\n"
            message += f"-# [View detailed information](<{link}>)\n"
            message += f"```diff\n"
            if len(changed_files) < 8:
                for file, stats in changed_files.items():
                    message += f"=== {file} ===\n"
                    if stats['insertions'] > 0:
                        message += f"+ {stats['insertions']} lines\n"
                    if stats['deletions'] > 0:
                        message += f"- {stats['deletions']} lines\n"
                    message += "\n"
            else:
                insertions = sum(stats['insertions'] for stats in changed_files.values())
                deletions = sum(stats['deletions'] for stats in changed_files.values())
                message += f"... {len(changed_files)} files changed ...\n"
                message += f"+ {insertions} lines\n"
                message += f"- {deletions} lines\n"
                    
            message += "```\n\n"
            message += f"-# Commit **{commit_hash}** by **{author}** on <t:{timestamp}>"
            
            await self.channel.send(message)

    @commands.command()
    async def latest_update(self, ctx: commands.Context):
        author = ctx.author
        if author.id not in variables.ENV.ADMINS:
            await ctx.send(embed=error_embed("You do not have permission to run this command."))
            return
        
        last_commit = get_last_commit(ets2la_asset)
        if last_commit:
            await self.send_update_message(last_commit)
        else:
            await ctx.send(embed=error_embed("No commits found."))
            
    @commands.command()
    async def send_commit(self, ctx: commands.Context, hash: str):
        author = ctx.author
        if author.id not in variables.ENV.ADMINS:
            await ctx.send(embed=error_embed("You do not have permission to run this command."))
            return
        if not hash:
            await ctx.send(embed=error_embed("Please provide a commit hash."))
            return
        
        commit = get_commit_by_hash(hash, ets2la_asset)
        if commit:
            await self.send_update_message(commit)
        else:
            await ctx.send(embed=error_embed("No commit found with the specified hash."))

    @tasks.loop(minutes=1)
    async def update_repo_task(self):
        try:
            updated = await update_repo(ets2la_asset)
            if updated:
                last_commit = get_last_commit(ets2la_asset)
                if last_commit:
                    await self.send_update_message(last_commit)
        except:
            pass

async def setup(bot: commands.Bot):
    await bot.add_cog(update_watcher(bot))