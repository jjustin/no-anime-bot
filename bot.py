# bot.py
import os
import io
import numpy as np
import requests
from cv2 import cv2

import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CASCADE_FILE = os.getenv('CASCADE_FILE')
DEBUG = os.getenv('DEBUG')

if not os.path.isfile(CASCADE_FILE):
    raise RuntimeError("%s: cascade file not found" % CASCADE_FILE)
cascade = cv2.CascadeClassifier(CASCADE_FILE)

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(msg):
    if(msg.author.id == client.user.id):
        return
    
    to_check = [] # list of images to check
    
    # scan attachments
    for att in msg.attachments:
        to_check.append(await att.read())

    # scan embeds
    for embed in msg.embeds:
        if(embed.thumbnail.url != embed.Empty):
            to_check.append(requests.get(embed.thumbnail.url).content)
        if(embed.image.url != embed.Empty):
            to_check.append(requests.get(embed.image.url).content)
            
    # check each image seperately
    violated = False
    for img_bytes in to_check:
        nparr = np.frombuffer(img_bytes, dtype='uint8')
        img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = cascade.detectMultiScale(gray,
                                     scaleFactor=1.1,
                                     minNeighbors=5,
                                     minSize=(24, 24))
        
        # handle images that violate no anime conventions
        if(len(faces) != 0):
            violated = True
            
            # report where face was spotted in debug mode
            if(DEBUG == 1):
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.imwrite( "tmp.jpg", img)
                await msg.reply(file=discord.File('tmp.jpg'))
    
    # respond based on `violated` status
    if(violated):
        await msg.reply(file=discord.File('noAnime.png'))
        await msg.add_reaction("👎")
        
client.run(TOKEN)
