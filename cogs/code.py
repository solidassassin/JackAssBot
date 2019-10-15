import json

from discord.ext import commands


with open('data/languages.json') as f:
    languages = json.load(f)


class Code(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bad_format = "No code found, make sure you're using codeblocks"
        self.unsupported = "The specified language is not supported"
        self.lang_list = sorted(languages.keys())

    async def block_cleanup(self, user_input):
        try:
            params = user_input.split('\n', 1)
            language = params[0].strip().lower()
            block = params[1]
        except ValueError:
            raise commands.BadArgument(self.bad_format)

        if not (block.startswith('```') and block.endswith('```')):
            raise commands.BadArgument(self.bad_format)
        else:
            block_strip = block.split('\n')[1:-1]
            block_clean = '\n'.join(block_strip)
        if language not in self.lang_list:
            return self.unsupported
        else:
            version = languages[language]
        return block_clean, language, version

    @commands.command(
        name='run',
        aliases=('execute', 'code')
    )
    async def jdoodle(self, ctx, *, code_raw):
        """
        A command to execute your provided code.
        Example input:
        *jack run python3
        \\`\\`\\`[language here]
        print('Hello world!')
        \\`\\`\\`*
        """
        code = await self.block_cleanup(code_raw)
        if code == self.unsupported:
            await ctx.send(
                f"{self.unsupported}\n" +
                f"Here's a list of supported languages:\n" +
                f"```{', '.join(self.lang_list)}```"
            )
            return
        payload = {
            'clientId': self.bot.config.jdoodleClientId,
            'clientSecret': self.bot.config.jdoodleClientSecret,
            'script': code[0],
            'language': code[1],
            'versionIndex': code[2]
        }
        data = json.dumps(payload)

        url = 'https://api.jdoodle.com/v1/execute'
        headers = {'content-type': 'application/json'}
        async with ctx.typing():
            async with self.bot.session.post(
                url,
                data=data,
                headers=headers
            ) as r:
                if r.status != 200:
                    raise commands.CommandInvokeError(
                        self.bot.BAD_RESPONSE
                    )
                output = await r.json()

            if len(output) > 1990:
                await ctx.send(
                    f'Sorry {ctx.author.mention}, your output is too long.'
                )
                return
            await ctx.send(f'```\n{output["output"]}\n```')


def setup(bot):
    bot.add_cog(Code(bot))
