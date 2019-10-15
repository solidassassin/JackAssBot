from discord.ext import commands
from discord import Member


class GuildConv(commands.Converter):
    async def convert(self, ctx, guild):
        if guild.isdigit():
            gen = (i for i in ctx.bot.guilds if int(guild) == i.id)
            return next(gen, None)
        gen = (i for i in ctx.bot.guilds if guild == i.name)
        return next(gen, None)


class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return ctx.author.permissions_in(ctx.channel).manage_guild

    @commands.cooldown(2, 300)
    @commands.command(
        aliases=('clean', 'delete', 'purge')
    )
    async def erase(self, ctx, amount: int):
        """Deletes a specified amount of messages."""
        if amount > 50:
            return await ctx.send('Purge limit exceeded')
        await ctx.channel.purge(limit=amount+1)

    @commands.command(
        name='member'
    )
    async def memberinfo(self, ctx, member: Member):
        """Provides information about the given member."""
        fields = {
            'Username:': str(member),
            'Status:': str(member.status).title(),
            'Account created at:': member.created_at.strftime("%Y/%m/%d"),
            'Top role:': member.top_role.mention
            if str(member.top_role) != '@everyone' else '@everyone',
            'Joined at:': member.joined_at.strftime("%Y/%m/%d"),
            'Current activities:': '\n'.join(i.name for i in member.activities)
            if member.activities else 'No current activities'
        }
        await ctx.embed(
            color=member.color,
            thumbnail=member.avatar_url,
            fields=fields,
            header_text=ctx.guild.name,
            header_icon=ctx.guild.icon_url,
            footer_default=True
        )

    @commands.group(
        invoke_without_command=True
    )
    async def leave(self, ctx):
        await ctx.guild.leave()

    @leave.command(
        name='guild',
        hidden=True
    )
    async def owner_leave(self, ctx, guild: GuildConv):
        if await ctx.bot.is_owner(ctx.author):
            if guild:
                await guild.leave()
                return
            await ctx.send("Guild doesn't exsist.")


def setup(client):
    client.add_cog(Mod(client))
