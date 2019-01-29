from  discord.ext import commands
import discord
import os
import json


client = commands.Bot(command_prefix=['jack ', 'Jack '], 
                      description='JackAss is here to piss you off!')

with open('config.json') as keys:
    config = json.load(keys)


@client.event
async def on_ready():
    print(f'{client.user} is in!')
    await client.change_presence(activity=discord.Activity(name='my creator', type=2))
    return True


for cog in os.listdir('cogs'):
    filename, filetype = os.path.splitext(cog)
    if '.py' in filetype:
        try:
            client.load_extension(f'cogs.{filename}')
        except:
            print(f'{cog} failed to load')


client.run(config['token'])
