from datetime import datetime
import typing
import discord
from discord.ext import commands
from discord import app_commands

class MolcarHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='pui? you need help?', description='run `/help [command]` to know more about what a specific command does!\n', color=0xfcb900, timestamp=datetime.now())
        for cog, commands in mapping.items():
           filtered = await self.filter_commands(commands, sort=True)
           command_signatures = [self.get_command_signature(c) for c in filtered]
           if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command), color=0xfcb900, timestamp=datetime.now())
        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_error_message(self, error):
        embed = discord.Embed(title='pui! you ran into an error', description=error, color=0xfcb900, timestamp=datetime.now())
        channel = self.get_destination()
        await channel.send(embed)

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        help_command = MolcarHelp()
        help_command.cog = self
        bot.help_command = help_command

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

    @app_commands.command(name='help', description='learn how the bot works')
    async def help(self, interaction: discord.Interaction, command_or_group: typing.Optional[str]):
        ctx = await self.bot.get_context(interaction)
        entity = command_or_group and (command_or_group,) or ()
        await ctx.send_help(*entity)

    # slash command credit: 
    # https://gist.github.com/InterStella0/b78488fb28cadf279dfd3164b9f0cf96?permalink_comment_id=5175257#gistcomment-5175257

async def setup(bot):
    await bot.add_cog(Help(bot))