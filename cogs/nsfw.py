import random

from discord.ext import commands


class Adult(commands.Cog, name='NSFW'):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return ctx.channel.is_nsfw()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            try:
                nsfw = (i.id for i in ctx.guild.text_channels if i.is_nsfw())
                await ctx.send(f"👉 <#{next(nsfw)}> 👌😩🍆💦")
            except StopIteration:
                await ctx.send('No `NSFW` channels. Pls make one 🍆💦')

    async def nudes(self, subreddit, file_type=('jpg', 'png', 'gif')):
        url = f'https://api.imgur.com/3/gallery/r/{subreddit}/new'
        headers = {
            'Authorization':
            f'Client-ID {self.client.config.imgur_clientid}'
        }
        async with self.client.session.get(url, headers=headers) as r:
            if r.status != 200:
                raise commands.CommandInvokeError(
                    self.client.BAD_RESPONSE
                )
            pics = await r.json()
        while True:
            pic = random.choice(pics['data'])['link']
            if pic[-3:] in file_type:
                break
        return pic

    @commands.command()
    async def hentai(self, ctx, gif='jpg'):
        """
        Sends a hentai picture.
        Optional parameter: <gif> to send a gif
        """
        if gif.lower() == 'gif':
            url = 'https://nekos.life/api/v2/img/Random_hentai_gif'
        else:
            url = 'https://nekos.life/api/v2/img/hentai'
        async with self.client.session.get(url) as r:
            if r.status != 200:
                raise commands.CommandInvokeError(
                    self.client.BAD_RESPONSE
                )
            hentai = await r.json()
        await ctx.embed(
            title='Hentai 😏',
            color=0xff75f8,
            image=hentai['url'],
            footer_default=True
        )

    @commands.command(
        name='teen',
    )
    async def teen_pic(self, ctx, gif='jpg'):
        """
        Sends a petite teen picture.
        Optional parameter: <gif> to send a gif
        """
        if gif == 'gif':
            pic = await self.nudes('FreshGIF', ('gif',))
        else:
            pic = await self.nudes('LegalTeens', ('jpg', 'png'))
        await ctx.embed(
            title='Teen 😉',
            color=0xf4428f,
            image=pic,
            footer_default=True
        )


def setup(client):
    client.add_cog(Adult(client))
