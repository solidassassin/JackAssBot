from discord.ext import commands
import discord


class Utility(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(
        brief='Enlarges the given emote',
        description="Outputs the emote's url",
        aliases=['emoji']
    )
    async def emote(self, ctx, emoji: discord.Emoji):
        e = discord.Embed(color=discord.Color.gold())
        e.set_image(url=emoji.url)
        e.set_footer(text=ctx.author.display_name,
                     icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)
        await ctx.message.add_reaction('✅')

    @emote.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Not a valid emote")
            await ctx.message.add_reaction('❌')

    @commands.command(
        brief="Displays requested user's avatar",
        description="Outputs the selected user's avatar url",
        aliases=['profile']
    )
    async def avatar(self, ctx, user: discord.User):
        e = discord.Embed(color=discord.Color.blurple())
        e.set_image(url=user.avatar_url)
        e.set_footer(text=ctx.author.display_name,
                     icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)

    @commands.command(
        brief="Pong!",
        description="Returns the bot's latency in miliseconds",
        aliases=['latency']
    )
    async def ping(self, ctx):
        ping = round(self.client.latency * 1000)
        await ctx.send(f'Pong ```{ping}ms```')

    @commands.command()
    async def joined(self, ctx, *, member: discord.Member):
        await ctx.send(f'<@{member.id}> joined on {member.joined_at}')


def setup(client):
    client.add_cog(Utility(client))
