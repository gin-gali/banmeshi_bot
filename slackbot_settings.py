import os

API_TOKEN = os.environ.get("SLACK_API_KEY", "")

default_reply ="Sorry, I don't understand that phrase."

PLUGINS = [
    "plugins",
]