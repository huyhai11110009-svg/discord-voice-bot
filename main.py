import discord
from discord.ext import commands
import json
import asyncio
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix="/", intents=intents)

CONFIG_FILE = "config.json"

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập: {bot.user}")
    config = load_config()
    if "voice_channel_id" in config:
        channel = bot.get_channel(config["voice_channel_id"])
        if channel:
            try:
                await channel.connect()
                print("🔁 Đã tự động vào lại voice channel sau khi restart.")
            except:
                pass

@bot.slash_command(name="becam", description="Bot tham gia voice channel hiện tại của bạn.")
async def becam(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        config = {"voice_channel_id": channel.id}
        save_config(config)
        await ctx.respond(f"🔊 Đã tham gia kênh thoại: {channel.name}")
    else:
        await ctx.respond("❌ Bạn cần vào kênh thoại trước.")

@bot.slash_command(name="cut", description="Bot rời khỏi voice channel.")
async def cut(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        save_config({})
        await ctx.respond("👋 Đã rời kênh thoại.")
    else:
        await ctx.respond("❌ Bot không ở trong kênh thoại nào.")

@bot.event
async def on_voice_state_update(member, before, after):
    vc = member.guild.voice_client
    if vc and not vc.is_connected():
        await asyncio.sleep(2)
        config = load_config()
        if "voice_channel_id" in config:
            channel = bot.get_channel(config["voice_channel_id"])
            if channel:
                await channel.connect()

keep_alive()
bot.run("MTQzMTIyOTcyMTkyODI2OTkzNA.G3CY5C.twvZVW2RJEG2AZtgofPT8GKPhhKqWflSFNGbE8")
