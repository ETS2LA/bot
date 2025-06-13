import utils.variables as variables
from discord.ext import commands
import discord

import websockets
import asyncio
import logging
import json

logger = logging.getLogger()

class Support(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot : commands.Bot = bot
        self.ws : websockets.WebSocketClientProtocol= None

        asyncio.create_task(self.ws_loop())

    @commands.Cog.listener()
    async def on_message(self, ctx: commands.Context, member: discord.Member = None):
        if member is None:
            member = ctx.author
        
        pass

    async def handle_message(self, message):
        if "message" in message:
            message = message["message"]
            channel = self.bot.get_channel(variables.SUPPORT_TICKET_CHANNEL)
            await channel.send(f"{message['user']}: {message['text']}")

    async def ws_loop(self):
        async with websockets.connect(variables.SUPPORT_API) as self.ws:
            await self.ws.send("connected")
            connected = False
            while not connected:
                msg = await self.ws.recv()
                if msg == "connected":
                    connected = True
            logger.info("Connected to the support chat websocket server, listening for messages...")

            try:
                while True:
                    msg = await self.ws.recv()
                    msg = json.loads(msg)
                    logger.info(f"Received support chat message: {msg}")
                    await self.handle_message(msg)
            except websockets.exceptions.ConnectionClosedError:
                logger.info("Connection to the support chat websocket server closed")

async def setup(bot: commands.Bot):
    await bot.add_cog(Support(bot))