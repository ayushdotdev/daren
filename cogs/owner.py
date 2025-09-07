import nextcord
from nextcord.ext import commands
from nextcord import Interaction

class Owner(commands.Cog):
  def __init__(self,bot):
    self.bot = bot
  
  @commands.command(name = "reload", help = "reloads a set of commands")
  @commands.is_owner()
  async def reload(self,ctx,*,cog: str):
    try:
      self.bot.reload_extension(f'cogs.{cog}')
      await ctx.send(f'Reloaded Extension {cog} <:success:1411668840181534851>')
    except Exception as e:
      await ctx.send(f'Error Reloading Extension {cog}: {e}')
      
  @nextcord.slash_command(name = "reload", description = "reloads a set of commands")
  async def reload_slash(self, interaction: Interaction, cog:str):
    if interaction.user.id == self.bot.owner_id:
      try:
        self.bot.reload_extension(f'cogs.{cog}')
        await interaction.response.send_message(f'Reloaded Extension {cog} <:success:1411668840181534851>')
      except Exception as e:
        await interaction.response.send_message(f'Error Reloading Extension {cog}: {e}')
    
      
def setup(bot):
  bot.add_cog(Owner(bot))