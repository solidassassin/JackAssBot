# cog management commands are a mess, will be cleaned
import logging

from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return await ctx.bot.is_owner(ctx.author)

    @commands.command(
        name='unload',
        hidden=True
    )
    async def unload_cog(self, ctx, ext):
        """
        Unloads a specified cog.
        """
        ext = f'cogs.{ext}'
        if ext in self.client.extensions.keys():
            try:
                self.client.unload_extension(ext)
                await ctx.send(f'```ini\n[{ext}] unloaded\n```')
            except commands.ExtensionError:
                await ctx.send(f'```css\n[{ext}] unload failed\n```')
                logging.exception(f'{ext} failed to unload')
            return
        await ctx.send('Cog not loaded.')

    @commands.command(
        name='load',
        hidden=True
    )
    async def load_cog(self, ctx, ext):
        """
        Unloads a specified cog.
        """
        ext = f'cogs.{ext}'
        if ext in self.client.all_cogs:
            try:
                self.client.load_extension(ext)
                await ctx.send(f'```ini\n[{ext}] loaded\n```')
            except commands.ExtensionError:
                await ctx.send(f'```css\n[{ext}] load failed\n```')
                logging.exception(f'{ext} failed to load')
            return
        await ctx.send('Cog not found.')

    @commands.command(
        name='reload',
        hidden=True
    )
    async def reload_cog(self, ctx, ext='all'):
        """
        Reloads all, or a specified cog.
        """
        ext = f'cogs.{ext}'
        info = '```ini\n'
        if ext == 'cogs.all':
            for i in self.client.all_cogs:
                try:
                    self.client.reload_extension(i)
                    info += f'[{i}] reloaded\n'
                except commands.ExtensionError:
                    info += f'[{i}] reload failed\n'
                    logging.exception()
            await ctx.send(f'{info}```')
            return
        elif ext in self.client.all_cogs:
            try:
                self.client.reload_extension(ext)
                info += f'[{ext}] reloaded\n'
            except commands.ExtensionError:
                info += f'[{ext}] reload failed\n'
                logging.exception()
            await ctx.send(f'{info}```')
            return
        await ctx.send("Cog doesn't exsist.")

    @commands.command(
        aliases=['goodbye', 'die'],
        hidden=True
    )
    async def logout(self, ctx):
        """
        Disable bot.
        """
        await ctx.send('See ya bitch!')
        await self.client.logout()


def setup(client):
    client.add_cog(Owner(client))
