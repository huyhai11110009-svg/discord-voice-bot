import discord
from discord.ext import commands
from keep_alive import keep_alive

keep_alive()  # Giữ cho web Render sống

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot {bot.user} đã sẵn sàng!")

@bot.command()
async def becam(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("Đã vào room thành công 🎧")
    else:
        await ctx.send("Bạn cần vào voice room trước!")

@bot.command()
async def cut(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Bot đã rời khỏi room ❌")
    else:
        await ctx.send("Bot không ở trong room.")

bot.run("TOKEN_DISCORD_CỦA_BẠN")
