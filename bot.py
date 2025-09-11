import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os 
from dotenv import load_dotenv

intents = discord.Intents.default()

cogs = [
  "cogs.general",
  "cogs.util",
  "cogs.moderation"
  ]

class Client(commands.Bot):
  async def setup_hook(self):
    for cog in cogs:
      await bot.load_extension(cog)
    await bot.tree.sync()

bot = Client(command_prefix = "!", intents = intents, help_command = None)

@bot.tree.error
async def on_app_commmand_error(interactions: discord.interactions,error: app_commands.AppCommandError):
  if isinstance(error, app_commands.MissingPermissions):
    error = discord.Embed(
      color = 0xed2939,
      description = f"<:darenError:1415768665642766407> **_You do not have enough permissions to use this command._**"
      )
    await interactions.response.send_message(embed = error, ephemeral = True)


@bot.event
async def on_ready():
  await bot.change_presence(
    activity = discord.Activity(type = discord.ActivityType.listening, name = "/help")
    )
  print(f"Logged in as {bot.user}")
  
if __name__ == "__main__":
  load_dotenv()
  bot.run(os.getenv('BOT_TOKEN'))