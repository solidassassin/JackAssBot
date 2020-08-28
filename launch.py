from discord.ext.commands import when_mentioned_or

from bot import JackassBot


bot = JackassBot(
    command_prefix=when_mentioned_or("dad ", "Dad "),
    case_insensitive=True
)

bot.run()
