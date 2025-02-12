CLIENT_TOKEN: str = ""
"""The discord client token for the bot."""
SERVER_ID: int = 0
"""The server ID the bot should listen to."""
UMAMI_URL: str = "https://umami.ets2la.com"
"""The URL for ETS2LA's Umami analytics."""
UMAMI_LOGIN: str = ""
"""The login for ETS2LA's Umami analytics."""
UMAMI_PASSWORD: str = ""
"""The password for ETS2LA's Umami analytics."""
UMAMI_ID: str = ""
"""The Umami website ID for ETS2LA's analytics."""
ADMINS: list[int] = []
"""The list of people who are allowed to use admin commands."""

filename = ".env"
for line in open(filename).readlines():
    if line.startswith("TOKEN"):
        CLIENT_TOKEN = line.split("=")[1].strip()
    if line.startswith("SERVER"):
        SERVER_ID = int(line.split("=")[1].strip())
    if line.startswith("UMAMI_URL"):
        UMAMI_URL = line.split("=")[1].strip()
    if line.startswith("UMAMI_LOGIN"):
        UMAMI_LOGIN = line.split("=")[1].strip()
    if line.startswith("UMAMI_PASS"):
        UMAMI_PASSWORD = line.split("=")[1].strip()
    if line.startswith("UMAMI_ID"):
        UMAMI_ID = line.split("=")[1].strip()
    if line.startswith("ADMINS"):
        ADMINS = list(map(int, line.split("=")[1].strip().split(",")))