import logging
from pathlib import Path

from discord.ext import commands
from aiohttp import ClientSession

from data import config
from cogs.utils.context import Context


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s: %(name)s -> %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


class JackassBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.BAD_RESPONSE = -1
        self.NO_RESULTS = -2
        self.NON_EXISTENT = -3

    @property
    def config(self):
        return config

    async def on_ready(self):
        log.info(f"{self.user} is in!")

    async def get_context(self, message, *, cls=Context):
        return await super().get_context(message, cls=cls)

    @property
    def module_list(self):
        m = list(Path("cogs").glob("*.py"))
        all_cogs = [f"cogs.{i.name}"[:-3] for i in m]
        return all_cogs

    async def load_modules(self):
        _output = []
        for cog in self.module_list:
            try:
                self.load_extension(cog)
                _output.append(f"[{cog}] loaded")
            except commands.ExtensionAlreadyLoaded:
                _output.append(f"[{cog}] already loaded")
            except commands.ExtensionNotLoaded:
                _output.append(f"[{cog}] not loaded")
                log.exception(f"Failed to load {cog}")
        return "\n".join(_output)

    async def start(self, token: str = None):
        if not token:
            token = self.config.token
        self.session = ClientSession()
        await self.load_modules()
        await super().start(token)

    async def close(self):
        await super().close()
        await self.session.close()
