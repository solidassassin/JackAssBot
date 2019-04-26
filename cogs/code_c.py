from discord.ext import commands
import json


with open('data/languages.json') as f:
    languages = json.load(f)


class Codeblocks:
    bad_format = "No code found, make sure you're using codeblocks"

    def __init__(self, user_input):
        try:
            params = user_input.split('\n', 1)
            language = params[0].strip().lower()
            block = params[1]
        except ValueError:
            raise commands.BadArgument(self.bad_format)

        if not block.startswith('```') and not block.endswith('```'):
            raise commands.BadArgument(self.bad_format)
        else:
            block_strip = block.split('\n')[1:-1]
            self.block_clean = '\n'.join(block_strip)
        if language not in languages:
            raise commands.BadArgument(self.bad_format)
        else:
            self.lang = language
            self.v = languages[language]


class Code(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(
        name='run',
        brief='Execute code',
        aliases=['execute']
    )
    async def jdoodle(self, ctx, *, code: Codeblocks):
        payload = {
            'clientId': self.client.config['clientId'],
            'clientSecret': self.client.config['clientSecret'],
            'script': code.block_clean,
            'language': code.lang,
            'versionIndex': code.v
        }
        data = json.dumps(payload)

        url = 'https://api.jdoodle.com/v1/execute'
        h = {'content-type': 'application/json'}
        async with ctx.typing():
            async with self.client.session.post(url, data=data, headers=h) as r:
                if r.status != 200:
                    await ctx.send(f'Bad response {ctx.author.mention} 😔')
                    return
                output = await r.json()

            if len(output) > 1990:
                await ctx.send(f'Sorry {ctx.author.mention}, your output is too long.')
            else:
                await ctx.send(f'```\n{output["output"]}\n```')


def setup(client):
    client.add_cog(Code(client))
