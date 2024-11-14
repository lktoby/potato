import calendar
import typing
import datetime
import discord
from discord.ext import commands
from discord import app_commands

class Util(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        print(f"Cog {self.__cog_name__} loaded!")
    
    @commands.hybrid_command(name='ping', description='returns bot ping', with_app_command=True)
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

    @commands.hybrid_command(name='timestamp', description='convert local time to discord timestamp', with_app_command=True)
    @app_commands.choices(format= [
        app_commands.Choice(name='short date time', value='f'),
        app_commands.Choice(name='long date time', value='F'),
        app_commands.Choice(name='short date', value='d'),
        app_commands.Choice(name='long date', value='D'),
        app_commands.Choice(name='short time', value='t'),
        app_commands.Choice(name='long time', value='T'),
        app_commands.Choice(name='relative', value='R')
    ])
    async def timestamp(self, ctx: commands.Context, format:str='f',*, time: typing.Optional[str]):
        if time is None:
            time = datetime.datetime.utcnow().utctimetuple()
            unix = calendar.timegm(time)
        else :
            t = datetime.datetime.strptime(time, '%Y/%m/%d %H:%M')
            unix = round(datetime.datetime.timestamp(t))
        ts = f'<t:{unix}:{format}>'
        await ctx.send(f'converted timestamp: {ts}')

    @timestamp.error
    async def timestamp_error(self, ctx: commands.Context, error):
        embed = discord.Embed(title='pui? an error occured', description=error, color=0xfcb900)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='timeguide', description='shows how to use timestamp command', with_app_command=True)
    async def timeguide(self, ctx: commands.Context):
        embed = discord.Embed(title='timestamp help', color=0xfcb900, timestamp=datetime.datetime.now(), description='format:\n \
                              <t:1729142820:f> - short date time\n \
                              <t:1729142820:F> - long date time\n \
                              <t:1729142820:d> - short date\n \
                              <t:1729142820:D> - long date\n \
                              <t:1729142820:t> - short time\n \
                              <t:1729142820:T> - long time\n \
                              <t:1729142820:R> - relative\n \
                              leave blank for short date time\n\n \
                              time\ninput according to the following format: yyyy/mm/dd hh:mm\n \
                              e.g. 2024/10/17 14:17\n \
                              leave blank for current time (follows local time on your device)')
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Util(bot))