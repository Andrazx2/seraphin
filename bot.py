import discord
from discord.ext import commands
import os
import aiohttp
import asyncio

# ---- Configuration ----
PREFIX = "!"  # Command prefix, you can change this for example: "?", "."

# intents required so the bot can read messages/members
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Raw file URL to fetch
UNIVERSAL_SCRIPT_RAW_URL = "https://raw.githubusercontent.com/nniellx/SeraphinHub/refs/heads/main/SeraphinMain.lua"


# ---- Event when bot is active ----
@bot.event
async def on_ready():
    print(f"✅ Bot {bot.user} is now online!")
    await bot.change_presence(activity=discord.Game(name="Exploit"))


# ---- Helper function: fetch text from URL (aiohttp) ----
async def fetch_raw_text(url: str, timeout: int = 10) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as resp:
                if resp.status == 200:
                    return await resp.text()
                else:
                    return f"ERROR: HTTP {resp.status} while fetching {url}"
    except asyncio.TimeoutError:
        return f"ERROR: Timeout while fetching {url}"
    except Exception as e:
        return f"ERROR: Exception while fetching {url}: {e}"


# ---- Event: catch messages without prefix ----
@bot.event
async def on_message(message):
    # do not respond to messages from the bot itself
    if message.author.bot:
        return

    content = message.content

    # ---------- If the message contains the word "script"
    if "script" in content.lower():
        # 1) fetch the remote file content
        fetched = await fetch_raw_text(UNIVERSAL_SCRIPT_RAW_URL)

        # 2) if fetch fails, send a short error message
        if fetched.startswith("ERROR:"):
            await message.channel.send(f"⚠️ Failed to fetch script: `{fetched}`")
            await bot.process_commands(message)
            return

        # 3) send script content only (without translation)
        MAX_CHARS = 1900  # safe margin for code block wrapper
        if len(fetched) <= MAX_CHARS:
            embed_orig = discord.Embed(title="📝 Universal Script", color=0x836dc9)
            embed_orig.add_field(name="Raw content", value=f"```lua\n{fetched}\n```", inline=False)
            embed_orig.set_footer(text=f"Source: {UNIVERSAL_SCRIPT_RAW_URL}")
            await message.channel.send(embed=embed_orig)
        else:
            await message.channel.send("📝 Universal Script:")
            for i in range(0, len(fetched), MAX_CHARS):
                part = fetched[i:i+MAX_CHARS]
                await message.channel.send(f"```lua\n{part}\n```")

        return

    # ---------- Still process commands with prefix
    await bot.process_commands(message)


# ---- Basic Commands ----
@bot.command()
async def ping(ctx):
    """Test bot connection"""
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


@bot.command()
async def rules(ctx):
    """Send server rules in an embed"""
    embed = discord.Embed(
        title="📜 Server Rules",
        description=(
            "**This LUA code based server is created for educational purposes only, "
            "and we are not responsible for any of our clients using any way to violate the TOS.**\n\n"
            "We won’t tolerate our members selling any sort of illegal items, "
            "or posting malicious links. They will be instantly banned from our server.\n\n"
            "We always obey Discord TOS.\n"
            "👉 [Discord TOS](https://discord.com/terms)"
        ),
        color=0x836dc9
    )
    await ctx.send(embed=embed)


@bot.command()
async def status(ctx):
    """Send status info embed"""
    embed = discord.Embed(
        title="Status Info",
        description=(
            "🟣 - Undetected and Working\n"
            "🟢 - Working\n"
            "🟡 - Updating and Not Working\n"
            "🔴 - Down"
        ),
        color=0x836dc9
    )
    await ctx.send(embed=embed)


@bot.command()
async def download(ctx):
    """Send download link"""
    embed = discord.Embed(
        title=":inbox_tray: Download Seraphin Windows",
        description="[Download Link](https://getSeraphin.vercel.app)",
        color=0x836dc9
    )
    embed.set_footer(text="Seraphin Windows • Download Link")
    await ctx.send(embed=embed)


@bot.command()
async def changelog(ctx):
    """Send application changelog"""
    embed = discord.Embed(
        title=":clipboard: Seraphin Windows — Change Logs",
        description="Latest updates for **Seraphin Windows**",
        color=0x836dc9
    )

    embed.add_field(
        name=":sparkles: Core Changes",
        value="```md\n- Updated to newest Roblox version\n- Improved stability and performance\n- Optimized memory usage\n```",
        inline=False
    )
    embed.add_field(
        name=":hammer: Fixes",
        value="```md\n- Fixed injection bug\n```",
        inline=False
    )
    embed.add_field(
        name=":rocket: New Features",
        value="```md\n- Added Auto Update\n```",
        inline=False
    )
    embed.add_field(
        name=":inbox_tray: Download",
        value="[Download](https://getSeraphin.vercel.app)",
        inline=False
    )
    embed.set_footer(text="Seraphin Windows — Official Update")

    await ctx.send(content="@everyone", embed=embed)


@bot.command()
async def changelogscripts(ctx):
    """Send script changelog"""
    embed = discord.Embed(
        title=":clipboard: Script Change Logs",
        description="Latest updates for **Universal Script**",
        color=0x5bc0de
    )

    embed.add_field(
        name=":sparkles: Major Changes",
        value="```md\n- Added request bypass function\n- Optimized hook performance\n```",
        inline=False
    )
    embed.add_field(
        name=":hammer: Fixes",
        value="```md\n- Fixed auto execute bug\n- Fixed console output error\n```",
        inline=False
    )
    embed.add_field(
        name=":rocket: New Features",
        value="```md\n- Support Luarmor Compatibility\n- Auto detect executor\n```",
        inline=False
    )
    embed.add_field(
        name=":inbox_tray: Download / Copy",
        value="[Script Link](https://getSeraphin.vercel.app/script)",
        inline=False
    )
    embed.set_footer(text="Universal Script — Official Update")

    await ctx.send(content="@everyone", embed=embed)


@bot.command()
async def say(ctx, *, message_text: str):
    """Bot repeats your message"""
    await ctx.send(message_text)


@bot.command()
async def clear(ctx, amount: int = 5):
    """Delete messages (default 5)"""
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 {amount} messages deleted!", delete_after=3)
    else:
        await ctx.send("❌ You don’t have permission to delete messages.")


@bot.command()
async def send(ctx, *, message_text: str):
    """Send a message to a specific channel"""
    channel_id = 1396412369361436763  # replace with your target channel ID
    channel = bot.get_channel(channel_id)

    if channel:
        await channel.send(message_text)
        await ctx.send(f"✅ Message sent to <#{channel_id}>")
    else:
        await ctx.send("❌ Channel not found or bot has no access.")


@bot.command()
async def setprefix(ctx, new_prefix: str):
    """Change bot prefix"""
    global PREFIX
    PREFIX = new_prefix
    bot.command_prefix = PREFIX
    await ctx.send(f"✅ Prefix changed to `{PREFIX}`")


# ---- Run Bot ----
TOKEN = os.getenv("DISCORD_TOKEN")  # Get token from environment variable
if TOKEN is None:
    print("❌ ERROR: Token not found! Make sure DISCORD_TOKEN is set in Railway.")
else:
    bot.run(TOKEN)
