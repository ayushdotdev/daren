import discord
from discord.ext import commands
import asyncio
import os 
from dotenv import load_dotenv

intents = discord.Intents.default()

cogs = [
  "cogs.general",
  "cogs.util"
  ]

class Client(commands.Bot):
  async def setup_hook(self):
    for cog in cogs:
      await bot.load_extension(cog)
    await bot.tree.sync()

bot = Client(command_prefix = "!", intents = intents)


@bot.event
async def on_ready():
  await bot.change_presence(
    activity = discord.Activity(type = discord.ActivityType.listening, name = "/help")
    )
  print(f"Logged in as {bot.user}")
  
if __name__ == "__main__":
  load_dotenv()
  bot.run(os.getenv('BOT_TOKEN'))