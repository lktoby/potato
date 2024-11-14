import json
import os
import sys
import typing
import discord
from discord.ext import commands
from discord import app_commands

class Mod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        print(f"Cog {self.__cog_name__} loaded!")

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
    
    @commands.hybrid_command(name='restart', description='restarts the bot', with_app_command=True)
    @commands.is_owner()
    async def restart(self, ctx: commands.Context):
        await ctx.send('restarting...')
        print(f'{ctx.author} ({ctx.author.id}) is restarting the bot...')
        os.execv(sys.executable, ['python'] + sys.argv)
    
    @commands.command(name='sync', hidden=True)
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        await ctx.send('syncing commands...')
        sync = await ctx.bot.tree.sync()
        await ctx.send(f'all {len(sync)} commands synced!')

async def setup(bot):
    await bot.add_cog(Mod(bot))