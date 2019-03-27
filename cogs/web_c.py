from discord.ext import commands
from discord import Embed, Color
from urllib.parse import quote as quote_uri  # to avoid problems with some searches
import requests
import praw  # didn't want to bother with reddit's API
import random
import json


with open('data/config.json') as keys:
    config = json.load(keys)

KEY = praw.Reddit(client_id=config['reddit_id'],
                  client_secret=config['reddit_secret'],
                  password=config['reddit_password'],
                  user_agent='testscript by /u/JackAssBot',
                  username='JackAssBot')


class Scrape:

    def __init__(self, terms):
        self.terms = quote_uri(terms)

    def test(self):  # TODO: add exception
        subreddit = KEY.subreddit(self.terms)
        rPosts = subreddit.hot(limit=50)
        rPost = random.choice([[s.title, s.url] for s in rPosts])
        title, link = rPost[0], rPost[1]
        return title, link

    def urls(self):
        try:
            gifs = requests.get(f"http://api.giphy.com/v1/gifs/search?api_key={config['giphy']}&q=\
                {self.terms}&limit=20").json()

            data = random.choice([[gifs['data'][i]['title'],
                                 gifs['data'][i]['images']['original']['url']]
                                 for i in range(len(gifs['data']))])

            title, gif = data[0], data[1]
            return title, gif
        except IndexError:  # for when no results are returned
            pass

    def goog(self):
        try:
            search = requests.get(f"https://www.googleapis.com/customsearch/v1?q={self.terms}\
                &cx={config['google_cx']}&key={config['google']}").json()

            title, link, snippet = search['items'][0]['title'], search['items'][0]['link'], search['items'][0]['snippet']
            timing, results = search['searchInformation']['formattedSearchTime'], search['searchInformation']['totalResults']
            try:
                image = search['items'][0]['pagemap']['cse_thumbnail'][0]['src']
            except KeyError:
                image = None

            return title, link, snippet, image, timing, results

        except KeyError:
            pass


class Web(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(
        name='subreddit',
        brief='Displays a random post from the specified subreddit',
        description='Outupts the title and url of a random post from the \
            hot page of the specified subreddit (out of 50 posts)',
        aliases=['reddit']
    )
    async def subred(self, ctx, subreddit):
        try:
            p = Scrape(subreddit)
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
        g = Scrape(gif)
        gg = g.urls()
        if gg is None:
            await ctx.send(f'Sorry {ctx.author.mention}, no gifs found 😔')
            await ctx.message.add_reaction('❌')
        else:
            e = Embed(title=gg[0], color=0x000000)
            e.set_image(url=gg[1])
            e.set_footer(text=ctx.author.display_name,
                         icon_url=ctx.author.avatar_url)

            await ctx.send(embed=e)
            await ctx.message.add_reaction('✅')

    @commands.command(
        brief="For people who don't know how to use Google",
        description='Outputs a lmgtfy link with the given criteria',
        aliases=['lemme google']
    )
    async def lmgtfy(self, ctx, *, terms):
        lmg = f'http://lmgtfy.com/?q={quote_uri(terms)}'
        e = Embed(title=terms, url=lmg, color=Color.blue())
        await ctx.send(embed=e)

    @commands.command(
        brief='Searches Google',
        aliases=['search', 'find']
    )
    async def google(self, ctx, *, crit):
        g = Scrape(crit)
        gg = g.goog()
        if gg is None:
            await ctx.send(f'Sorry {ctx.author.mention}, nothing found 😔')
            await ctx.message.add_reaction('❌')
        else:
            e = Embed(title=gg[0], url=gg[1], description=gg[2],
                      color=Color.blue())
            if gg[3] is not None:
                e.set_thumbnail(url=gg[3])
            e.set_footer(text=f'Total results: {gg[5]} | \
                Search time: {gg[4]} seconds')

            await ctx.send(embed=e)
            await ctx.message.add_reaction('✅')


def setup(client):
    client.add_cog(Web(client))
