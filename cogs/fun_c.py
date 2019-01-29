from discord.ext import commands
import discord
import random
import json

class Fun:

    def __init__(self, client):
        self.client = client


    @commands.command(
        brief='Rolls a six-sided dice',
        description='Displays a number after randomly selecting it from 6 sides',
        aliases=['roll']
    )
    async def dice(self, ctx):
        d = random.choice(range(1, 7))
        await ctx.send(d)


    @commands.command(
        brief="Repeats the user's words",
        description='Copies everything you type after the command',
        aliases=['follow']
    )
    async def repeat(self, ctx, *, sentence):
        await ctx.send(f'<@{ctx.message.author.id}> said: {sentence}')


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

def setup(client):
    client.add_cog(Fun(client))