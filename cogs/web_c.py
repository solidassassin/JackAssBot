from discord.ext import commands
from discord import Embed
from urllib.parse import quote
import random


class Web(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(
        name='gif',
        brief='Dispalys a specified gif',
        aliases=['jif', 'giphy']
    )
    async def gif_embed(self, ctx, *, gif):
        giphy_url = (
            f'http://api.giphy.com/v1/gifs/search' +
            f'?api_key={self.client.config["giphy"]}' +
            f'&q={quote(gif)}' +
            f'&lang=en'
        )
        async with self.client.session.get(giphy_url) as r:
            if r.status != 200:
                await ctx.send(f'Bad response {ctx.author.mention} 😔')
                return
            gifs = await r.json()
        try:
            gif = random.choice(gifs['data'])['images']['original']['url']
        except IndexError:
            await ctx.send(f'Sorry {ctx.author.mention}, no gifs found 😔')
            await ctx.message.add_reaction('❌')
            return
        e = Embed(title='Gif 😉', color=0x000000)
        e.set_image(url=gif)
        e.set_footer(
            text=ctx.author.display_name,
            icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=e)
        await ctx.message.add_reaction('✅')

    @commands.command(
        brief="For people who don't know how to use Google",
        description='Outputs a lmgtfy link with the given criteria'
    )
    async def lmgtfy(self, ctx, *, terms):
        url = f'http://lmgtfy.com/?q={quote(terms)}'
        e = Embed(title=terms, url=url, color=0x75c5ff)
        await ctx.send(embed=e)

    @commands.command(
        brief='Searches Google',
        aliases=['search', 'find']
    )
    async def google(self, ctx, *, crit):
        goog_url = (
            f'https://www.googleapis.com/customsearch/' +
            f'v1?q={quote(crit)}' +
            f'&cx={self.client.config["google_cx"]}' +
            f'&key={self.client.config["google"]}'
        )
        async with self.client.session.get(goog_url) as r:
            if r.status != 200:
                await ctx.send(f'Bad response {ctx.author.mention} 😔')
                await ctx.message.add_reaction('❌')
                return
            search = await r.json()
        if 'items' not in search:
            await ctx.send(f'Sorry {ctx.author.mention}, no results found 😔')
            await ctx.message.add_reaction('❌')
            return
        if 'cse_thumbnail' in search['items'][0]['pagemap']:
            image = search['items'][0]['pagemap']['cse_thumbnail'][0]['src']
        else:
            image = None
        title = search['items'][0]['title']
        link = search['items'][0]['link']
        snippet = search['items'][0]['snippet']
        timing = search['searchInformation']['formattedSearchTime']
        results = search['searchInformation']['totalResults']

        e = Embed(
            title=title, url=link,
            description=snippet, color=0x4486F4
        )
        if image is not None:
            e.set_thumbnail(url=image)
        e.set_footer(
            text=f'Total results: {results} |' +
            f' Search time: {timing} seconds'
        )
        await ctx.send(embed=e)
        await ctx.message.add_reaction('✅')


def setup(client):
    client.add_cog(Web(client))
