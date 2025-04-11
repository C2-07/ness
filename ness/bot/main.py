import discord
from discord.ext import commands
from discord import app_commands
import os
import logging
import aiohttp
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='?', intents=intents)

FASTAPI_BASE_URL = "http://localhost:8000/api"  # Change if needed

# Utility to fetch dropdown options from FastAPI
async def fetch_options_from_api(endpoint: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{FASTAPI_BASE_URL}/{endpoint}") as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    logger.warning(f"Failed to fetch {endpoint} options: {resp.status}")
        except Exception as e:
            logger.error(f"Error fetching {endpoint}: {e}")
    return []

# Modal for Ask command
class AskModal(discord.ui.Modal, title="Ask Something"):
    def __init__(self, prompt_types):
        super().__init__()
        self.add_item(discord.ui.TextInput(label="Your Question", custom_id="user_message", style=discord.TextStyle.paragraph))

        if prompt_types:
            self.prompt_type_input = discord.ui.Select(
                placeholder="Select a prompt type (optional)",
                options=[discord.SelectOption(label=pt) for pt in prompt_types],
                custom_id="prompt_type",
                min_values=0,
                max_values=1
            )
            self.add_item(self.prompt_type_input)

    async def on_submit(self, interaction: discord.Interaction):
        user_message = self.children[0].value
        prompt_type = self.prompt_type_input.values[0] if hasattr(self, 'prompt_type_input') and self.prompt_type_input.values else None

        await interaction.response.send_message(
            f"Sent your message: `{user_message}` with prompt_type: `{prompt_type}`", ephemeral=True
        )
        # Here you send data to FastAPI

# Modal for Do command
class DoModal(discord.ui.Modal, title="Do Something"):
    def __init__(self, do_types):
        super().__init__()
        self.add_item(discord.ui.TextInput(label="What to do", custom_id="task", style=discord.TextStyle.paragraph))

        if do_types:
            self.do_type_input = discord.ui.Select(
                placeholder="Select a task type (optional)",
                options=[discord.SelectOption(label=dt) for dt in do_types],
                custom_id="do_type",
                min_values=0,
                max_values=1
            )
            self.add_item(self.do_type_input)

    async def on_submit(self, interaction: discord.Interaction):
        task = self.children[0].value
        do_type = self.do_type_input.values[0] if hasattr(self, 'do_type_input') and self.do_type_input.values else None

        await interaction.response.send_message(
            f"Executing task: `{task}` with do_type: `{do_type}`", ephemeral=True
        )
        # Here you send data to FastAPI


@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user.name} ({bot.user.id})')
    try:
        synced = await bot.tree.sync()
        logger.info(f'Synced {len(synced)} commands')
    except Exception as e:
        logger.error(f'Error syncing commands: {e}')


@bot.tree.command(name='ask', description='Ask anything using Gemini AI')
async def ask(interaction: discord.Interaction):
    prompt_types = await fetch_options_from_api("prompts")
    await interaction.response.send_modal(AskModal(prompt_types))


@bot.tree.command(name='do', description='Execute a predefined action')
async def do(interaction: discord.Interaction):
    do_types = await fetch_options_from_api("do-types")
    await interaction.response.send_modal(DoModal(do_types))


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logger.error("DISCORD_TOKEN not found in environment variables.")
    else:
        bot.run(token)
