from discord.ext import commands
import discord
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
        
        
    def test(self):
        subreddit = self.KEY.subreddit(self.subred)
        rPosts = subreddit.hot(limit=50)
        rPost = random.choice([f'{s.title}\n{s.url}' for s in rPosts])
        return rPost


class Beautiful:

    def __init__(self, terms):
        self.terms = terms

    def results(self):
        data = requests.get(f'http://www.euroleague.net/competition/teams/showteam?clubcode={self.terms}&seasoncode=E2018#!games')
        soup = BeautifulSoup(data.text, 'lxml')
        game = soup.find('span', {'class': 'TeamPhaseGamesRecord'})
        return game.text

    def urls(self):
        response = requests.get(f"http://api.giphy.com/v1/gifs/search?api_key={config['giphy']}&q={self.terms}&limit=20").json()

        data = [response['data'][i]['images']['original']['url'] for i in range(len(response['data']))]
        final = random.choice(data)
        
        return final


class Web:

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
            await ctx.send(p.test())
        except:
            await ctx.send('Sorry Chief, did not find a subreddit named like that')

    @commands.command(
    brief='Dispalys a specified gif',
    description="Outputs the specified gif's url",
    aliases=['giphy']
    )
    async def gif(self, ctx, *, gif):
        g = Beautiful(f'{gif}')
        await ctx.send(g.urls())


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