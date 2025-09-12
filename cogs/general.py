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
    
  @app_commands.command(name="help", description="Shows list of all commands present.")
  async def _help(self, interaction: discord.Interaction):
    pages = []
    for cog_name, cog in self.bot.cogs.items():
        lines = [f"**/{cmd.name}** - {cmd.description or 'No description provided'}"
                 for cmd in cog.get_app_commands()]
        embed = discord.Embed(
            color=0x4b00ff,
            title=f"{cog_name} Commands",
            description="\n".join(lines) or "No commands"
        )
        pages.append(embed)

    if not pages:
        await interaction.response.send_message("No commands available.", ephemeral=True)
        return

    index = 0
    def make_embed(i):
        e = pages[i].copy()
        e.set_footer(text=f"Page {i+1}/{len(pages)}")
        return e

    view = discord.ui.View()

    if len(pages) > 1:
        async def prev_btn_callback(interaction: discord.Interaction):
            nonlocal index
            index = (index - 1) % len(pages)
            await interaction.response.edit_message(embed=make_embed(index), view=view)

        async def nxt_btn_callback(interaction: discord.Interaction):
            nonlocal index
            index = (index + 1) % len(pages)
            await interaction.response.edit_message(embed=make_embed(index), view=view)

        prev_btn = discord.ui.Button(label="◀", style=discord.ButtonStyle.primary)
        prev_btn.callback = prev_btn_callback
        view.add_item(prev_btn)

        nxt_btn = discord.ui.Button(label="▶", style=discord.ButtonStyle.primary)
        nxt_btn.callback = nxt_btn_callback
        view.add_item(nxt_btn)

        await interaction.response.send_message(embed=make_embed(index), view=view)
    else:
        await interaction.response.send_message(embed=make_embed(index))
      
async def setup(bot: commands.Bot):
  await bot.add_cog(General(bot))