import utils.variables as variables
from discord.ext import commands
import discord

from typing import TypedDict, Optional, Literal
import websockets
import traceback
import requests
import asyncio
import logging

logger = logging.getLogger()

# region Types

class MemberDict(TypedDict):
    '''Dictionary which holds information about a member of a conversation'''
    username: str # Username of the member
    uuid: str # type == "ETS2LA" -> uuid, type == "Discord" -> discord_id
    type: Literal["ETS2LA", "Discord"] # Type of the member (ETS2LA or Discord)

class MessageContentsDict(TypedDict):
    '''Dictionary which holds information about a message'''
    id: int # Each message in a conversation has a unique id, starts at 0
    uuid: str # UUID of the user who sent the message, must match a MemberDict.uuid in the conversation
    text: str # Text of the message
    images: list[bytes] # List of base64 encoded image attachments
    reply: Optional[int] # ID of the message which is being replied to

class MessageDict(TypedDict):
    '''Wrapper for MessageContentsDict to keep MessageDict and EventDict consistent'''
    message: MessageContentsDict # Wrapper for MessageContentsDict

class EventDict(TypedDict):
    '''Dictionary which holds information about an event'''
    event: str # Event text, ex. "{user} started a new conversation"

class ConversationDict(TypedDict):
    '''Dictionary which holds information about a conversation'''
    id: int # Each users conversation has a unique id, starts at 0
    name: str # Name of the conversation
    members: list[MemberDict] # List of members
    messages: list[MessageDict | EventDict] # List of chat events
    tags: list[str] # List of tags

# region Classes

class TicketManager:
    def __init__(self, bot : commands.Bot):
        self.bot : commands.Bot = bot
        self.tickets : list[ConversationDict] = []
        self.channel : discord.ForumChannel = bot.get_channel(variables.SUPPORT_TICKET_CHANNEL)

    def add_ticket(self, ticket: ConversationDict):
        # TODO: Save ticket
        self.tickets.append(ticket)

# region Cog

class Support(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot : commands.Bot = bot
        self.ws : websockets.WebSocketClientProtocol = None
        self.attempted_ws_connection = False
        self.api_available = False

        self.channel = bot.get_channel(variables.SUPPORT_TICKET_CHANNEL)
        self.new_webhook_url = f"{variables.DISCORD_WEBHOOK}/channels/{self.channel.id}/webhooks"

        asyncio.create_task(self.attempt_ws_connection())
        while not self.attempted_ws_connection: pass # Wait for the connection to be attempted
        self.conversations = self.get_db_conversations()

    def get_db_conversations(self):
        if not self.api_available:
            return []
        
        try:
            headers = {"Authorization": f"Bearer {variables.ENV.CHAT_API_TOKEN}"}
            response = requests.get(f"{variables.SUPPORT_API}/conversations", headers=headers)
        except:
            logger.error(f"Failed to get conversations from the support chat API: {traceback.format_exc()}")
            return []
        
        try:
            json_response = response.json()
            if json_response["status"] != "success":
                logger.error(f"Support chat API returned an error: {json_response['error']}")
                return []
            return json_response["data"]
        except:
            logger.error(f"Failed to parse conversations from the support chat API: {traceback.format_exc()}")
            return []

    def add_chat_event(self, conv_id: int, event: EventDict | MessageDict):
        if not self.api_available:
            return
        
        try:
            requests.post(f"{variables.SUPPORT_API}/conversations/", json=self.conversations)
        except:
            logger.error(f"Failed to save conversations to the support chat API: {traceback.format_exc()}")

    @commands.Cog.listener("on_message")
    async def on_message(self, ctx: commands.Context, member: discord.Member = None):
        if member is None:
            member = ctx.author

        
        
        pass

    def after_connection_actions(self):
        self.api_available = True
        self.conversations = self.get_db_conversations()

    async def handle_message(self, message : MessageDict | EventDict):
        if "message" in message:
            message = message["message"]
            pass
        elif "event" in message:
            message = message["event"]
            pass
        else:
            logger.warning(f"Unknown message type was received: {message}")
            return

    async def ws_loop(self):
        self.ws = None
        try:
            async with websockets.connect(variables.SUPPORT_API) as self.ws:
                await self.ws.send("connected")
                connected = False
                while not connected:
                    msg = await self.ws.recv()
                    if msg == "connected":
                        self.after_connection_actions()
                        connected = True
                logger.info("Connected to the support chat websocket server, listening for messages...")

                while True:
                    msg = await self.ws.recv()
                    print(f"Received support chat message: {msg}")
                    self.handle_message(msg)

        except websockets.ConnectionClosed or websockets.ConnectionClosedOK or websockets.ConnectionClosedError:
            logging.warning("The ETS2LA chat support servers closed the connection.")
            self.ws = False
        except ConnectionRefusedError:
            logging.warning("A connection could not be made with the ETS2LA chat support servers.")
            self.ws = False
        finally:
            try: await self.ws.close()
            except: pass

    async def attempt_ws_connection(self):
        while True:
            await self.ws_loop() # If this returns, the connection failed or was closed
            self.api_available = False
            await asyncio.sleep(300) # Attempt to reconnect every 5 minutes

async def setup(bot: commands.Bot):
    await bot.add_cog(Support(bot)) 

# endregion