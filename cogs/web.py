import random
from urllib.parse import quote

from discord.ext import commands


class Web(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def giphy_results(self, gif):
        giphy_url = (
            f'http://api.giphy.com/v1/gifs/search' +
            f'?api_key={self.client.config.giphy}' +
            f'&q={quote(gif)}' +
            f'&lang=en'
        )
        async with self.client.session.get(giphy_url) as r:
            if r.status != 200:
                raise commands.CommandInvokeError(
                    self.client.BAD_RESPONSE
                )
            gifs = await r.json()
        try:
            gif = random.choice(gifs['data'])['images']['original']['url']
        except IndexError:
            raise commands.CommandInvokeError(
                self.client.NO_RESULTS
            )
        return gif

    async def google_results(self, search):
        goog_url = (
            f'https://www.googleapis.com/customsearch/' +
            f'v1?q={quote(search)}' +
            f'&cx={self.client.config.google_cx}' +
            f'&key={self.client.config.google}'
        )
        async with self.client.session.get(goog_url) as r:
            if r.status != 200:
                raise commands.CommandInvokeError(
                    self.client.BAD_RESPONSE
                )
            search = await r.json()
        if 'items' not in search:
            raise commands.CommandInvokeError(
                self.client.NO_RESULTS
            )
        if 'cse_thumbnail' in search['items'][0]['pagemap']:
            image = search['items'][0]['pagemap']['cse_thumbnail'][0]['src']
        else:
            image = None
        title = search['items'][0]['title']
        link = search['items'][0]['link']
        snippet = search['items'][0]['snippet']
        timing = search['searchInformation']['formattedSearchTime']
        results = search['searchInformation']['totalResults']
        return title, link, snippet, image, results, timing

# -----------commands--------------
    @commands.command(
        name='gif',
        aliases=('jif', 'giphy')
    )
    async def gif_embed(self, ctx, *, gif):
        """Dispalys a specified gif."""
        final = await self.giphy_results(gif)
        await ctx.embed(
            image=final,
            color=0x000000,
            footer_default=True
        )

    @commands.command()
    async def lmgtfy(self, ctx, *, terms):
        """For people who don't know how to use Google.
        A.K.A lmgtfy link"""
        url = f'http://lmgtfy.com/?q={quote(terms)}'
        await ctx.embed(
            title=terms,
            url=url,
            color=0x000000
        )

    @commands.command(
        name='google',
        aliases=('search', 'find')
    )
    async def google(self, ctx, *, criteria):
        """A Google search of the provided criteria."""
        async with ctx.typing():
            info = await self.google_results(criteria)
            await ctx.embed(
                title=info[0],
                url=info[1],
                description=info[2],
                color=0x3498db,
                thumbnail=info[3],
                footer_text=(
                    f'Total results: {info[4]} |' +
                    f' Search time: {info[5]} seconds'
                )
            )


def setup(client):
    client.add_cog(Web(client))
