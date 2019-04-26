"""
TODO:
1. Custom help command  // probs gonna take a while
3. More management commands
4. Urban dictionary command  // almost done
5. New, nsfw cog  // almost done
6. Better error and check handling
8. Recatagorize sum shit
9. A guild leave command  // almost done
10. A few more owner commands  // almost done
11. Testing with music commands  // tests working
"""
from discord.ext import commands
from aiohttp import ClientSession
import discord
import os
import json
import logging


class Jackass(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('jack ', 'Jack '),
            case_insensitive=True,
            description='JackAss is here to piss you off!'
        )
        with open('data/config.json') as keys:
            self.config = json.load(keys)
        with open('data/languages.json') as keys:
            self.languages = json.load(keys)
        self.session = ClientSession()

    async def on_ready(self):
        await self.modules()
        print(f'{self.user} is in!')
        await self.change_presence(
            activity=discord.Streaming(
                name='dangerous stunts!',
                url='https://www.twitch.tv/twitchrivals'
            )
        )

    async def modules(self):
        for cog in os.listdir('cogs'):
            filename, filetype = os.path.splitext(cog)
            if '.py' in filetype:
                try:
                    self.load_extension(f'cogs.{filename}')
                except Exception as e:
                    print(f'{cog} failed to load: {e}')

    # do a seperate module for error handling
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Finish your sentece and only then I'll help 😉")
            await ctx.message.add_reaction('❌')
        if isinstance(error, commands.MissingPermissions):
            await ctx.message.add_reaction('⛔')
        if isinstance(error, commands.CheckFailure):
            print('Permissions denied')
        else:
            logging.exception(error)

    def run(self):
        super().run(self.config['token'])


if __name__ == "__main__":
    Jackass().run()
