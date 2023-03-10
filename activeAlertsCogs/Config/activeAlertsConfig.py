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
# from pyrebase4 import pyrebase4
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

CONFIG = {
  "type": "service_account",
  "project_id": "black-bot-8458c",
  "private_key_id": "58f5a1818155607f5f7153a579c258ce478df5a4",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCwyiE1sZ9/UYWD\nnesvDmDeNngWyp6JfvZmmcVP33JOd7KNpvlDwWDDXZfD1d8PH/zloSuHkojFgfoH\nzy1/thefKutMx9Q9892HhAuCt1J4Stx2qZuFelTL5nNgI6rgQPIIiAxq+7DYn4I1\nQam2rf3hL2U/lBKPp0R9hDaqX5nY/1uFPnDLMh2lI0iCugYRDHRvMLIGjf/9Dj3I\n33bRom3nWVIHPeo4n95Z0yVeB0t4u+FzqyNe5HEMXMl3Rpfw88xFjl6HHRaMrYiO\nYiKTo7sgTdg4GypO8KlTyy/hTE5schLSpxzjtHSGMrfZbLxgBqptCen+1+dK4cMo\nbcoY+5DnAgMBAAECggEAHM5Km/udr/qiBSCZnhi7Kun4JkqMi33O+0fJ8SpI70Us\nqE0RJ3ueXybkYCn8hvPg2q+orpXvSDNWAKi+0qTic3JkVaXnzNJsAbU/xORHAUe9\nZW5cY2Lb5z9dBEi7gn/CkCZO063AEoPnDPNuilAOYn89AZ+IaLTKAaOl3pvmLwej\nGv0mpADsMA1Vk6AZpjYYKqa1r6igKlPQXqpt6qZTtqt27KvVpFB/MiENPtPrdfmc\nXNG55iKiqkgHs2+DOdk4ec9Ue3KLpff5r7KuujOPdKpSsY/vuuSCjbTV086HohYG\nyRDMljZBg4ylaz83xDL2/mzA1d+S9Al1HSeQFeKqzQKBgQDnC1PWkiUDxNY8QgOH\n0ZcBn5ezUfryr+4meVHBeLXrXNFKMYnVjH28JgP1yE3jfeDGOIWr9dqFR7N49IJf\npKBkw+y+txSg86wTxG6yTjUNpLkmNq5LcmP+AtnoBodgE5M85iWPF/goqCON+Z1G\nyZ18zULQVpVcnp9VQjEk0knfHQKBgQDD4pcTc+FhiIWWB2ZzjFwQRjulesFNBhGV\nGYW2FrEF8H97WO16QZF3Qcq3xMezCwxW81HlWwyoofeZnle/lVmeHfdxKmyR7AK5\nG+IYeK46NpQlt0jOu0TGNYsnNhyB4G+sjjd13sAOBUzDlRHs3oRubUiogwHmzM42\n8AmsIj+c0wKBgQCJLUmOyWCetzy3tD4iYsd0mEvalR8Y/mm4gCmRZFkmsAo3Mehz\nWSHCFxQc1tuf6ToOlrqO2b7viR2+//V0UetFSKqEpXDjCyos5mEPDq4jNp0TWj3r\n37QMuaalQ1MXMSgnbUH5jrKxePr7Law6vjP6SGiWCAJQZoGVfmJtSUnA5QKBgQDA\n3cYgOhVsIa5d1LV0CXvP7kbmHKJcgyAmrLVxXpA3p97tBNb1a7+dKyM8ozx4teUV\na4d0CpzBIJAYKcZ99MADJcAvJTU2y6i2t5R6wb/Rw1FEfVzrZ4lEmw2Csw2IdwGd\nZX2HyaVRaLh3TbwTe9fqniFPAYaKx5Y2k0sCt8noTwKBgHCF2Ewra4wI9lFcnxSc\nuBaHOu1T1Et74x9SNu9e7vpDZVf1P22CR/+Y4rdz/314v9goO/JrsVJZH/tiUMgB\n8iCRs78qNh0TknEWEnfJz4x34hBsI1+wTVwUni4ksjc2AqftwzY92kLtCnkZPctM\nXrJHlP7U6YDCGG6sAw98c1gn\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-r7g2v@black-bot-8458c.iam.gserviceaccount.com",
  "client_id": "117004446963643146883",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-r7g2v%40black-bot-8458c.iam.gserviceaccount.com"
}

# firebase = pyrebase.initialize_app(CONFIG)

CONFIG1 = {
    "apiKey": "AIzaSyC08u4sUrVrq-eiX-B6Te09cCvnS_AfXHU",
    "authDomain": "philosophia-b2b5d.firebaseapp.com",
    "databaseURL": "https://philosophia-b2b5d-default-rtdb.firebaseio.com",
    "projectId": "philosophia-b2b5d",
    "storageBucket": "philosophia-b2b5d.appspot.com",
    "messagingSenderId": "889150830407",
    "appId": "1:889150830407:web:0d025eb4defde771fcbe62"

}

# firebase1 = pyrebase.initialize_app(CONFIG1)

"""String Variables"""
economy = "<a:arcadia:845876705364934686>"
usage = "**Usage :** "
explain = "**Explanation :** "
perms = "**Permissions :** "
aliases = "**Aliases :** "
example = "**Example :** "
cool_down = "**Cool Down :** "
note = "**Note :** "
another = "**or**"
head_staff = "Admin"
owner = "Death"
cancel = ["Cancel", "cancel"]
stop = ["Stop", "stop"]
forward = "▶"
backward = "◀"
cancel_emoji = "⏹"
approve = "✅"
retry = "🔄"
lock = "🔒"
deny = "❎"
one = "1️⃣"
two = "2️⃣"
pre = "!p "
skip = ["Skip", "skip"]
remove = ["Remove", "remove"]
staff = "Staff"
prefix = "!p "
APIKEY = "AIzaSyC7glVM0Gjn7qOJN6YJfvxiRLPCuxxPA3k"
SEARCHENGINEID = "f5fc73a6457027f48"
WEBHOOKTOKEN = "gg5_n-GggXZb_eZVNxmjs4yso8It4A7Eb_bQG4Hvv5CXbqGgTqacAvCSD5ZNlDnDtcO8"
languages = {
"🇺🇲":"um",
"🇹🇦":"ta",
"🇸🇯":"sj",
"🇲🇫":"mf",
"🇭🇲":"hm",
"🇩🇬":"dg",
"🇻🇳":"vn",
"🇼🇫":"wf",
"🇪🇭":"eh",
"🇾🇪":"ye",
"🇿🇲":"zm",
"🇿🇼":"zw",
"🇦🇨":"ac",
"🇧🇻":"bv",
"🇨🇵:":"cp",
"🇻🇪🇻🇦🇻🇺":"ve",
"None1":"va",
"None":"vu",
"🇺🇿":"uz",
"🇺🇾":"uy",
"🇺🇸":"us",
"🇹🇷":"tr",
"🇹🇲":"tm",
"🇹🇨":"tc",
"🇻🇮":"vi",
"🇹🇻":"tv",
"🇺🇬":"ug",
"🇺🇦":"ua",
"🇬🇧":"gb",
"🇦🇪":"ae",
"🇹🇳":"tn",
"🇹🇹":"tt",
"🇹🇴":"to",
"🇹🇰":"tk",
"🇹🇬":"tg",
"🇹🇱":"tl",
"🇹🇭":"th",
"🇹🇿":"tz",
"🇹🇯":"tj",
"🇵🇲":"pm",
"🇻🇨":"vc",
"🇸🇩":"sd",
"🇸🇷":"sr",
"🇸🇿":"sz",
"🇸🇪":"se",
"🇨🇭":"ch",
"🇸🇾":"sy",
"🇹🇼":"tw",
"🇱🇨":"lc",
"🇰🇳":"kn",
"🇸🇭":"sh",
"🇧🇱":"bl",
"🇱🇰":"lk",
"🇪🇸":"es",
"🇸🇬":"sg",
"🇸🇸":"ss",
"🇰🇷":"kr",
"🇿🇦":"za",
"🇸🇨":"sc",
"🇸🇱":"sl",
"🇸🇽":"sx",
"🇸🇰":"sk",
"🇸🇮":"si",
"🇬🇸":"gs",
"🇸🇧":"sb",
"🇸🇴":"so",
"🇷🇸":"rs",
"🇸🇳":"sn",
"🇸🇦":"sa",
"🇸🇹":"st",
"🇸🇲":"sm",
"🇼🇸":"ws",
"🇷🇼":"rw",
"🇷🇺":"ru",
"🇷🇴":"ro",
"🇵🇾":"py",
"🇵🇪":"pe",
"🇵🇭":"ph",
"🇵🇳":"pn",
"🇵🇱":"pl",
"🇵🇹":"pt",
"🇵🇷":"pr",
"🇶🇦":"qa",
"🇷🇪":"re",
"🇵🇬":"pg",
"🇵🇦":"pa",
"🇵🇸":"ps",
"🇵🇼":"pw",
"🇵🇰":"pk",
"🇴🇲":"om",
"🇳🇴":"no",
"🇲🇵":"mp",
"🇰🇵":"kp",
"🇳🇵":"np",
"🇳🇱":"nl",
"🇳🇨":"nc",
"🇳🇿":"nz",
"🇳🇮":"ni",
"🇳🇪":"ne",
"🇳🇬":"ng",
"🇳🇺":"nu",
"🇳🇫":"nf",
"🇳🇷":"nr",
"🇳🇦":"na",
"🇲🇲":"mm",
"🇲🇿":"mz",
"🇲🇸":"ms",
"🇲🇦":"ma",
"🇲🇪":"me",
"🇲🇳":"mn",
"🇲🇨":"mc",
"🇲🇹":"mt",
"🇲🇭":"mh",
"🇲🇶":"mq",
"🇲🇷":"mr",
"🇲🇺":"mu",
"🇾🇹":"yt",
"🇲🇽":"mx",
"🇫🇲":"fm",
"🇲🇩":"md",
"🇲🇱":"ml",
"🇲🇾":"my",
"🇲🇻":"mv",
"🇲🇼":"mw",
"🇲🇬":"mg",
"🇲🇰":"mk",
"🇲🇴":"mo",
"🇱🇺":"lu",
"🇱🇹":"lt",
"🇰🇼":"kw",
"🇰🇬":"kg",
"🇱🇦":"la",
"🇱🇻":"lv",
"🇱🇧":"lb",
"🇱🇸":"ls",
"🇱🇷":"lr",
"🇱🇾":"ly",
"None3":"li",
"None2":"xk",
"🇰🇮":"ki",
"🇰🇪":"ke",
"🇰🇿":"kz",
"🇯🇴":"jo",
"🇯🇪":"je",
"🇯🇵":"ja",
"🇯🇲":"jm",
"🇮🇸":"is",
"🇮🇳":"in",
"🇮🇩":"id",
"🇮🇷":"ir",
"🇮🇶":"iq",
"🇮🇪":"ie",
"🇮🇲":"im",

"🇮🇹":"it",
"🇭🇺":"hu",
"🇭🇰":"hk",
"🇭🇳":"hn",
"🇭🇹":"ht",
"🇬🇾":"gy",
"🇬🇼":"gw",
"🇬🇳":"gn",
"🇬🇬":"gg",
"🇬🇹":"gt",
"🇬🇪":"ge",
"🇩🇪":"de",
"🇬🇭":"gh",
"🇬🇮":"gi",
"🇬🇷":"gr",
"🇬🇱":"gl",
"🇬🇩":"gd",
"🇬🇵":"gp",
"🇬🇺":"gu",
"🇬🇲":"gm",
"🇬🇦":"ga",
"🇹🇫":"tf",
"🇵🇫":"pf",
"🇬🇫":"gf",
"🇫🇷":"fr",
"🇫🇮":"fi",
"🇫🇯":"fj",
"🇫🇴":"fo",
"🇪🇨":"ec",
"🇪🇬":"eg",
"🇸🇻":"sv",
"🇬🇶":"gq",
"🇪🇷":"er",
"🇪🇪":"ee",
"🇪🇹":"et",
"🇪🇺":"eu",
"🇫🇰":"fk",
"🇩🇴":"do",
"🇩🇲":"dm",
"🇩🇯":"dj",
"🇩🇰":"dk",
"🇨🇿":"cz",
"🇨🇾":"cy",
"🇨🇼":"cw",
"🇨🇺":"cu",
"🇭🇷":"hr",
"🇨🇽":"cx",
"🇨🇨":"cc",
"🇨🇴":"co",
"🇰🇲":"km",
"🇨🇬":"cg",
"🇨🇰":"ck",
"🇨🇷":"cr",
"🇨🇮":"ci",
"🇨🇳":"cn",
"🇨🇱":"cl",
"🇹🇩":"td",
"🇨🇫":"cf",
"🇰🇾":"ky",
"🇧🇶":"bq",
"🇨🇻":"cv",
"🇮🇨":"ic",
"🇨🇦":"ca",
"🇧🇷":"br",
"🇮🇴":"io",
"🇻🇬":"vg",
"🇧🇳":"bn",
"🇧🇬":"bg",
"🇧🇫":"bf",
"🇧🇮":"bi",
"🇰🇭":"kh",
"🇨🇲":"cm",
"🇧🇼":"bw",
"🇧🇦":"ba",
"🇧🇴":"bo",
"🇧🇹":"bt",
"🇧🇲":"bm",
"🇧🇯":"bj",
"🇧🇪":"be",
"🇧🇿":"bz",
"🇧🇾":"by",
"🇦🇲":"am",
"🇦🇼":"aw",
"🇦🇺":"au",
"🇦🇹":"at",
"🇦🇿":"az",
"🇧🇸":"bs",
"🇧🇭":"bh",
"🇧🇩":"bd",
"🇧🇧":"bb",



}
"""Integer Variables"""

mute_role_id = 0
random_color = random.randint(0, 0xffffff)
banned_categories = [772407133979017236, 772394105325748224, 767486977640628225]
arena_cagetory_ID = 837440246152691732
guild_ID = 756513497411616888
serverVoterID = 845427840660275201
serverVoter10xID = 845428337480564808
serverVoter20xID = 845428130319433788
serverVoter30xID = 845428250053181460
serverVoter40xID = 845428445101686825
active_alerts_ID = 847261861841076254
authors = [509928901007376384, 652084886496346133]
WEBHOOKID = 841759475731136583
firstSlowdownTime = 5
secondSlowdownTime = 60
thirdSlowdownTime = 300
gamesCount = 4
"""Other Variables"""
# analyser = SentimentIntensityAnalyzer()
# db = firebase.database()
# db1 = firebase1.database()
# translator = google_translator()
# webhook = Webhook.partial(WEBHOOKID, WEBHOOKTOKEN, adapter=RequestsWebhookAdapter())
# session = aiohttp.ClientSession()

"""Functions"""
async def get_json( url:str):
    try:

        async with session.get(url) as resp:
            try:
                load = await resp.json()
                return load
            except:
                return {}
    except asyncio.TimeoutError:
        return {}


