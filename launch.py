from discord.ext.commands import when_mentioned_or

from bot import JackassBot


bot = JackassBot(
    command_prefix=when_mentioned_or("jack ", "Jack "),
    case_insensitive=True
)

bot.run()
