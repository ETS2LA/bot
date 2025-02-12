CLIENT_TOKEN: str = ""
"""The discord client token for the bot."""
SERVER_ID: int = 0
"""The server ID the bot should listen to."""

filename = ".env"
for line in open(filename).readlines():
    if line.startswith("TOKEN"):
        CLIENT_TOKEN = line.split("=")[1].strip()
    if line.startswith("SERVER"):
        SERVER_ID = int(line.split("=")[1].strip())