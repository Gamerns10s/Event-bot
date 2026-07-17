import discord
from discord.ext import commands
from discord import app_commands

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roleids", aliases=["giveroleid", "roleid"])
    async def roleids_prefix(self, ctx, *, roles_data: str):
        role_names = [r.strip().lower() for r in roles_data.split(',')]
        found_roles = []
        for r_name in role_names:
            if not r_name: continue
            r_id = None
            if r_name.startswith('<@&') and r_name.endswith('>'):
                try: r_id = int(r_name[3:-1])
                except: pass
            elif r_name.isdigit(): r_id = int(r_name)
            role = ctx.guild.get_role(r_id) if r_id else discord.utils.find(lambda r: r.name.lower() == r_name, ctx.guild.roles)
            if role and role not in found_roles: found_roles.append(role)
        if not found_roles:
            await ctx.send("❌ Could not find any roles matching your input.")
            return
        response = "\n".join([f"{role.name}: {role.id}" for role in found_roles])
        await ctx.send(f"**Role IDs:**\n```\n{response}\n```")

    @app_commands.command(name="roleids", description="Get the IDs of up to 5 roles")
    async def roleids_slash(self, interaction: discord.Interaction, role1: discord.Role, role2: discord.Role = None, role3: discord.Role = None, role4: discord.Role = None, role5: discord.Role = None):
        roles = [r for r in [role1, role2, role3, role4, role5] if r is not None]
        response = "\n".join([f"{role.name}: {role.id}" for role in roles])
        await interaction.response.send_message(f"**Role IDs:**\n```\n{response}\n```", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Roles(bot))
