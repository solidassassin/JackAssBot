import json
import random

from discord.ext import commands


with open("data/responses.json", "r") as f:
    responses = json.load(f)


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="flip",
        aliases=("coin",)
    )
    async def coin_flip(self, ctx):
        """Flips a coin."""
        flip = random.choice(("Heads", "Tails"))
        await ctx.send(f"**{flip}**")

    @commands.command(
        aliases=("8ball", "question:")
    )
    async def should(self, ctx):
        """Sends a response to a yes or no question."""
        answer = random.choice(responses)
        await ctx.send(answer)

    @commands.command(
        name="fact"
    )
    async def fact(self, ctx):
        """Shows a random fact."""
        url = "https://nekos.life/api/v2/fact"
        img_url = "https://i.ytimg.com/vi/GD6qtc2_AQA/maxresdefault.jpg"
        async with self.bot.session.get(url) as r:
            if r.status != 200:
                raise commands.CommandInvokeError(
                    self.bot.BAD_RESPONSE
                )
            fact = await r.json()
        await ctx.embed(
            title=fact["fact"],
            color=0x000000,
            image=img_url
        )


def setup(bot):
    bot.add_cog(Fun(bot))
