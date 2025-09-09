import discord
from discord.ext import commands
import asyncio
import os 
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

class Client(commands.Bot):
  async def setup_hook(self):
    await bot.load_extension("cogs.general")
    await bot.tree.sync()

bot = Client(command_prefix = "!", intents = intents)


@bot.event
async def on_ready():
  print(f"Logged in as {bot.user}")
  
if __name__ == "__main__":
  load_dotenv()
  bot.run(os.getenv('BOT_TOKEN'))