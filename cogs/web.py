import random
from urllib.parse import quote

from discord.ext import commands


class Web(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def giphy_results(self, gif):
        giphy_url = (
            "http://api.giphy.com/v1/gifs/search"
            f"?api_key={self.bot.config.giphy}"
            f"&q={quote(gif)}"
            "&lang=en"
        )
        async with self.bot.session.get(giphy_url) as r:
            if (status := r.status) != 200:
                raise commands.CommandError(
                    self.bot.error_messages["api"].format(status)
                )
            gifs = await r.json()
        try:
            gif = random.choice(gifs["data"])["images"]["original"]["url"]
        except IndexError:
            raise commands.CommandError(
                self.bot.error_messages["no_results"].format(gif)
            )
        return gif

    async def google_results(self, search):
        goog_url = (
            "https://www.googleapis.com/customsearch/"
            f"v1?q={quote(search)}"
            f"&cx={self.bot.config.google_cx}"
            f"&key={self.bot.config.google}"
        )
        async with self.bot.session.get(goog_url) as r:
            if (status := r.status) != 200:
                raise commands.CommandError(
                    self.bot.error_messages["api"].format(status)
                )
            search = await r.json()
        if "items" not in search:
            raise commands.CommandError(
                self.bot.error_messages["no_results"].format(search)
            )
        if "cse_thumbnail" in search["items"][0]["pagemap"]:
            image = search["items"][0]["pagemap"]["cse_thumbnail"][0]["src"]
        else:
            image = None
        title = search["items"][0]["title"]
        link = search["items"][0]["link"]
        snippet = search["items"][0]["snippet"]
        return title, link, snippet, image

# -----------commands--------------
    @commands.command(
        name="gif"
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
        url = f"http://lmgtfy.com/?q={quote(terms)}"
        await ctx.embed(
            title=terms,
            url=url,
            color=0x000000
        )

    @commands.command(
        name="google",
        aliases=("search", "find")
    )
    async def google(self, ctx, *, criteria):
        """A Google search of the provided criteria."""
        async with ctx.typing():
            info = await self.google_results(criteria)
            await ctx.embed(
                title=info[0],
                url=info[1],
                description=info[2],
                color=0x04aad4,
                thumbnail=info[3],
                footer_default=True
            )


def setup(bot):
    bot.add_cog(Web(bot))
