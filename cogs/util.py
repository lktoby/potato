import os
import sys
import json
import typing
import aiohttp
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

load_dotenv()
tenor_api_key = os.getenv('TENOR_API_KEY')
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
    async def perms(self, ctx:commands.Context):
        perm_list = [perm[0] for perm in ctx.author.guild_permissions if perm[1]]
        await ctx.send(f'{ctx.author.name}\n{perm_list}')

    @commands.hybrid_command(name='restart', description='restarts the bot', with_app_command=True)
    @commands.is_owner()
    async def restart(self, ctx: commands.Context):
        await ctx.send('restarting...')
        print(f'{ctx.author} ({ctx.author.id}) is restarting the bot...')
        os.execv(sys.executable, ['python'] + sys.argv)

    @app_commands.command(name='embed', description='outputs an embed from json')
    @commands.has_permissions(administrator=True)
    async def embed(self, interaction: discord.Interaction, channel: typing.Union[discord.TextChannel, discord.Thread], *, input: str):
        e = json.loads(input)
        embed = discord.Embed.from_dict(e)
        await channel.send(embed=embed)
        await interaction.response.send_message(f'embed sent to {channel.mention}!', ephemeral=True)

    @app_commands.command(name='echo', description='make the bot say something')
    @commands.has_permissions(administrator=True)
    async def echo(self, interaction: discord.Interaction, channel: typing.Union[discord.TextChannel, discord.Thread], *, input: str):
        await channel.send(input)
        await interaction.response.send_message(f'message sent to {channel.mention}!', ephemeral=True)

    @commands.command(name='sync')
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        await ctx.send('syncing commands...')
        sync = await ctx.bot.tree.sync()
        await ctx.send(f'all {len(sync)} commands synced!')

    @commands.hybrid_command(name='game', description='set what potato is playing', with_app_command=True)
    @commands.has_permissions(administrator=True)
    @app_commands.choices(type=[
        app_commands.Choice(name='Playing', value='Playing'),
        app_commands.Choice(name='Streaming', value='Streaming'),
        app_commands.Choice(name='Listening', value='Listening'),
        app_commands.Choice(name='Watching', value='Watching')
    ])
    async def game(self, ctx: commands.Context, type: str, *, activity: str):
        if type == 'Playing':
            await self.bot.change_presence(activity=discord.Game(name=activity))
        elif type == 'Streaming':
            await self.bot.change_presence(activity=discord.Streaming(name=activity))
        elif type == 'Listening':
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity))
        elif type == 'Watching':
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity))
        await ctx.send(f'activity set to {type} {activity}')

    @commands.hybrid_command(name='image', description='generates a random molcar image', with_app_command=True)
    async def image(self, ctx: commands.Context):
        q = "pui pui molcar"
        client_key = "potato"
        random = "true"
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://tenor.googleapis.com/v2/search?q={q}&key={tenor_api_key}&client_key={client_key}&random={random}') as resp:
                data = await resp.json()
                url = data['results'][0]['itemurl']
                await ctx.send(url)

async def setup(bot):
    await bot.add_cog(Util(bot))