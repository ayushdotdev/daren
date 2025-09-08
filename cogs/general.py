import discord
from discord.ext import commands

class General(commands.Cog):
  def __init__(self,bot):
    self.bot = bot
    
  @discord.slash_command(name = "ping" , description = "Check ping of the bot")
  async def ping(self,ctx: discord.ApplicationContext):
    latency = round(self.bot.latency *1000)
    await ctx.respond(f'Pong! Latency {latency}ms')
    
def setup(bot):
  bot.add_cog(General(bot))