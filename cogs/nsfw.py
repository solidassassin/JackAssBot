import random

from collections import deque
from discord.ext import commands


class Adult(commands.Cog, name="NSFW"):
    def __init__(self, bot):
        self.bot = bot
        self.error_message = "Problems connecting to the API (status code `{}`)"

    async def cog_check(self, ctx):
        return ctx.channel.is_nsfw()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            try:
                nsfw = (i.id for i in ctx.guild.text_channels if i.is_nsfw())
                await ctx.send(f"👉 <#{next(nsfw)}> 👌😩🍆💦")
            except StopIteration:
                await ctx.send("No `NSFW` channels. Pls make one 🍆💦")

    async def nudes(self, subreddit: str, state: str = "rising"):
        url = f"https://reddit.com/r/{subreddit}/{state}.json"

        async with self.bot.session.get(url) as r:
            if (status := r.status) != 200:
                raise commands.CommandError(self.error_message.format(status))
            posts = await r.json()
        return random.choice(posts["data"]["children"])["data"]

    @commands.command()
    async def hentai(self, ctx, img_type="jpg"):
        """Sends a hentai picture.
        Optional parameter: <gif> to send a gif"""
        if img_type.lower() == "gif":
            url = "https://nekos.life/api/v2/img/Random_hentai_gif"
        else:
            url = "https://nekos.life/api/v2/img/hentai"
        async with self.bot.session.get(url) as r:
            if (status := r.status) != 200:
                raise commands.CommandError(self.error_message.format(status))
            hentai = await r.json()
        await ctx.embed(
            title="Hentai 😏",
            color=0xFF75F8,
            image=hentai["url"],
            footer_default=True
        )

    @commands.command(
        name="teen"
    )
    async def teen_pic(self, ctx, state="new"):
        """Sends a nsfw teen picture"""
        post = await self.nudes("LegalTeens", state)
        await ctx.embed(
            title=post["title"],
            color=0xF4428F,
            image=post["url"],
            footer_default=True
        )


def setup(bot):
    bot.add_cog(Adult(bot))
