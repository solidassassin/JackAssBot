from discord.ext import commands
import discord


class Mod:

    def __init__(self, client):
        self.client = client

    
    @commands.command(
        brief='Disconnects bot',
        aliases=['goodbye', 'die'],
        hidden=True
    )
    async def logout(self, ctx):
        if ctx.message.author.id == 422042111827902484: # enter your id here
            await ctx.send('See ya bitch!')
            await self.client.close()
        else:
            await ctx.send("You can't tell me when to leave\n"
                            "https://www.youtube.com/watch?v=VDzAyiRyOMo")


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


