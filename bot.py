import discord
from discord.ext import commands
import os

# ---- Konfigurasi ----
PREFIX = "!"  # Prefix command bisa diganti, misal: "?", "."

# intents diperlukan agar bot bisa membaca pesan/member
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)


# ---- Event Saat Bot Aktif ----
@bot.event
async def on_ready():
    print(f"✅ Bot {bot.user} sudah online!")
    await bot.change_presence(activity=discord.Game(name="Exploit"))


# ---- Command Dasar ----
@bot.command()
async def ping(ctx):
    """Tes koneksi bot"""
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


@bot.command()
async def rules(ctx):
    """Kirim aturan server dalam embed"""
    embed = discord.Embed(
        title="📜 Server Rules",
        description=(
            "**This LUA code based server are created for educational purposes only, "
            "and we are not responsible for any of our clients using any way to violate the TOS.**\n\n"
            "We won't tolerate our members that are selling any sort of illegal items, "
            "or any link malicious, They will be banned instantly from our server.\n\n"
            "We always obey the Discord TOS.\n"
            "👉 [Discord TOS](https://discord.com/terms)"
        ),
        color=0xfc0404
    )
    await ctx.send(embed=embed)


@bot.command()
async def status(ctx):
    """Kirim status info embed"""
    embed = discord.Embed(
        title="Status Info",
        description=(
            "🟣 - Undetected and Working\n"
            "🟢 - Working\n"
            "🟡 - Updating and Not Working\n"
            "🔴 - Down"
        ),
        color=0xfc0404
    )
    await ctx.send(embed=embed)


@bot.command()
async def download(ctx):
    """Kasih link download"""
    embed = discord.Embed(
        title=":inbox_tray: Download Seraphin Windows ",
        description="[Download Link](https://getSeraphin.vercel.app)",
        color=0xfc0404
    )
    embed.set_footer(text="Seraphin Windows  • Download Link")
    await ctx.send(embed=embed)


@bot.command()
async def changelog(ctx):
    """Kirim changelog rapi dengan embed"""
    embed = discord.Embed(
        title=":clipboard: Seraphin Windows  — Change Logs",
        description="Update new for **Seraphin Windows **",
        color=0xfc0404
    )

    embed.add_field(
        name=":sparkles: Core Changes",
        value="```md\n- Updated to newest Roblox version\n- Improved stability and performance\n- Optimized memory usage\n```",
        inline=False
    )
    embed.add_field(
        name=":hammer: Fixes",
        value="```md\n- Fixxed Injection Bug\n```",
        inline=False
    )
    embed.add_field(
        name=":rocket: New Features",
        value="```md\n- Add Auto Update\n```",
        inline=False
    )
    embed.add_field(
        name=":inbox_tray: Download",
        value="[download](https://getSeraphin.vercel.app)",
        inline=False
    )
    embed.set_footer(text="Seraphin Windows  — Official Update")

    await ctx.send(content="@everyone", embed=embed)


@bot.command()
async def say(ctx, *, pesan: str):
    """Bot mengulangi pesanmu"""
    await ctx.send(pesan)


@bot.command()
async def clear(ctx, jumlah: int = 5):
    """Hapus pesan (default 5)"""
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=jumlah + 1)
        await ctx.send(f"🧹 {jumlah} pesan dihapus!", delete_after=3)
    else:
        await ctx.send("❌ Kamu tidak punya izin hapus pesan.")


@bot.command()
async def kirim(ctx, *, pesan: str):
    """Kirim pesan ke channel tertentu"""
    channel_id = 1396412369361436763  # ganti dengan ID channel target
    channel = bot.get_channel(channel_id)

    if channel:
        await channel.send(pesan)
        await ctx.send(f"✅ Pesan terkirim ke <#{channel_id}>")
    else:
        await ctx.send("❌ Channel tidak ditemukan atau bot tidak punya akses.")


@bot.command()
async def setprefix(ctx, prefix_baru: str):
    """Ganti prefix bot"""
    global PREFIX
    PREFIX = prefix_baru
    bot.command_prefix = PREFIX
    await ctx.send(f"✅ Prefix diganti jadi `{PREFIX}`")


# ---- Jalankan Bot ----
TOKEN = os.getenv("DISCORD_TOKEN")  # Ambil token dari environment variable
if TOKEN is None:
    print("❌ ERROR: Token tidak ditemukan! Pastikan DISCORD_TOKEN sudah diset di Railway.")
else:
    bot.run(TOKEN)


