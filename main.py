import discord
from discord.ext import commands
from mwthesaurus import MWClient
import json

with open("tokens.json", "r") as file:
    tokens = json.loads(file.read())

client = discord.Client()

client.mwc = MWClient(key=tokens["mw"])
client.webhook_cache = {}
client.user_cache = {}

# stuff here

@client.event
async def on_message(message):
    if message.author.id == message.channel.guild.me.id:
        return
    if message.content.startswith("?"):
        if len(message.content) == 1:
            return
        elif message.content[1:].startswith("optin"):
            userdata = client.user_cache.pop(message.channel.id,None)
            if userdata == None:
                userdata = [message.author.id]
            elif not message.author.id in userdata:
                userdata.append(message.author.id)
            client.user_cache[message.channel.id] = userdata
            await message.channel.send("Done!")
            return
        elif message.content[1:].startswith("optout"):
            userdata = client.user_cache.pop(message.channel.id,None)
            if userdata == None:
                return
            elif message.author.id in userdata:
                userdata.remove(message.author.id)
            else:
                return
            client.user_cache[message.channel.id] = userdata
            await message.channel.send("Done!")
            return
        if message.channel.id in client.user_cache and message.author.id in client.user_cache[message.channel.id]:
            

# start the bot

client.run(tokens["bot"])
