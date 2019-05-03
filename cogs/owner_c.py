from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return await ctx.bot.is_owner(ctx.author)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('🖕')
            await ctx.message.add_reaction('⛔')

    @commands.command(
        brief='Disables bot',
        aliases=['goodbye', 'die']
    )
    async def logout(self, ctx):
        await ctx.send('See ya bitch!')
        await self.client.logout()


def setup(client):
    client.add_cog(Owner(client))
