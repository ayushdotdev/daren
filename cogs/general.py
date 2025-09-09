import discord
from discord.ext import commands
from discord import app_commands

class General(commands.Cog):
  def __init__(self,bot):
    self.bot = bot
    
  @app_commands.command(name = "ping", description = "Shows latency of bot")
  async def _ping(self,interaction:discord.Interaction):
    latency = round(self.bot.latency*1000)
    await interaction.response.send_message(f"Pong! Latency {latency}ms ")
    
async def setup(bot: commands.Bot):
  await bot.add_cog(General(bot))