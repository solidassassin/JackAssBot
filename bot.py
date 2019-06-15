import logging
from pathlib import Path

import discord
from discord.ext import commands
from aiohttp import ClientSession

from data import config
from cogs.extras.context import Context


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s: %(name)s -> %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger(__name__)


class JackassBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.all_cogs = None
        self.session = None
        self.BAD_RESPONSE = -1
        self.NO_RESULTS = -2
        self.NON_EXISTENT = -3

    async def on_ready(self):
        log.info(f'{self.user} is in!')
        await self.change_presence(
            activity=discord.Streaming(
                name='dangerous stunts!',
                url='https://www.twitch.tv/twitchrivals'
            )
        )

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)
        await self.invoke(ctx)

    async def load_modules(self):
        m = list(Path('cogs').glob('*.py'))
        self.all_cogs = [f'cogs.{i.name}'[:-3] for i in m]
        for cog in self.all_cogs:
            try:
                self.load_extension(cog)
            except commands.ExtensionError:
                log.exception(f'Failed to load {cog}')

    async def start(self):
        self.session = ClientSession()
        await self.load_modules()
        await super().start(self.config.token)

    async def close(self):
        await super().close()
        await self.session.close()
