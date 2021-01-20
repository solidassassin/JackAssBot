import unicodedata
from urllib.parse import quote

from discord import Emoji, Member
from discord.ext import commands


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def char_info(self, char):
        name = unicodedata.name(char, None)
        if not name:
            raise commands.CommandError(
                self.bot.error_messages["no_results"].format(char)
            )
        code = f"{ord(char):x}"
        name_url = name.lower().replace(" ", "-")
        url = f"https://emojipedia.org/{name_url}"
        about = (
            f"**Hex:** {code}\n"
            f"**Python:** \\N{{{name}}}"
        )
        return name, url, about

    async def urban(self, word) -> dict:
        url = f"http://api.urbandictionary.com/v0/define?term={quote(word)}"
        async with self.bot.session.get(url) as r:
            if (status := r.status) != 200:
                raise commands.CommandError(
                    self.bot.error_messages["api"].format(status)
                )
            answer = await r.json()
        if not answer["list"]:
            raise commands.CommandError(
                self.bot.error_messages["no_results"].format(word)
            )
        definition = answer["list"][0]["definition"]
        example = answer["list"][0]["example"]
        for i in ("[", "]"):
            definition = definition.replace(i, "")
            example = example.replace(i, "")
        if len(definition) > 1000:
            definition = f"{definition[:1000]}..."
        fields = {"Definition:": definition}
        if example:
            fields["Example:"] = example
        return fields, url

    @commands.command(
        aliases=("emoji",)
    )
    async def emote(self, ctx, emoji: Emoji):
        """Enlarges the provided emoji.
        It has to be a custom emote (not unicode)."""
        await ctx.embed(
            color=0xffff00,
            image=emoji.url,
            footer_default=True
        )

    @commands.command(
        name="avatar",
        aliases=("profile",)
    )
    async def avatar_info(self, ctx, member: Member = None):
        """Returns an image of the user's avatar"""
        if not member:
            member = ctx.author
        await ctx.embed(
            image=member.avatar_url,
            footer_default=True
        )

    @commands.command(
        aliases=("member",)
    )
    async def memberinfo(self, ctx, member: Member = None):
        """Provides information about the given member."""
        if not member:
            member = ctx.author
        fields = {
            "Username:": str(member),
            "Status:": str(member.status).title(),
            "Account created at:": member.created_at.strftime("%Y/%m/%d"),
            "Top role:": member.top_role.mention
            if str(member.top_role) != "@everyone" else "@everyone",
            "Joined at:": member.joined_at.strftime("%Y/%m/%d"),
            "Current activities:": "\n".join(i.name for i in member.activities)
            if member.activities else "No current activities"
        }
        await ctx.embed(
            color=member.color,
            thumbnail=member.avatar_url,
            fields=fields,
            footer_default=True
        )

    @commands.command(
        name="ping",
        aliases=("latency",)
    )
    async def latency_info(self, ctx):
        """Latency of the bot in miliseconds."""
        ping = round(self.bot.latency * 1000, 2)
        await ctx.embed(
            title=f"Pong!",
            description=f"🏓 `{ping}ms`"
        )

    @commands.command(
        name="char",
        aliases=("charinfo", "unicode")
    )
    async def char_send(self, ctx, char: str):
        """Provides information about the given unicode char."""
        info = await self.char_info(char)
        await ctx.embed(
            title=f"{info[0]} {char}",
            url=info[1],
            description=info[2]
        )

    @commands.command(
        name="definition",
        aliases=("urbandict", "urban")
    )
    async def urbandictionary(self, ctx, *, word):
        """Shows the definition of the provided word."""
        await ctx.trigger_typing()
        fields, url = await self.urban(word)
        await ctx.embed(
            title=word.title(),
            url=url,
            color=0x1D2439,
            fields=fields,
            inline=False,
            footer_default=True
        )


def setup(bot):
    bot.add_cog(Utility(bot))
