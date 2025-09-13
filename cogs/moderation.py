from discord import app_commands
from discord.ext import commands
import discord

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Kick a member")
    @app_commands.checks.has_permissions(kick_members=True)
    async def _kick(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = "No reason provided"):
        if member.id in [interaction.client.user.id, interaction.user.id, interaction.guild.owner_id]:
            error = discord.Embed(
                color=0xed2939,
                description="<:darenError:1415768665642766407> **_I cannot kick this user._**"
            )
            await interaction.response.send_message(embed=error, ephemeral=True)
            return
          
        if member.bot:
          error = discord.Embed(
            color=0xed2939,
            description="<:darenError:1415768665642766407> **_I cannot kick other bots._**"
          )
          await interaction.response.send_message(embed=error, ephemeral=True)
          return
    
        if member.top_role.position >= interaction.guild.me.top_role.position:
            error = discord.Embed(
                color=0xed2939,
                description="<:darenError:1415768665642766407> **_My role isn't high enough to moderate this user. Move my role up above others._**"
            )
            await interaction.response.send_message(embed=error, ephemeral=True)
            return
    
        if member.top_role.position >= interaction.user.top_role.position and interaction.guild.owner_id != interaction.user.id:
            error = discord.Embed(
                color=0xed2939,
                description="<:darenError:1415768665642766407> **_You cannot kick this user._**"
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
            pass
    
        await member.kick(reason=reason)
    
        success = discord.Embed(
            color=0x48a860,
            description=f"<:darenSuccess:1415789425652269096> **{member.name} was kicked**"
        )
        await interaction.response.send_message(embed=success)
        
    @app_commands.command(name="ban", description="Ban a member")
    @app_commands.checks.has_permissions(ban_members=True)
    async def _ban(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = "No reason provided"):
        if member.id in [interaction.client.user.id, interaction.user.id, interaction.guild.owner_id]:
            error = discord.Embed(
                color=0xed2939,
                description="<:darenError:1415768665642766407> **_I cannot ban this user._**"
            )
            await interaction.response.send_message(embed=error, ephemeral=True)
            return
    
        if member.top_role.position >= interaction.guild.me.top_role.position:
            error = discord.Embed(
                color=0xed2939,
                description="<:darenError:1415768665642766407> **_My role isn't high enough to moderate this user. Move my role up above others._**"
            )
        
        if member.bot:
          error = discord.Embed(
            color=0xed2939,
            description="<:darenError:1415768665642766407> **_I cannot ban other bots._**"
          )
          await interaction.response.send_message(embed=error, ephemeral=True)
          return
    
        if member.top_role.position >= interaction.user.top_role.position and interaction.guild.owner_id != interaction.user.id:
            error = discord.Embed(
                color=0xed2939,
                description="<:darenError:1415768665642766407> **_You cannot ban this user._**"
            )
            await interaction.response.send_message(embed=error, ephemeral=True)
            return
    
        if not interaction.guild.me.guild_permissions.ban_members:
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
            pass
    
        await member.ban(reason=reason)
    
        success = discord.Embed(
            color=0x48a860,
            description=f"<:darenSuccess:1415789425652269096> **{member.name} was banned**"
        )
        await interaction.response.send_message(embed=success)
    
    
    @app_commands.command(name="unban", description="Unban a user")
    @app_commands.checks.has_permissions(ban_members=True)
    async def _unban(self, interaction: discord.Interaction, user_id: str, *, reason: str = "No reason provided"):
        try:
            user_id = int(user_id)
        except ValueError:
            await interaction.response.send_message(
                embed=discord.Embed(
                    color=0xed2939,
                    description="<:darenError:1415768665642766407> **_Invalid user ID._**"
                ),
                ephemeral=True
            )
            return
    
        try:
            user = await interaction.client.fetch_user(user_id)
            await interaction.guild.unban(user, reason=reason)
    
            success = discord.Embed(
                color=0x48a860,
                description=f"<:darenSuccess:1415789425652269096> **{user} was unbanned**"
            )
            await interaction.response.send_message(embed=success)
    
            try:
                await user.send(
                    embed=discord.Embed(
                        title=f"Unbanned from {interaction.guild.name}",
                        description=f"You have been **unbanned** from **{interaction.guild.name}**\n\n**Reason:**\n{reason}",
                        color=0x48a860
                    )
                )
            except discord.Forbidden:
                pass
    
        except discord.NotFound:
            error = discord.Embed(
                color=0xed2939,
                description="<:darenError:1415768665642766407> **_This user is not banned._**"
            )
            await interaction.response.send_message(embed=error, ephemeral=True)
            
    @app_commands.command(name="softban", description="Softban a member. (ban and then immediate unban to delete their messages")
    @app_commands.checks.has_permissions(ban_members=True)
    async def _softban(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = "No reason provided"):
        if member.id in [interaction.client.user.id, interaction.user.id, interaction.guild.owner_id]:
            error = discord.Embed(
                color=0xed2939,
                description="<:darenError:1415768665642766407> **_I cannot kick this user._**"
            )
            await interaction.response.send_message(embed=error, ephemeral=True)
            return
    
        if member.top_role.position >= interaction.guild.me.top_role.position:
            error = discord.Embed(
                color=0xed2939,
                description="<:darenError:1415768665642766407> **_My role isn't high enough to moderate this user. Move my role up above others._**"
            )
        
        if member.bot:
          error = discord.Embed(
            color=0xed2939,
            description="<:darenError:1415768665642766407> **_I cannot kick other bots._**"
          )
          await interaction.response.send_message(embed=error, ephemeral=True)
          return
    
        if member.top_role.position >= interaction.user.top_role.position and interaction.guild.owner_id != interaction.user.id:
            error = discord.Embed(
                color=0xed2939,
                description="<:darenError:1415768665642766407> **_You cannot kick this user._**"
            )
            await interaction.response.send_message(embed=error, ephemeral=True)
            return
    
        if not interaction.guild.me.guild_permissions.ban_members:
            error = discord.Embed(
                color=0xed2939,
                description="<:darenError:1415768665642766407> **_I don’t have permission to ban members._**"
            )
            await interaction.response.send_message(embed=error, ephemeral=True)
            return
    
        try:
            await member.send(
                embed=discord.Embed(
                    title=f"Kicked from {interaction.guild.name}",
                    description=f"You have been **kicked** from **{interaction.guild.name}**\n\n**Reason:**\n{reason}",
                    color=0xff2400
                )
            )
        except discord.Forbidden:
            pass
    
        await interaction.guild.ban(member, reason = reason)
        await interaction.guild.unban(member, reason = reason)
    
        success = discord.Embed(
            color=0x48a860,
            description=f"<:darenSuccess:1415789425652269096> **_{member.name} was softbanned._**"
        )
        await interaction.response.send_message(embed=success)
        
    purge = app_commands.Group(name = "purge", description = "Delete a number of messages from a channel. (limit 1000)")
    
    @purge.command(name = "any", description = "Deletes any message type")
    @app_commands.checks.has_permissions(manage_messages = True)
    async def purge_cmd(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1,1000]):
      await interaction.response.defer(ephemeral = True)
      deleted = await interaction.channel.purge(limit = amount)
      await interaction.followup.send(embed = discord.Embed(
        color=0x48a860,
        description=f"<:darenSuccess:1415789425652269096> **_Deleted {len(deleted)} messages._**"
        ), ephemeral = True)
      

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))