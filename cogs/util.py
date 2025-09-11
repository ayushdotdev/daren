import discord
from discord.ext import commands
from discord import app_commands

class Utility(commands.Cog):
  def __init__(self,bot):
    self.bot = bot
    
  @app_commands.command(name = "avatar", description = "View avatar of a user")
  async def _avatar(self, interaction: discord.Interaction, member: discord.Member):
    avatar = discord.Embed(
      color = 0x4b00ff,
      title = member.name,
      description = f"**User Avatar**"
      )
    avatar.set_image(url = member.avatar.url)
    await interaction.response.send_message(embed = avatar)
      
async def setup(bot: commands.Bot):
  await bot.add_cog(Utility(bot))