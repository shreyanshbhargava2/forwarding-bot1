import discord
from discord.ext import commands
import aiohttp
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_CHANNEL_ID = 1489655258836762636
DESTINATION_WEBHOOK = os.getenv("DESTINATION_WEBHOOK")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.event
async def on_message(message):
    if message.channel.id != SOURCE_CHANNEL_ID:
        return
    if message.author.bot:
        return

    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(DESTINATION_WEBHOOK, session=session)
        await webhook.send(
            content=message.content,
            username=message.author.display_name,
            avatar_url=message.author.display_avatar.url
        )

@bot.event
async def on_message_edit(before, after):
    if after.channel.id != SOURCE_CHANNEL_ID:
        return
    if after.author.bot:
        return

    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(DESTINATION_WEBHOOK, session=session)
        await webhook.send(
            content=f"**[Edited]** {after.content}",
            username=after.author.display_name,
            avatar_url=after.author.display_avatar.url
        )

bot.run(BOT_TOKEN)
