from discord import Embed, Color
from discord.ext import commands


# work in progress
class Context(commands.Context):
    def __init__(self, **attrs):
        super().__init__(**attrs)

    # testing, decreased functionality
    async def embed(self, **attrs):
        e = Embed(
            title=attrs.get('title'),
            color=attrs.get('color', Color.blurple()),
            description=attrs.get('description'),
            url=attrs.get('url')
        )
        if 'image' in attrs:
            e.set_image(url=attrs['image'])
        if attrs.get('thumbnail') is not None:
            e.set_thumbnail(url=attrs['thumbnail'])
        # I usually only put the text when I want something custom
        if 'footer_text' in attrs:
            e.set_footer(text=attrs['footer_text'])
        else:
            e.set_footer(
                text=self.author.display_name,
                icon_url=self.author.avatar_url
            )
        if 'header_text' in attrs:
            e.set_author(
                name=attrs['header_text'],
                icon_url=attrs['header_icon']
            )
        # fields will be a list of dicts
        if 'fields' in attrs:
            for i in attrs['fields']:
                e.add_field(
                    name=i['name'],
                    value=i['value'],
                    inline=i.get('inline', True)
                )
        await self.send(embed=e)
