import utils.classes as classes
from utils.update import *
from utils.message import *

from discord.ext import commands, tasks
import datetime
import discord
import yaml
import sys
import os

translations_repo = classes.get_asset_with_name("translations", variables.ASSET_URLS).path
class translation(commands.Cog):
    keys = None
    
    @tasks.loop(minutes=10)
    async def update_repo_task(self):
        await update_repo("translations")
        
        files = os.listdir(translations_repo)
        
        self.old_keys = self.keys
        self.languages = []
        self.keys = []
        self.translations = {}
        for file in files:
            if file.endswith(".yaml"):
                if not file.startswith("keys"):
                    with open(f"{translations_repo}/{file}", "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                        self.translations[data["Language"]["name_en"]] = data["Translations"]
                        self.languages.append(data["Language"])
                else:
                    with open(f"{translations_repo}/{file}", "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                        self.keys = data
            
        if self.old_keys and self.old_keys != self.keys:
            new_keys = [key for key in self.keys if key not in self.old_keys]
            removed_keys = [key for key in self.old_keys if key not in self.keys]
            messages = []
            messages.append("<@&1271896625438003320>" + f"\n-# Update found on <t:{int(datetime.datetime.now().timestamp())}>")
            
            if new_keys:
                message = "### New keys found.\nThese are translations that haven't been in the app before.\n\n"
                message += "```diff\n"
                for key in new_keys:
                    message += f"+ {key}\n"
                message += "```"
                messages.append(message)
            if removed_keys:
                message = "### Removed keys found.\nThese are translations that have been removed from the app.\n\n"
                message += "```diff\n"
                for key in removed_keys:
                    message += f"- {key}\n"
                message += "```"
                messages.append(message)
                
            if new_keys or removed_keys:
                for message in messages:
                    await self.bot.get_channel(variables.TRANSLATION_UPDATE_CHANNEL).send(message)
    
    def __init__(self, bot):
        print("- Translations initialized")
        self.bot = bot
        self.update_repo_task.start()
        print("- Started translation update task")

    async def list(self, ctx: commands.Context, type: str):
        if type == "languages":
            languages = ""
            for language in self.languages:
                languages += f"- {language['name_en']} ({language['iso_code']})\n"
            await ctx.send(embed=info_embed("Available languages", languages))
        elif type == "keys":
            keys_text = "Unfortunately there are too many keys to list here. \
                        We've attached the `keys.yaml` file for you to download and view."
            await ctx.send(embed=info_embed("Available keys", keys_text), file=discord.File(f"{translations_repo}/keys.yaml"))
        else:
            await ctx.send(embed=error_embed("Invalid type provided, please use either `languages` or `keys`"))

    async def status(self, ctx: commands.Context, language: str):
        if not language or language == "":
            await ctx.send(embed=error_embed("Please provide a language to lookup"))
            return
            
        if language not in self.translations and language != "all":
            await ctx.send(embed=error_embed("The specified language was not found"))
            return
        
        languages = self.translations.keys() if language == "all" else [language]
        
        embeds = []
        for language in languages:
            total_keys = len(self.keys) - 5 # Remove the language keys
            extra_keys = 0
            keys_found = 0
            for key in self.translations[language]:
                if key in self.keys:
                    keys_found += 1
                else:
                    extra_keys += 1
            
            description = f"**Total keys:** {total_keys}\n"
            description += f"**Keys translated:** {keys_found}/{total_keys} ({round(keys_found / total_keys * 100, 1)}%)\n"
            description += f"**Extra keys:** {extra_keys}"
            embed = success_embed(description, f"{language}")
            embeds.append(embed)
            
        await ctx.send(embeds=embeds)

    async def translate(self, ctx: commands.Context, language: str, key: str):
        if not language or language == "":
            await ctx.send(embed=error_embed("Please provide a language to translate to"))
            
        if not key or key == "":
            await ctx.send(embed=error_embed("Please provide a key to translate"))
            
        if language not in self.translations:
            await ctx.send(embed=error_embed("The specified language was not found"))
            return
        
        if key not in self.keys:
            await ctx.send(embed=error_embed("The specified key was not found"))
            return
        
        english = self.translations["English"][key]
        translation = self.translations[language][key]
        await ctx.send(embed=success_embed(f"Translation for `{english}` in `{language}`", translation))

    @commands.command(name="translation")
    async def translation(self, ctx: commands.Context, command: str = None, *args):
        if not command or command == "":
            await ctx.send(embed=error_embed("Please provide a command to lookup (use `help` for a list)"))
            return
        
        if command == "help":
            available_commands = "- `help` - Show this message\n"
            available_commands += "- `list { languages OR keys }` - List all available languages or keys\n"
            available_commands += "- `status { language_en OR all }` - Get the translation status of a language (or all of them)\n"
            available_commands += "- `translate {language_en} {key}` - Translate a key to a language\n"
            await ctx.send(embed=info_embed("Available commands", available_commands))
            return
        
        if command == "list":
            await self.list(ctx, args[0] if len(args) > 0 else "")
            
        if command == "status":
            await self.status(ctx, " ".join(args))
            
        if command == "translate":
            await self.translate(ctx, args[0], args[1])

async def setup(bot: commands.Bot):
    await bot.add_cog(translation(bot))