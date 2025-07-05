import discord
from discord.ext import commands
import os
import json
import logging
from filter import is_message_clean, add_banned_word, remove_banned_word, list_banned_words
from keep_alive import keep_alive

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Permission levels:
# 1. Regular users - Can use confession commands
# 2. Manage Messages - Can manage word filters  
# 3. Administrator - Can set up channels

# Discord bot intents
intents = discord.Intents.default()
intents.message_content = True
# Remove members intent as it's not needed for confession bot
# intents.members = True

# Initialize bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Load saved channel configs
if os.path.exists("channels.json"):
    with open("channels.json", "r") as f:
        confession_channels = json.load(f)
else:
    confession_channels = {}

def save_channels():
    with open("channels.json", "w") as f:
        json.dump(confession_channels, f)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # ✅ If it's a DM
    if isinstance(message.channel, discord.DMChannel):
        # Only respond to valid commands (starting with !)
        if message.content.startswith("!"):
            await bot.process_commands(message)
        else:
            # Ignore non-command DMs
            await message.channel.send("ℹ️ Please use a valid command (e.g. `!confess`).")
    else:
        # ✅ In servers, process commands as usual
        await bot.process_commands(message)

# 🛠️ Admin Setup Command
@bot.command()
@commands.has_permissions(administrator=True)
async def setchannel(ctx, category: str, channel: discord.TextChannel):
    """Administrator command to set confession channels"""
    guild_id = str(ctx.guild.id)
    if guild_id not in confession_channels:
        confession_channels[guild_id] = {}
    confession_channels[guild_id][category] = channel.id
    save_channels()
    await ctx.send(f"✅ Set `{category}` confessions to {channel.mention}")

@bot.command()
@commands.has_permissions(administrator=True)
async def viewchannels(ctx):
    """Administrator command to view configured channels"""
    guild_id = str(ctx.guild.id)
    if guild_id in confession_channels:
        channels = confession_channels[guild_id]
        msg = "\n".join([f"**{k}** → <#{v}>" for k, v in channels.items()])
        await ctx.send(f"📋 Configured channels:\n{msg}")
    else:
        await ctx.send("❌ No channels configured for this server.")



# 🔍 Helper to get channel
def get_channel(guild, category):
    guild_id = str(guild.id)
    if guild_id in confession_channels and category in confession_channels[guild_id]:
        return bot.get_channel(confession_channels[guild_id][category])
    return None

# 📝 General Confession
@bot.command()
async def confess(ctx, *, message):
    # Only delete message if not in DM
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.message.delete()
    
    # Get guild (either from context or first guild if DM)
    guild = ctx.guild if ctx.guild else discord.utils.get(bot.guilds)
    if not guild:
        await ctx.author.send("❌ Bot is not connected to any servers.")
        return
    
    # Content filtering
    if not is_message_clean(message, guild.id):
        await ctx.author.send("🚫 Your message contains inappropriate content and was not sent.")
        return
    
    channel = get_channel(guild, "general")
    if not channel:
        await ctx.author.send("❌ Confession channel not set. Ask an admin to use `!setchannel general #channel`.")
        return
    embed = discord.Embed(title="📢 Anonymous Confession", description=message, color=discord.Color.purple())
    msg = await channel.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    await ctx.author.send("✅ Your confession has been sent anonymously!")

    log = get_channel(guild, "log")
    if log:
        await log.send(f"🕵️ Confession by {ctx.author}:\n{message}")

# 💘 Crush Confession
@bot.command()
async def confesscrush(ctx, *, message):
    # Only delete message if not in DM
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.message.delete()
    
    # Get guild (either from context or first guild if DM)
    guild = ctx.guild if ctx.guild else discord.utils.get(bot.guilds)
    if not guild:
        await ctx.author.send("❌ Bot is not connected to any servers.")
        return
    
    # Content filtering
    if not is_message_clean(message, guild.id):
        await ctx.author.send("🚫 Your message contains inappropriate content and was not sent.")
        return
    
    channel = get_channel(guild, "crush")
    if not channel:
        await ctx.author.send("❌ Crush channel not set. Ask an admin to use `!setchannel crush #channel`.")
        return
    embed = discord.Embed(title="💘 Secret Crush", description=message, color=discord.Color.red())
    msg = await channel.send(embed=embed)
    await msg.add_reaction("❤️")
    await msg.add_reaction("💔")
    await ctx.author.send("💌 Your crush confession has been sent anonymously!")

    log = get_channel(guild, "log")
    if log:
        await log.send(f"💘 Crush confession by {ctx.author}:\n{message}")

# 🎭 Truth or Dare
@bot.command()
async def truthordare(ctx, *, message):
    # Only delete message if not in DM
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.message.delete()
    
    # Get guild (either from context or first guild if DM)
    guild = ctx.guild if ctx.guild else discord.utils.get(bot.guilds)
    if not guild:
        await ctx.author.send("❌ Bot is not connected to any servers.")
        return
    
    # Content filtering
    if not is_message_clean(message, guild.id):
        await ctx.author.send("🚫 Your message contains inappropriate content and was not sent.")
        return
    
    channel = get_channel(guild, "truthordare")
    if not channel:
        await ctx.author.send("❌ Truth or Dare channel not set. Ask an admin to use `!setchannel truthordare #channel`.")
        return
    embed = discord.Embed(title="🎭 Truth or Dare", description=message, color=discord.Color.orange())
    msg = await channel.send(embed=embed)
    await msg.add_reaction("🎯")
    await msg.add_reaction("😳")
    await ctx.author.send("🎲 Your Truth or Dare has been sent anonymously!")

    log = get_channel(guild, "log")
    if log:
        await log.send(f"🎭 Truth or Dare by {ctx.author}:\n{message}")

# ❓ Ask Me Anything
@bot.command()
async def askmeanything(ctx, *, message):
    # Only delete message if not in DM
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.message.delete()
    
    # Get guild (either from context or first guild if DM)
    guild = ctx.guild if ctx.guild else discord.utils.get(bot.guilds)
    if not guild:
        await ctx.author.send("❌ Bot is not connected to any servers.")
        return
    
    # Content filtering
    if not is_message_clean(message, guild.id):
        await ctx.author.send("🚫 Your message contains inappropriate content and was not sent.")
        return
    
    channel = get_channel(guild, "ama")
    if not channel:
        await ctx.author.send("❌ AMA channel not set. Ask an admin to use `!setchannel ama #channel`.")
        return
    embed = discord.Embed(title="❓ Ask Me Anything", description=message, color=discord.Color.blue())
    msg = await channel.send(embed=embed)
    await msg.add_reaction("🤔")
    await ctx.author.send("📬 Your AMA has been sent anonymously!")

    log = get_channel(guild, "log")
    if log:
        await log.send(f"❓ AMA by {ctx.author}:\n{message}")

# 🛡️ Filter Management Commands
@bot.command()
@commands.has_permissions(manage_messages=True)
async def addfilter(ctx, *, word):
    """Manage Messages permission required"""
    if add_banned_word(ctx.guild.id, word):
        await ctx.send(f"✅ Added `{word}` to the filter list.")
    else:
        await ctx.send(f"⚠️ `{word}` is already in the filter list.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def removefilter(ctx, *, word):
    """Manage Messages permission required"""
    if remove_banned_word(ctx.guild.id, word):
        await ctx.send(f"🗑️ Removed `{word}` from the filter list.")
    else:
        await ctx.send(f"⚠️ `{word}` was not in the filter list.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def listfilters(ctx):
    """Manage Messages permission required"""
    words = list_banned_words(ctx.guild.id)
    if words:
        await ctx.send(f"📜 Filtered words: {', '.join(words)}")
    else:
        await ctx.send("✅ No custom filtered words set for this server.")

keep_alive()
bot.run(os.getenv("TOKEN"))
