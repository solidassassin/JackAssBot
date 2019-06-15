from discord.ext.commands import when_mentioned_or

from bot import JackassBot


client = JackassBot(
    command_prefix=when_mentioned_or('jack ', 'Jack '),
    case_insensitive=True
)

client.run()
