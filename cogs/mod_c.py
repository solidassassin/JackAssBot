from discord.ext import commands


class Mod(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(
        brief='Deletes the specified amount of messages',
        description="Deletes the specified amount of messages",
        aliases=['clean', 'delete', 'erase']
    )
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount+1)


def setup(client):
    client.add_cog(Mod(client))
