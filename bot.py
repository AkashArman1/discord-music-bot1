import discord
from discord.ext import commands
import wavelink
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Connect to Lavalink node
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    # Check if NodePool is already connected
    if not wavelink.NodePool.nodes:
        await wavelink.NodePool.create_node(
            bot=bot,
            host='lava.link',      # Free public Lavalink
            port=2333,
            password='youshallnotpass',
            https=False
        )
    print('Bot ready and connected to Lavalink!')

# Join VC
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect(cls=wavelink.Player)
        await ctx.send(f"Joined {channel}")
    else:
        await ctx.send("You are not in a voice channel!")

# Leave VC
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected")
    else:
        await ctx.send("I am not in a voice channel!")

# Play music
@bot.command()
async def play(ctx, *, query: str):
    if not ctx.voice_client:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            return await ctx.send("Join a voice channel first!")

    tracks = await wavelink.YouTubeTrack.search(query=query, return_first=True)
    await ctx.voice_client.play(tracks)
    await ctx.send(f"Now playing: {tracks.title}")

# Skip
@bot.command()
async def skip(ctx):
    if ctx.voice_client.is_playing():
        await ctx.voice_client.stop()
        await ctx.send("Skipped!")
    else:
        await ctx.send("Nothing is playing!")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
