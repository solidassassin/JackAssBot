from discord.ext import commands
from discord import Embed
import praw # didn't want to bother with reddit's API for now
import random
import requests
from bs4 import BeautifulSoup
import json


with open('data/config.json') as keys:
    config = json.load(keys)

class Posts:


    KEY = praw.Reddit(client_id=config['reddit_id'],
                      client_secret=config['reddit_secret'],
                      password=config['reddit_password'],
                      user_agent='testscript by /u/JackAssBot',
                      username='JackAssBot')


    def __init__(self, subred):
        self.subred = subred
        
        
    def test(self):  # TODO: add exception
        subreddit = self.KEY.subreddit(self.subred)
        rPosts = subreddit.hot(limit=50)
        rPost = random.choice([[s.title, s.url] for s in rPosts])
        title, link = rPost[0], rPost[1]
        return title, link


class Beautiful:  # TODO: Add scrapping for google search

    def __init__(self, terms):
        self.terms = terms

    def results(self):
        data = requests.get(f'http://www.euroleague.net/competition/teams/showteam?clubcode=\
            {self.terms}&seasoncode=E2018#!games')
        soup = BeautifulSoup(data.text, 'lxml')
        game = soup.find('span', {'class': 'TeamPhaseGamesRecord'})
        return game.text

    def urls(self):
        try:
            gifs = requests.get(f"http://api.giphy.com/v1/gifs/search?api_key={config['giphy']}&q=\
                {self.terms}&limit=20").json()

            data = random.choice([[gifs['data'][i]['title'], 
                gifs['data'][i]['images']['original']['url']] for i in range(len(gifs['data']))])

            title, gif = data[0], data[1]
            return title, gif
        except IndexError:  # for when no results are returned
            pass


class Web(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(
    name='subreddit',
    brief='Displays a random post from the specified subreddit',
    description='Outupts the title and url of a random post from the hot page of the specified subreddit (out of 50 posts)',
    aliases=['reddit']
    )
    async def subred(self, ctx, subreddit):
        try:
            p = Posts(f'{subreddit}')
            embed1 = Embed(title=p.test()[0], color=0xFF6A33)
            embed1.set_image(url=p.test()[1])
            embed1.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed1)
            await ctx.message.add_reaction('✅')
        except Exception:
            await ctx.send('Sorry Chief, did not find a subreddit named like that')
            await ctx.message.add_reaction('❌')


    @commands.command(
        name='gif',
        brief='Dispalys a specified gif',
        aliases=['jif', 'giphy']
    )
    async def gif_embed(self, ctx, *, gif):
        g = Beautiful(gif)
        gg = g.urls()
        if gg == None:
            await ctx.send(f'Sorry <@{ctx.message.author.id}>, no gifs found 😔')
            await ctx.message.add_reaction('❌')
        else:
            e = Embed(title=gg[0], color=0x000000)
            e.set_image(url=gg[1])
            e.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)

            await ctx.send(embed=e)
            await ctx.message.add_reaction('✅')

    # TODO: edit the search command to display first results in the channel
    @commands.command(
    brief='Searches given keywords on Google',
    description='Outputs a Google the search result with the given criteria',
    aliases=['search']
    )
    async def google(self, ctx, *, terms):
        gg = terms.replace(' ', '+')
        await ctx.send(f'Here: https://www.google.com/search?q={gg}\nNow leave me alone')


    @commands.command(
    brief="Displays the selected team's stats"
    )
    async def team(self, ctx, ratio):
        try:
            ratio = ratio.upper()
            t = Beautiful(f'{ratio}')
            await ctx.send(f'{ratio} has: {t.results()}')
        except:
            await ctx.send("Are you sure that's a valid Euroleague team code?\nDid not find anything")

    
def setup(client):
    client.add_cog(Web(client))