from discord.ext import commands
from discord import Embed


class Adult(commands.Cog, name='NSFW'):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return ctx.channel.is_nsfw()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            try:
                nsfw = [i.id for i in ctx.guild.text_channels if i.is_nsfw()]
                await ctx.send(f"👉 <#{nsfw[0]}> 👌😩🍆💦")
            except IndexError:
                await ctx.send('No nsfw channels available in this server.')
            await ctx.message.add_reaction('⛔')

    @commands.command(
        name='hentai',
        brief='Retruns a hentai pic'
    )
    async def anime(self, ctx):
        url = 'https://nekos.life/api/v2/img/hentai'
        async with self.client.session.get(url) as r:
            if r.status != 200:
                await ctx.send(f'Bad response {ctx.author.mention} 😔')
                await ctx.message.add_reaction('❗')
                return
            hentai = await r.json()
        e = Embed(title='Hentai 😏', color=0xff75f8)
        e.set_image(url=hentai['url'])
        e.set_footer(
            text=ctx.author.display_name,
            icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=e)
        await ctx.message.add_reaction('✅')


def setup(client):
    client.add_cog(Adult(client))
