import random
import asyncio
import requests
import re
import os, sys
import emoji
import urllib
import aiosqlite
import json
import traceback
from io import BytesIO
from datetime import timedelta, datetime
from itertools import cycle
from discord.utils import get
from discord import *
from discord.ext import commands, tasks
from discord.ext.commands import cooldown
from difflib import get_close_matches
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('activeAlertsCogs/Config/.env')
load_dotenv(dotenv_path=dotenv_path)
TOKEN = os.getenv('TOKEN')
forward = "▶"
backward = "◀"
cancel_emoji = "⏹"
approve = "✅"
retry = "🔄"
lock = "🔒"
deny = "❎"
one = "1️⃣"
two = "2️⃣"
usage = "**Usage :** "
explain = "**Explanation :** "
perms = "**Permissions :** "
aliases = "**Aliases :** "
example = "**Example :** "
cool_down = "**Cool Down :** "
note = "**Note :** "
another = "**or**"

prefix = "!aa "
pre = prefix
def random_color():
    return random.randint(0, 0xffffff)