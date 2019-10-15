import logging
import traceback

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

        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(
                f"Looks like I don't have enough" +
                f" permissions to execute {ctx.command}. " +
                f"Give me more POWER!"
            )
            return

        if isinstance(error, commands.BadArgument):
            await ctx.embed(
                title='Error',
                description=str(error),
                color=0xFF0000
            )
            return

        if isinstance(error, commands.CommandInvokeError):
            if error.original == self.bot.BAD_RESPONSE:
                await ctx.send('Bad response from the API.')
            elif error.original == self.bot.NO_RESULTS:
                await ctx.send('No results found.')
            elif error.original == self.bot.NON_EXISTENT:
                await ctx.send("Command/Cog doesn't exsist or unavailable.")
            else:
                log.error(error)
                traceback.print_exception(
                    type(error), error, error.__traceback__
                )
            await ctx.message.add_reaction('❗')
            return

        if isinstance(error, commands.CommandError):
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
