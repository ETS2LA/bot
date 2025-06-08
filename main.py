from utils.message import error_embed, success_embed, cooldown_embed, info_embed
from utils.logger import setup_logger
from utils.update import update_repo
import utils.variables as variables

from discord.ext import commands

logger = setup_logger()
bot = commands.Bot(
    command_prefix=variables.PREFIX, 
    intents=variables.INTENTS
)
cogs = [
    "ping",
    "version",
    "stats",
    "translation",
    "xdd",
    "update_watcher",
    "verify",
]

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user}")
    for cog in cogs:
        try:
            await bot.load_extension(f"cogs.{cog}")
            logger.info(f"- Loaded {cog}")
        except Exception as e:
            logger.error(f"- Failed to load {cog}: {e}")
    
@bot.event
async def on_command_error(ctx, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed=error_embed("The specified command was not found."))
    elif isinstance(error, commands.CommandOnCooldown):
        await cooldown_embed(ctx, error)
    else:
        await ctx.send(embed=error_embed(f"The command ran into an error.\n```{error}```"))
        
@bot.command("update")
async def update_repo_command(ctx: commands.Context, repo: str):
    author = ctx.author
    if author.id not in variables.ENV.ADMINS:
        await ctx.send(embed=error_embed("You do not have permission to run this command."))
        return
    
    message = await ctx.send(embed=info_embed(f"Updating {repo}", "This may take a while."))
    await update_repo(repo)
    await message.edit(embed=success_embed(f"{repo} has been updated to the newest version on github."))
    
@bot.command("reload")
async def reload(ctx: commands.Context, *target_cogs):
    author = ctx.author
    if author.id not in variables.ENV.ADMINS:
        await ctx.send(embed=error_embed("You do not have permission to run this command."))
        return
    
    i = 0
    embeds = []
    message = None
    for cog in cogs if not target_cogs else target_cogs:
        embeds.append(info_embed("Reloading", f"Reloading `{cog}` ({i + 1}/{len(cogs)})"))
        i += 1
    
    message = await ctx.send(embeds=embeds)
        
    i = 0
    for cog in cogs if not target_cogs else target_cogs:
        try:
            await bot.reload_extension(f"cogs.{cog}")
            embeds[i] = success_embed(f"Reloaded `{cog}` ({i + 1}/{len(cogs)})")
            await message.edit(embeds=embeds)
        except Exception as e:
            embeds[i] = error_embed(f"Failed to reload `{cog}` ({i + 1}/{len(cogs)})\n```{e}```")
            await message.edit(embeds=embeds)
        i += 1

bot.run(variables.ENV.CLIENT_TOKEN)