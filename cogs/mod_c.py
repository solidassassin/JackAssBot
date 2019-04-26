from discord.ext import commands


class Mod(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return ctx.author.permissions_in(ctx.channel).manage_guild

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.message.add_reaction('⛔')
            await ctx.send("🖕")

    @commands.command(
        brief='Deletes the specified amount of messages',
        description="Deletes the specified amount of messages",
        aliases=['clean', 'delete', 'erase', 'purge']
    )
    async def clear(self, ctx, amount: int):
        if amount > 200:
            await ctx.send('Purge limit exceeded')
        else:
            await ctx.channel.purge(limit=amount+1)


def setup(client):
    client.add_cog(Mod(client))
