import json
import re

from urllib.parse import quote
from collections import OrderedDict
from discord.ext import commands


with open("data/languages.json") as f:
    languages = json.load(f)


class Code(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.aliases = languages.keys()
        self.lang_set = set([*self.aliases, *languages.values()])
        # message_id | response_message_object
        self.history = OrderedDict()

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

    async def fetch_content(self, language, code):
        url = "https://emkc.org/api/v1/piston/execute"
        data = {
            "language": language,
            "source": code
        }
        if language in ("ltx", "latex"):
            lnk = r"https://latex.codecogs.com/png.latex?%5Chuge%5Ccolor%7Bwhite%7D"
            return lnk + quote(code)

        async with self.bot.session.post(url, data=data) as r:
            if (status := r.status) != 200:
                raise commands.CommandError(
                    self.bot.error_messages["api"].format(status)
                )
            response = await r.json()
        if len((output := response["output"])) > 1980:
            output = output[:1980] + "\n..."
        if len((splited := output.split("\n"))) > 40:
            output = "\n".join(splited[:40])

        return f"```\n{output}\n```"

    @commands.Cog.listener()
    async def on_message_edit(self, _, after):
        if (id_ := after.id) not in self.history:
            return
        message = self.history[id_]
        new_content = await self.fetch_content(
            *self.process_input(after.clean_content)
        )
        await message.edit(content=new_content)

    @commands.command(
        aliases=("execute", "code")
    )
    async def run(self, ctx):
        """Executes user code."""
        content = await self.fetch_content(
            *self.process_input(ctx.message.clean_content)
        )

        msg = await ctx.send(content)

        if len(self.history) >= 20:
            self.history.popitem(last=False)
        self.history[ctx.message.id] = msg


def setup(bot):
    bot.add_cog(Code(bot))
