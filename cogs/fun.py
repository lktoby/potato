import os
import aiohttp
import typing
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from google.cloud import translate_v3

load_dotenv()
tenor_api_key = os.getenv('TENOR_API_KEY')
gcp_id = os.getenv('GCP_ID')

def translate_jpen(text: str = ''):
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{gcp_id}/locations/global"
    response = client.translate_text(
        contents=[text],
        target_language_code="en",
        parent=parent,
        mime_type="text/plain",
        source_language_code="ja",
    )
    translated_text = response.translations[0].translated_text
    return translated_text

class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        print(f"Cog {self.__cog_name__} loaded!")

    @commands.hybrid_command(
        name="image",
        description="generates a random molcar image",
        with_app_command=True,
    )
    @app_commands.choices(
        character=[
            app_commands.Choice(name="potato", value="potato pui pui molcar"),
            app_commands.Choice(name="shiromo", value="shiromo pui pui molcar"),
            app_commands.Choice(name="choco", value="choco pui pui molcar"),
            app_commands.Choice(name="abbey", value="abbey pui pui molcar"),
            app_commands.Choice(name="teddy", value="teddy pui pui molcar"),
        ]
    )
    async def image(self, ctx: commands.Context, character: typing.Optional[str]):
        if character is None:
            q = "pui pui molcar"
        else:
            q = character
        client_key = "potato"
        random = "true"
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://tenor.googleapis.com/v2/search?q={q}&key={tenor_api_key}&client_key={client_key}&random={random}') as resp:
                data = await resp.json()
                url = data['results'][0]['itemurl']
                await ctx.send(url)

    @commands.hybrid_command(name='translate', description='translate something japanese to english', with_app_command=True)
    async def translate(self, ctx: commands.Context, *, content: str):
        await ctx.send(translate_jpen(content))

async def setup(bot):
    await bot.add_cog(Fun(bot))
