import logging
import traceback

from discord import Embed
from discord.ext import commands
from discord.errors import NotFound


log = logging.getLogger(__name__)


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"You're on cooldown {ctx.author.mention}." +
                f" Try after `{round(error.retry_after, 2)}s`"
            )
            return

        if isinstance(error, commands.CheckFailure):
            await ctx.message.add_reaction('⛔')
            log.info(f'{ctx.author} was denied permissions to {ctx.command}')
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send_help(ctx.command)
            await ctx.message.add_reaction('❌')
            return

        e = Embed(
            title="Error",
            color=0xFF0000
        )
        e.set_footer(
            text=ctx.author.display_name,
            icon_url=ctx.author.avatar_url
        )

        if isinstance(error, commands.BotMissingPermissions):
            e.description = (
                "Looks like I don't have enough"
                f" permissions to execute {ctx.command}. "
                "Be a gentleman and give me more power."
            )
            await ctx.send(embed=e)
            return

        if isinstance(error, commands.BadArgument):
            e.description = str(error)
            await ctx.send(embed=e)
            return

        if isinstance(error, commands.CommandError):
            e.description = str(error)
            await ctx.send(embed=e)
            log.error(error)
            traceback.print_exception(
                type(error), error, error.__traceback__
            )

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        try:
            await ctx.message.add_reaction('✅')
        except NotFound:
            pass


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
