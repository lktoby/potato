import re
import discord
from discord.ext import commands

class Verify(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        print(f"Cog {self.__cog_name__} loaded!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if 'waiting-room' not in message.channel.name:
            return
        trusted_mol = message.guild.get_role(1230352726999957534)
        if re.search(r'^[pP][uU][iI]$', message.content):
            await message.author.add_roles(trusted_mol)
            await message.channel.send(f'{message.author.name} is now a trusted mol!')


async def setup(bot):
    await bot.add_cog(Verify(bot))