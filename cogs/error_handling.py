import discord
from discord.ext import commands
import sys
import traceback

class ExceptionHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        print(f"Cog {self.__cog_name__} loaded!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        await ctx.reply(f'an error occured!\n{error}',
                        mention_author=False)
        print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        
async def setup(bot: commands.Bot):
    await bot.add_cog(ExceptionHandler(bot))