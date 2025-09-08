import discord
import os 
from dotenv import load_dotenv

bot = discord.Bot()

cogs = [
  "cogs.general"
  ]

@bot.event
async def on_ready():
  for cog in cogs:
    bot.load_extension(cog)
  print(f'Logged in as {bot.user}')
  
if __name__ == "__main__":
  load_dotenv()
  token = os.getenv('BOT_TOKEN')
  bot.run(token)