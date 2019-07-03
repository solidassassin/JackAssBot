from discord import Embed, Color
from discord.ext import commands


class Context(commands.Context):
    @property
    def session(self):
        return self.bot.session

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

        if attrs.get('footer_default'):
            e.set_footer(
                text=self.author.display_name,
                icon_url=self.author.avatar_url
            )
        elif 'footer_text' in attrs and 'footer_icon' in attrs:
            e.set_footer(
                text=attrs['footer_text'],
                icon_url=attrs['footer_icon']
            )
        elif 'footer_text' in attrs:
            e.set_footer(text=attrs['footer_text'])

        if 'header_text' in attrs and 'header_icon' in attrs:
            e.set_author(
                name=attrs['header_text'],
                icon_url=attrs['header_icon']
            )
        elif 'header_text' in attrs:
            e.set_author(name=attrs['header_text'])

        # fields will be a dictionary
        if 'fields' in attrs:
            inline = attrs.get('inline', True)
            for name, value in attrs['fields'].items():
                e.add_field(
                    name=name,
                    value=value,
                    inline=inline
                )

        await self.send(embed=e)
