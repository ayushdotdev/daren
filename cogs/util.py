import discord
from discord.ext import commands
from discord import app_commands

class Utility(commands.Cog):
  def __init__(self,bot):
    self.bot = bot
    
  avatar = app_commands.Group(name="avatar", description="Displays avatar of someone")

  @avatar.command(name="get", description="Get a user's avatar (guild if set, else global)")
  async def avatar_cmd(self, interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    embed = discord.Embed(
      color=0x4b00ff,
      description="**User's Avatar**"
      )
    embed.set_author(name=member.name, icon_url=member.display_avatar.url)
    embed.set_image(url=member.display_avatar.url)
    await interaction.response.send_message(embed=embed)

  @avatar.command(name="global", description="Get a user's global avatar")
  async def avatar_global(self, interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    embed = discord.Embed(color=0x4b00ff, description="**User's Global Avatar**")
    embed.set_author(name=member.name, icon_url=member.avatar.url)
    embed.set_image(url=member.avatar.url)
    await interaction.response.send_message(embed=embed)

  @avatar.command(name="guild", description="Get a user's guild avatar if they have one")
  async def avatar_guild(self, interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    if member.display_avatar != member.avatar:
      embed = discord.Embed(color=0x4b00ff, description="**User's Guild Avatar**")
      embed.set_author(name=member.name, icon_url=member.display_avatar.url)
      embed.set_image(url=member.display_avatar.url)
      await interaction.response.send_message(embed=embed)
    else:
      error_embed = discord.Embed(color=0xed2939, description=f"<:darenError:1415768665642766407> **_User does not have a server avatar._**")
      await interaction.response.send_message(embed=error_embed, ephemeral=True)
async def setup(bot: commands.Bot):
  await bot.add_cog(Utility(bot))