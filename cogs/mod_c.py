from discord.ext import commands
from discord import Member


class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return ctx.author.permissions_in(ctx.channel).manage_guild

    @commands.cooldown(2, 300)
    @commands.command(
        aliases=('clean', 'delete', 'erase', 'purge')
    )
    async def clear(self, ctx, amount: int):
        """
        Deletes a specified amount of messages.
        """
        if amount > 50:
            await ctx.send('Purge limit exceeded')
            return
        await ctx.channel.purge(limit=amount+1)

    @commands.command(
        name='member'
    )
    async def memberinfo(self, ctx, member: Member):
        """
        Provides information about the given member.
        """
        if member.activities:
            activity_names = '\n'.join([i.name for i in member.activities])
        else:
            activity_names = 'No present activities'
        fields = [
            {
                'name': 'Username:',
                'value': f'{member.name}#{member.discriminator}'
            },
            {
                'name': 'Status:',
                'value': f'{member.status}'.title()
            },
            {
                'name': 'Account created at:',
                'value': member.created_at.strftime("%Y/%m/%d")
            },
            {
                'name': 'Top role:',
                'value': member.top_role.mention
            },
            {
                'name': 'Joined at:',
                'value': member.joined_at.strftime("%Y/%m/%d")
            },
            {
                'name': 'Current activities:',
                'value': activity_names
            }
        ]
        await ctx.embed(
            thumbnail=member.avatar_url,
            fields=fields,
            header_text=ctx.guild.name,
            header_icon=ctx.guild.icon_url
        )


def setup(client):
    client.add_cog(Mod(client))
