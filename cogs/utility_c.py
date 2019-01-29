from discord.ext import commands
import discord

class Utility:

    def __init__(self, client):
        self.client = client

    @commands.command(
        brief='Enlarges the given emote',
        description="Outputs the emote's url",
        aliases=['emoji']
    )
    async def emote(self, ctx, emoji: discord.Emoji):
        await ctx.send(emoji.url)


    @commands.command(
        brief="Displays requested user's avatar",
        description="Outputs the selected user's avatar url",
        aliases=['profile']
    )
    async def avatar(self, ctx, user: discord.User):
        await ctx.send(user.avatar_url)


    @commands.command(
        brief="Pong!",
        description="Returns the bot's latency in miliseconds",
        aliases=['latency']
    )
    async def ping(self, ctx):
        ping = round(self.client.latency * 1000)
        await ctx.send(f'Pong ```{ping}ms```')

        
def setup(client):
    client.add_cog(Utility(client))