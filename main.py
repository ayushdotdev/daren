import os
from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.message_content = True

def get_prefix(bot,message):
  return commands.when_mentioned_or("!")(bot,message)
  
bot = commands.Bot(command_prefix = get_prefix, intents = intents)

@bot.event()
async def on_ready():
  print(f'logged in as {bot.user.name}')
  await bot.change_presence(
    activity = nextcord.GAME(name = "@Daren help")
    )
    
if __name__ = "__main__":
  load_dotenv()
  bot_token = os.getenv('BOT_TOKEN')
  bot.run(bot_token)