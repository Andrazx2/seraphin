import discord
from discord.ext import commands
from discord import app_commands
import os

# ---- Configuration ----
PREFIX = "!"
UNIVERSAL_SCRIPT_RAW_URL = "https://raw.githubusercontent.com/nniellx/SeraphinHub/main/SeraphinMain.lua"
LOADSTRING_CODE = f'loadstring(game:HttpGet("{UNIVERSAL_SCRIPT_RAW_URL}"))()'
ROLE_ID = 1415257513368227992  # role yg bisa buat script publik

# intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.bans = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# ---- Event when bot is ready ----
@bot.event
async def on_ready():
    print(f"✅ Bot {bot.user} is now online!")
    try:
        await bot.tree.sync()
        print("🔧 Slash commands synced!")
    except Exception as e:
        print(f"❌ Error syncing slash commands: {e}")

# ---- Helper: cek role ----
def has_script_role(member: discord.Member) -> bool:
    return any(role.id == ROLE_ID for role in member.roles)

# ---- Moderation Commands ----
@bot.command()
async def ban(ctx, user_id: int, *, reason: str = "No reason provided"):
    if not any(role.id == ROLE_ID for role in ctx.author.roles):
        await ctx.send("❌ Kamu tidak punya izin untuk ban.")
        return
    try:
        user = await bot.fetch_user(user_id)
        try:
            await user.send(f"🚫 Kamu telah diban dari server **{ctx.guild.name}**.\n📝 Reason: {reason}")
        except:
            pass
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f"✅ {user} telah dibanned.\n📝 Reason: {reason}")
    except Exception as e:
        await ctx.send(f"❌ Gagal ban user. Error: {e}")

@bot.command()
async def unban(ctx, user_id: int):
    if not any(role.id == ROLE_ID for role in ctx.author.roles):
        await ctx.send("❌ Kamu tidak punya izin untuk unban.")
        return
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"✅ {user} telah di-unban.")
    except Exception as e:
        await ctx.send(f"❌ Gagal unban user. Error: {e}")

@bot.command()
async def banlist(ctx):
    if not any(role.id == ROLE_ID for role in ctx.author.roles):
        await ctx.send("❌ Kamu tidak punya izin untuk melihat ban list.")
        return
    try:
        bans = await ctx.guild.bans()
        if not bans:
            await ctx.send("📋 Ban list kosong.")
            return
        embed = discord.Embed(
            title="📋 Ban List",
            description=f"Total: {len(bans)} user(s) diban",
            color=0xe74c3c
        )
        for entry in bans[:10]:
            embed.add_field(
                name=f"{entry.user} ({entry.user.id})",
                value=f"Reason: {entry.reason or 'Tidak ada reason'}",
                inline=False
            )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Gagal mengambil ban list. Error: {e}")

# ---- Basic Commands ----
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command()
async def rules(ctx):
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
    embed = discord.Embed(
        title=":inbox_tray: Download Seraphin Windows",
        description="[Download Link](https://getSeraphin.vercel.app)",
        color=0x836dc9
    )
    embed.set_footer(text="Seraphin Windows • Download Link")
    await ctx.send(embed=embed)

@bot.command()
async def changelog(ctx):
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
    await ctx.send(message_text)

@bot.command()
async def clear(ctx, amount: int = 5):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 {amount} messages deleted!", delete_after=3)
    else:
        await ctx.send("❌ You don’t have permission to delete messages.")

@bot.command()
async def send(ctx, *, message_text: str):
    channel_id = 1396412369361436763  # ganti dengan channel ID target
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message_text)
        await ctx.send(f"✅ Message sent to <#{channel_id}>")
    else:
        await ctx.send("❌ Channel not found or bot has no access.")

@bot.command()
async def setprefix(ctx, new_prefix: str):
    global PREFIX
    PREFIX = new_prefix
    bot.command_prefix = PREFIX
    await ctx.send(f"✅ Prefix changed to `{PREFIX}`")

# ---- Slash Command: /script ----
@bot.tree.command(name="script", description="Get the Seraphin Script Loader")
async def script_slash(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📝 Seraphin Script Loader",
        description=f"```lua\n{LOADSTRING_CODE}\n```",
        color=0x836dc9
    )
    embed.set_footer(text="Copy & paste into your executor")

    if has_script_role(interaction.user):
        # Role khusus -> publik
        await interaction.response.send_message(embed=embed, ephemeral=False)
    else:
        # User biasa -> ephemeral (hanya dia lihat)
        await interaction.response.send_message(embed=embed, ephemeral=True)

# ---- Run Bot ----
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN is None:
    print("❌ ERROR: Token not found! Make sure DISCORD_TOKEN is set.")
else:
    bot.run(TOKEN)
