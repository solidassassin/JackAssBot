import json
import re
import typing

from discord import Embed
from discord.ext import commands


with open("data/languages.json") as f:
    languages = json.load(f)


class Code(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.aliases = languages.keys()
        self.lang_set = set([*self.aliases, *languages.values()])

    def process_input(self, content):
        data = re.search(
            r"(?:\b\w+\b[\s\r\n]*){2}(\w+)?[\s\r\n]+```(?:(\w+)\n)?(.+)```",
            content, re.S
        )
        if not data:
            raise commands.BadArgument("No text detected.")
        data = data.groups()
        lang = data[0] or data[1]

        if not (code := data[2]):
            raise commands.BadArgument("No code present.")
        if not (lang and lang in self.lang_set):
            raise commands.BadArgument("Unsupported language provided.")
        if lang in self.aliases:
            lang = languages[lang]

        return lang, code

    @commands.command(
        aliases=("execute", "code")
    )
    async def run(self, ctx):
        """Executes user code."""
        language, code = self.process_input(ctx.message.clean_content)

        url = "https://emkc.org/api/v1/piston/execute"
        data = {
            "language": language,
            "source": code
        }

        async with self.bot.session.post(url, data=data) as r:
            if (status := r.status) != 200:
                raise commands.CommandError(
                    self.bot.error_messages["api"].format(status)
                )
            response = await r.json()
        if len((output := response["output"])) > 1980:
            output = output[:1980]
        if len((splited := output.split("\n"))) > 40:
            output = "\n".join(splited[:40])

        await ctx.send(f"```\n{output}\n...\n```")


def setup(bot):
    bot.add_cog(Code(bot))
