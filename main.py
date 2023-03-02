import discord
import os
import firebase_admin
from firebase_admin import credentials
from activeAlertsCogs.Config.activeAlertsConfig import *

cred = credentials.Certificate(CONFIG)
firebase_admin.initialize_app(cred)

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hi Daddy! 😘')


client.run(os.getenv('TOKEN'))