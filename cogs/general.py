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
    
  @app_commands.command(name = "help", description = "Shows list of all commands present.")
  async def _help(self, interaction: discord.Interaction):
    pages = []
    for cog_name, cog in self.bot.cogs.items():
      lines = []
      for cmd in cog.get_app_commands():
        lines.append(f"**/{cmd.name}** - {cmd.description or 'No description provided'}")
      embed = discord.Embed(
        color = 0x4b00ff,
        title = f"{cog_name} Commands",
        description = "\n".join(lines)
        )
      pages.append(embed)
      
      index = 0
      async def update(interaction: discord.Interaction):
        await interaction.response.edit_message(embed = pages[index])
        
      view = discord.ui.View(timeout = 180)
      async def prev_btn_callback(interaction: discord.Interaction):
        nonlocal index
        index = (index - 1) % len(pages)
        await update(interaction)
        
      prev_btn = discord.ui.Button(
        label = "◀️",
        style = discord.ButtonStyle.primary
        )
      prev_btn.callback = prev_btn_callback
      view.add_item(prev_btn)
      
      async def nxt_btn_callback(interaction: discord.Interaction):
        nonlocal index
        index = (index + 1) % len(pages)
        await update(interaction)
        
      nxt_btn = discord.ui.Button(
        label = "▶️",
        style = discord.ButtonStyle.primary
        )
      nxt_btn.callback = nxt_btn_callback
      view.add_item(nxt_btn)
      
      await interaction.response.send_message(embed = pages[index], view = view)
      
async def setup(bot: commands.Bot):
  await bot.add_cog(General(bot))