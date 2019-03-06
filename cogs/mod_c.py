from discord.ext import commands
import discord


class Mod(commands.Cog):

    def __init__(self, client):
        self.client = client

    
    @commands.command(
        brief='Disconnects bot',
        aliases=['goodbye', 'die'],
        hidden=True
    )
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send('See ya bitch!')
        await self.client.close()



    @commands.command(
        brief='Deletes the specified amount of messages',
        description="Deletes the specified amount of messages above your's from all users",
        aliases=['clean', 'delete', 'erase']
    )
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount+1)


def setup(client):
    client.add_cog(Mod(client))


