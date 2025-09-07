import nextcord
from nextcord.ext import commands
from nextcord import ButtonStyle, Interaction

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---------- Ping Logic ----------
    async def ping_logic(self, ctx_or_interaction):
        latency = round(self.bot.latency * 1000)
        message = f"Pong! Latency {latency} ms"
        
        if isinstance(ctx_or_interaction, commands.Context):
            await ctx_or_interaction.send(message)
        else:  # Interaction (slash command)
            await ctx_or_interaction.response.send_message(message)

    @commands.command(name="ping", help="Check latency of the bot")
    async def ping(self, ctx):
        await self.ping_logic(ctx)

    @nextcord.slash_command(name="ping", description="Check latency of the bot")
    async def ping_slash(self, interaction: Interaction):
        await self.ping_logic(interaction)

    # ---------- Help Logic ----------
    async def help_logic(self, ctx_or_interaction):
        view = nextcord.ui.View()
        prev_btn = nextcord.ui.Button(label="◀️", style=ButtonStyle.primary)
        next_btn = nextcord.ui.Button(label="▶️", style=ButtonStyle.primary)
        view.add_item(prev_btn)
        view.add_item(next_btn)

        pages = []
        for cog_name, cog_object in self.bot.cogs.items():
            page = nextcord.Embed(
                title=f"**{cog_name} Commands**",
                color=0x4b00ff
            )
            for cmd in cog_object.get_commands():
                page.add_field(
                    name=f"!{cmd.name}",
                    value=cmd.help or "No description provided",
                    inline=False
                )
            pages.append(page)

        current_page = 0

        async def prev_callback(interaction: Interaction):
            nonlocal current_page
            current_page = max(current_page - 1, 0)
            await interaction.response.edit_message(embed=pages[current_page], view=view)

        async def next_callback(interaction: Interaction):
            nonlocal current_page
            current_page = min(current_page + 1, len(pages) - 1)
            await interaction.response.edit_message(embed=pages[current_page], view=view)

        prev_btn.callback = prev_callback
        next_btn.callback = next_callback

        # Send message depending on context type
        if isinstance(ctx_or_interaction, commands.Context):
            await ctx_or_interaction.send(embed=pages[current_page], view=view)
        else:
            await ctx_or_interaction.response.send_message(embed=pages[current_page], view=view)

    @commands.command(name="help", help="Shows this message")
    async def help(self, ctx, *, cmd: str = None):
        await self.help_logic(ctx)

    @nextcord.slash_command(name="help", description="Shows this message")
    async def help_slash(self, interaction: Interaction):
        await self.help_logic(interaction)


def setup(bot):
    bot.add_cog(General(bot))