import discord
from discord.ext import commands
import os

# ---- Configuration ----
PREFIX = "!"  # Can be changed
UNIVERSAL_SCRIPT_RAW_URL = "https://raw.githubusercontent.com/nniellx/SeraphinHub/main/SeraphinMain.lua"
LOADSTRING_CODE = f'loadstring(game:HttpGet("{UNIVERSAL_SCRIPT_RAW_URL}"))()'

# intents so the bot can read message content and members
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# ---- Event when bot is ready ----
@bot.event
async def on_ready():
    print(f"✅ Bot {bot.user} is now online!")
    await bot.change_presence(activity=discord.Game(name="Exploit"))


# ---- Event: catch messages without prefix ----
@bot.event
async def on_message(message):
    # ignore messages from the bot itself
    if message.author.bot:
        return

    content = message.content

    # If message contains the word "script"
    if "script" in content.lower():
        embed = discord.Embed(
            title="📝 Universal Script Loader",
            description=f"```lua\n{LOADSTRING_CODE}\n```",
            color=0x836dc9
        )
        embed.set_footer(text="Copy & paste into your executor")
        await message.channel.send(embed=embed)
        return

    # still allow prefix commands to work
    await bot.process_commands(message)


# ---- Basic Commands ----
@bot.command()
async def ping(ctx):
    """Test bot connection"""
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


@bot.command()
async def rules(ctx):
    """Send server rules"""
    embed = discord.Embed(
        description=(
            "**This LUA code-based server is for educational purposes only. "
            "We are not responsible for any misuse that violates TOS.**\n\n"
            "Members selling illegal items or posting malicious links will be banned instantly.\n\n"
            "We always follow Discord TOS.\n"
            "👉 [Discord TOS](https://discord.com/terms)"
        ),
        color=0x836dc9
    )
    await ctx.send(embed=embed)


@bot.command()
async def status(ctx):
    """Send status info"""
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
    """Send a message to a specific channel (change channel_id)"""
    channel_id = 1396412369361436763  # replace with your channel ID
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


@bot.command()
async def script(ctx):
    """Send loadstring (command alternative to typing 'script')"""
    embed = discord.Embed(
        title="📝 Universal Script Loader",
        description=f"```lua\n{LOADSTRING_CODE}\n```",
        color=0x836dc9
    )
    embed.set_footer(text="Copy & paste into your executor")
    await ctx.send(embed=embed)


# ---- Run Bot ----
TOKEN = os.getenv("DISCORD_TOKEN")  # get token from environment
if TOKEN is None:
    print("❌ ERROR: Token not found! Make sure DISCORD_TOKEN is set.")
else:
    bot.run(TOKEN)
