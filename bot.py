from discord.ext import commands
import discord
import os
import json


client = commands.Bot(command_prefix=['jack ', 'Jack ', 'jackass ', 'Jackass'],
                      description='JackAss is here to piss you off!',
                      pm_help=True)

with open('data/config.json') as keys:
    config = json.load(keys)


@client.event
async def on_ready():
    print(f'{client.user} is in!')
    await client.change_presence(
        activity=discord.Streaming(
            name='dangerous stunts!',
            url='https://www.twitch.tv/twitchrivals'))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Finish your sentece and only then I'll help 😉")
        await ctx.message.add_reaction('❌')
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.add_reaction('⛔')
    if isinstance(error, commands.CheckFailure):
        print('Permissions denied')


for cog in os.listdir('cogs'):
    filename, filetype = os.path.splitext(cog)
    if '.py' in filetype:
        try:
            client.load_extension(f'cogs.{filename}')
        except Exception as e:
            print(f'{cog} failed to load: {e}')


client.run(config['token'])
