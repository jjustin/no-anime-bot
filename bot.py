# bot.py
import os
import numpy as np
from cv2 import cv2

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
cascade_file = os.getenv('CASCADE_FILE')

if not os.path.isfile(cascade_file):
    raise RuntimeError("%s: cascade file not found" % cascade_file)
cascade = cv2.CascadeClassifier(cascade_file)

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(msg):
    if(len(msg.attachments) == 0):
        return
    att = msg.attachments[0]
    img_bytes = await att.read()
    nparr = np.frombuffer(img_bytes, dtype='uint8')
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    faces = cascade.detectMultiScale(gray,
                                     # detector options
                                     scaleFactor=1.1,
                                     minNeighbors=5,
                                     minSize=(24, 24))
    if(len(faces) != 0):
        await msg.reply(file=discord.File('noAnime.png'))
        await msg.add_reaction("👎")

client.run(TOKEN)
