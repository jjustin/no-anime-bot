# no-anime-bot

Discord bot for detecting anime images

Uses [nagadomi/lbpcascade_animeface](https://github.com/nagadomi/lbpcascade_animeface)

## requirements

```
pip install python-dotenv discord.py opencv-python numpy
```

## run

```
python bot.py
```

## .env

```
DISCORD_TOKEN={bot-token}
CASCADE_FILE=./lbpcascade_animeface.xml
TEST_GUILD_IDS={guild that get messages with faces mared}
```
