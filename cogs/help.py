import itertools

from discord import Embed
from discord.ext import commands


class CustomHelp(commands.HelpCommand):
    def __init__(self, **options):
        super().__init__(**options)
        self.paginator = None
        self.spacer = "\u1160 "

    async def send_pages(self, header=False, footer=False):
        destination = self.get_destination()
        embed = Embed(
            color=0x71368a
        )
        if header:
            embed.set_author(
                name=header,
                icon_url=self.context.bot.user.avatar_url
            )
        for category, entries in self.paginator:
            embed.add_field(
                name=category,
                value=entries,
                inline=False
            )
        if footer:
            embed.set_footer(
                text='Use jack help <command/category> for more information.'
            )
        await destination.send(embed=embed)

    async def send_bot_help(self, mapping):
        ctx = self.context
        bot = ctx.bot

        def get_category(command):
            cog = command.cog
            return cog.qualified_name + ':' if cog is not None else 'Help:'

        filtered = await self.filter_commands(
            bot.commands,
            sort=True,
            key=get_category
        )
        to_iterate = itertools.groupby(filtered, key=get_category)
        for cog_name, command_grouper in to_iterate:
            cmds = sorted(command_grouper, key=lambda c: c.name)
            category = f'► {cog_name}'
            if len(cmds) == 1:
                entries = f'{self.spacer}**{cmds[0].name}** → {cmds[0].short_doc}'
            else:
                entries = ' | '.join(f'**{command.name}**' for command in cmds)
                entries = self.spacer + entries
            self.paginator.append((category, entries))
        await self.send_pages(header='Help', footer=True)

    async def send_cog_help(self, cog):
        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        if not filtered:
            await self.context.send(
                'No commands in this cog.'
            )
            return
        category = f'▼ {cog.qualified_name}'
        entries = '\n'.join(
            self.spacer +
            f'**{command.name}** → {command.short_doc or command.description}'
            for command in filtered
        )
        self.paginator.append((category, entries))
        await self.send_pages(header='Commands', footer=True)

    async def send_group_help(self, group):
        filtered = await self.filter_commands(group.commands, sort=True)
        if not filtered:
            await self.context.send('No public commands in group.')
            return
        category = f'**{group.name}** - {group.description or group.short_doc}'
        entries = '\n'.join(
            self.spacer + f'**{command.name}** → {command.short_doc}'
            for command in filtered
        )
        self.paginator.append((category, entries))
        await self.send_pages(header='Commands', footer=True)

    async def send_command_help(self, command):
        signature = self.get_command_signature(command)
        helptext = command.help or command.description or 'No help provided.'
        self.paginator.append((signature,  helptext))
        await self.send_pages(header='Description')

    async def prepare_help_command(self, ctx, command=None):
        self.paginator = []
        await super().prepare_help_command(ctx, command)


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.help_command = CustomHelp(
            command_attrs={
                'aliases': ('info', 'commands'),
                'help': 'This message.'
            }
        )

    def cog_unload(self):
        self.client.get_command('help').hidden = False
        self.client.help_command = commands.DefaultHelpCommand()


def setup(client):
    client.add_cog(Help(client))
