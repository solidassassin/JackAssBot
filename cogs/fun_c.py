from discord.ext import commands
from discord import Embed
import random
import json


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(
        brief='Rolls a six-sided dice',
        description='Displays a number after' +
        ' randomly selecting it from 6 sides',
        aliases=['roll']
    )
    async def dice(self, ctx):
        d = random.choice(range(1, 7))
        await ctx.send(d)

    @commands.command(
        brief="Repeats the user's words",
        description='Copies everything you type after the command',
        aliases=['follow'],
        hidden=True
    )
    async def repeat(self, ctx, *, sentence):
        await ctx.send(f'{ctx.author.mention} said: {sentence}')

    @commands.command(
        brief='Answers a yes/no question',
        description='Outputs a response to a yes or no question',
        aliases=['8ball', 'question:']
    )
    async def question(self, ctx):
        with open('data/responses.json', 'r') as res:
            file = json.load(res)
        answer = random.choice(file)
        await ctx.send(answer)

    @commands.command(
        name='fact',
        brief='Random fact',
        description='Gives the user a random fact'
    )
    async def fact(self, ctx):
        url = 'https://nekos.life/api/v2/fact'
        img_url = 'https://i.ytimg.com/vi/GD6qtc2_AQA/maxresdefault.jpg'
        async with self.client.session.get(url) as r:
            if r.status != 200:
                await ctx.send(f'Bad response {ctx.author.mention} 😔')
                return
            fact = await r.json()
        e = Embed(title=fact['fact'], color=0x000000)
        e.set_image(url=img_url)
        await ctx.send(embed=e)


def setup(client):
    client.add_cog(Fun(client))
