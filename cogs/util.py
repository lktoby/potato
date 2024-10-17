import typing
import datetime
import discord
from discord.ext import commands
from discord import app_commands

class Util(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        print("Cog util loaded!")
    
    @commands.hybrid_command(name='ping', description='returns bot ping' , with_app_command=True)
    async def ping(self, ctx: commands.Context):
        ping = round(self.bot.latency, 2) * 1000
        await ctx.send(f'ping: {ping} ms')

    @commands.hybrid_command(name='perms', description='check user permissions in the server', with_app_command=True)
    async def perms(self, ctx:commands.Context, user: typing.Optional[discord.Member]):
        if user is None:
            user = ctx.author
        perm_list = [perm[0] for perm in user.guild_permissions if perm[1]]
        roles_list = [role.mention for role in user.roles]
        embed = discord.Embed(title=user.name, color=0xfcb900, timestamp=datetime.datetime.now())
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(name='permissions', value='\n'.join(perm_list))
        embed.add_field(name='roles', value='\n'.join(roles_list))
        embed.add_field(name='account created at', value=user.created_at.strftime('%D'), inline=True)
        embed.add_field(name='joined at', value=user.joined_at.strftime('%d %b %Y'), inline=True)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Util(bot))