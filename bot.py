import asyncio
import discord
from discord.ext import commands

# Masukkan token bot Discord kamu di sini
TOKEN = "MTU0NjQ2NDk0NTEyNDgxMDg0Mw.GeQS27.X-i_AmATf3qSTMVq-P_yea5OfBMs02-lOw3k0E"

# ID Voice Channel
VOICE_CHANNEL_ID = 1454101701404397652

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
from flask import Flask

app = Flask(__name__)

@app.get("/")
def read_root():
    return {"Python": "on Vercel"}

async def keep_voice_connected():
    await bot.wait_until_ready()

    while not bot.is_closed():
        try:
            channel = bot.get_channel(VOICE_CHANNEL_ID)

            if channel is None:
                print("❌ Voice Channel tidak ditemukan.")
                await asyncio.sleep(30)
                continue

            voice = discord.utils.get(
                bot.voice_clients,
                guild=channel.guild
            )

            if voice is None:
                print(f"🔊 Connecting to: {channel.name}")
                await channel.connect(self_deaf=True)

            elif not voice.is_connected():
                print("⚠️ Voice disconnected. Reconnecting...")
                await voice.disconnect(force=True)
                await channel.connect(self_deaf=True)

            elif voice.channel.id != channel.id:
                print("🔄 Memindahkan bot ke Voice Channel...")
                await voice.move_to(channel)

            await asyncio.sleep(30)

        except Exception as e:
            print(f"❌ Voice error: {e}")
            await asyncio.sleep(30)


@bot.event
async def on_ready():
    print("================================")
    print(f"✅ Bot online: {bot.user}")
    print(f"🎤 Voice Channel ID: {VOICE_CHANNEL_ID}")
    print("================================")


@bot.event
async def setup_hook():
    asyncio.create_task(keep_voice_connected())


bot.run(TOKEN)
