"""
This cog is for the custom help command.
It's quite messy, because it's temporary.
Will be replaced when I figure out how the default
 help command mechanism works.
"""
from discord.ext import commands


# so I can pass the command as argument when invoking
class ToCommand(commands.Converter):
    async def convert(self, ctx, argument):
        obj = ctx.bot.get_cog(argument.title())
        if obj:
            return obj
        obj = ctx.bot.get_command(argument.lower())
        if not obj:
            return
        return obj


# add group support for future
class CustomHelp(commands.Cog, name='Help'):
    def __init__(self, client):
        self.client = client

    async def check_command(self, term, owner):
        if term.hidden and not owner:
            raise commands.CommandInvokeError(
                self.client.NON_EXISTENT
            )
        if term.help:
            return term.help
        return 'No info provided.'

    async def check_cog(self, term, owner) -> str:
        if owner:
            cog_commands = [
                '**{} →** {}'.format(i.name, i.help.split('\n')[0])
                for i in term.get_commands() if i.help
            ]
        else:
            cog_commands = [
                '**{} →** {}'.format(i.name, i.help.split('\n')[0])
                for i in term.get_commands() if not i.hidden and i.help
            ]
        if not cog_commands:
            raise commands.CommandInvokeError(
                self.client.NON_EXISTENT
            )
        return '\n'.join(cog_commands)

    async def fetch_help(self, owner):
        fields = []
        for name, cog in self.client.cogs.items():
            if owner:
                cog_commands = [i.name for i in cog.get_commands()]
            else:
                cog_commands = [
                    i.name for i in cog.get_commands() if not i.hidden
                ]
            if not cog_commands:
                continue
            fields.append(
                {
                    'name': f'► {name}',
                    'value': f'**{" | ".join(cog_commands)}**',
                    'inline': False
                }
            )
        return fields

    @commands.command(
        name='help',
        aliases=('info', 'commands')
    )
    async def custom_help(self, ctx, term: ToCommand = None):
        """
        This is it!
        """
        owner = await self.client.is_owner(ctx.author)
        if term:
            if isinstance(term, commands.Cog):
                fields = [
                    {
                        'name': f'▼ {term.qualified_name}',
                        'value': await self.check_cog(term, owner)
                    }
                ]
            else:
                fields = [
                    {
                        'name': f'{term.name} {term.signature}',
                        'value': await self.check_command(term, owner)
                    }
                ]
        else:
            fields = await self.fetch_help(owner)
        await ctx.embed(
            fields=fields,
            header_text='Commands',
            header_icon=ctx.me.avatar_url,
            footer_text='Use jack help <command/category> for more info.'
        )


def setup(client):
    client.remove_command('help')
    client.add_cog(CustomHelp(client))
