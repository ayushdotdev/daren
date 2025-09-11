from discord import app_commands
from discord.ext import commands
import discord

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Kick a member")
    @app_commands.checks.has_permissions(kick_members=True)
    async def _kick(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = "No reason provided"):
        if member.id == interaction.client.user.id or member.id == interaction.user.id:
            error = discord.Embed(
                color=0xed2939,
                description="<:darenError:1415768665642766407> **_I cannot kick this user._**"
            )
            await interaction.response.send_message(embed=error, ephemeral=True)
            return

        if member.top_role >= interaction.guild.me.top_role:
            error = discord.Embed(
                color=0xed2939,
                description="<:darenError:1415768665642766407> **_My role isn't high enough to moderate this user. Move my role up above others._**"
            )
            await interaction.response.send_message(embed=error, ephemeral=True)
            return

        if not interaction.guild.me.guild_permissions.kick_members:
            error = discord.Embed(
                color=0xed2939,
                description="<:darenError:1415768665642766407> **_I don’t have permission to kick members._**"
            )
            await interaction.response.send_message(embed=error, ephemeral=True)
            return

        try:
            await member.send(
                embed=discord.Embed(
                    title=f"Kicked from {interaction.guild.name}",
                    description=f"You have been **kicked** from **{interaction.guild.name}**\n\n**Reason:**\n{reason}",
                    color=0xe24c00
                )
            )
        except discord.Forbidden:
          await interaction.response.send_message(embed=discord.Embed(
            color=0xed2939,
            description="❌ Cannot DM this user (they may have DMs disabled)."
            ),ephemeral=True)


        await member.kick(reason=reason)

        success = discord.Embed(
            color=0x48a860,
            description=f"<:darenSuccess:1415789425652269096> **{member.name} was kicked**"
        )
        await interaction.response.send_message(embed=success)
    
    @app_commands.command(name="ban", description="Ban a member")
    @app_commands.checks.has_permissions(ban_members=True)
    async def _kick(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = "No reason provided"):
        if member.id == interaction.client.user.id or member.id == interaction.user.id:
            error = discord.Embed(
                color=0xed2939,
                description="<:darenError:1415768665642766407> **_I cannot ban this user._**"
            )
            await interaction.response.send_message(embed=error, ephemeral=True)
            return

        if member.top_role >= interaction.guild.me.top_role:
            error = discord.Embed(
                color=0xed2939,
                description="<:darenError:1415768665642766407> **_My role isn't high enough to moderate this user. Move my role up above others._**"
            )
            await interaction.response.send_message(embed=error, ephemeral=True)
            return

        if not interaction.guild.me.guild_permissions.kick_members:
            error = discord.Embed(
                color=0xed2939,
                description="<:darenError:1415768665642766407> **_I don’t have permission to ban members._**"
            )
            await interaction.response.send_message(embed=error, ephemeral=True)
            return

        try:
            await member.send(
                embed=discord.Embed(
                    title=f"Banned from {interaction.guild.name}",
                    description=f"You have been **banned** from **{interaction.guild.name}**\n\n**Reason:**\n{reason}",
                    color=0xff2400
                )
            )
        except discord.Forbidden:
          await interaction.response.send_message(embed=discord.Embed(
            color=0xed2939,
            description="<:darenError:1415768665642766407> Cannot DM this user (they may have DMs disabled)."
            ),ephemeral=True)


        await member.ban(reason=reason)

        success = discord.Embed(
            color=0x48a860,
            description=f"<:darenSuccess:1415789425652269096> **{member.name} was banned**"
        )
        await interaction.response.send_message(embed=success)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))