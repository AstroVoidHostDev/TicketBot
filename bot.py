from dotenv import load_dotenv
import discord
from discord.ext import commands
import json, os, io
from datetime import datetime

# ===== ENV =====
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
BOT_NAME = os.getenv("TICKET_BOT_NAME", "Ticket Bot")  # default fallback

# ===== CONFIG =====
def load_config():
    if not os.path.exists("config.json"):
        with open("config.json", "w") as f:
            json.dump({"servers": {}}, f)
    return json.load(open("config.json"))

def save_config(data):
    json.dump(data, open("config.json", "w"), indent=4)

config = load_config()

# ===== BOT =====
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)

# ===== ADMIN CHECK =====
async def is_admin(member):
    return member.guild_permissions.administrator

# =========================
# 🎯 DROPDOWN SELECT
# =========================
class TicketDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Support", emoji="🛠️", description="General Help"),
            discord.SelectOption(label="Bug Report", emoji="🐞", description="Report a bug"),
            discord.SelectOption(label="Purchase", emoji="💰", description="Buy something"),
            discord.SelectOption(label="Other", emoji="📩", description="Other queries"),
        ]
        super().__init__(
            placeholder="Select A Option According Your Need",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        choice = self.values[0]

        data = config["servers"].get(str(guild.id), {})
        category = discord.utils.get(guild.categories, id=data.get("category_id"))

        if not category:
            await interaction.response.send_message("❌ Setup nahi hua!", ephemeral=True)
            return

        # Already ticket check
        for ch in category.channels:
            if str(user.id) in ch.name:
                await interaction.response.send_message("❌ Already ticket Is Opened!", ephemeral=True)
                return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        channel = await guild.create_text_channel(
            name=f"{choice.lower()}-{user.id}",
            category=category,
            overwrites=overwrites
        )

        embed = discord.Embed(
            title=f"🎟️ {choice} Ticket",
            description=f"{user.mention} welcome!\nExplain your issue.\nStaff will respond soon 🚀",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"{BOT_NAME} ⚡ | {datetime.now().strftime('%d/%m %H:%M')}")

        await channel.send(embed=embed, view=CloseView())
        await interaction.response.send_message(f"✅ Ticket Created: {channel.mention}", ephemeral=True)

# =========================
# VIEW
# =========================
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketDropdown())

# =========================
# CLOSE BUTTON
# =========================
class CloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Close Ticket", style=discord.ButtonStyle.danger)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await is_admin(interaction.user):
            await interaction.response.send_message("❌ Only staff!", ephemeral=True)
            return

        channel = interaction.channel
        guild = interaction.guild
        data = config["servers"].get(str(guild.id), {})
        log_channel = bot.get_channel(data.get("log_channel_id"))

        msgs = [f"{m.author}: {m.content}" async for m in channel.history(limit=200)]
        file = discord.File(io.StringIO("\n".join(msgs)), filename=f"{channel.name}.txt")

        embed = discord.Embed(
            title="📜 Ticket Closed",
            description=f"{channel.name}\nClosed by {interaction.user.mention}",
            color=discord.Color.red()
        )

        if log_channel:
            await log_channel.send(embed=embed, file=file)

        await interaction.response.send_message("Closing...", ephemeral=True)
        await channel.delete()

# =========================
# SETUP
# =========================
@bot.tree.command(name="setup", description="Setup ticket system")
@commands.has_permissions(administrator=True)
async def setup(interaction: discord.Interaction, category: discord.CategoryChannel, log_channel: discord.TextChannel):
    config["servers"][str(interaction.guild.id)] = {
        "category_id": category.id,
        "log_channel_id": log_channel.id
    }
    save_config(config)
    await interaction.response.send_message("✅ Setup Done!", ephemeral=True)

# =========================
# 🔥 ULTRA PANEL
# =========================
@bot.command()
@commands.has_permissions(administrator=True)
async def panel(ctx):
    embed = discord.Embed(
        title=f"🎟️ {BOT_NAME} Ticket Menu",
        description=(
            "✨ **Welcome to Our Professional Support Hub** ✨\n\n"
            "🔮 **Quick Guide:**\n"
            "📋 Review our FAQ & Guidelines before submitting\n"
            "🚀 Our expert team responds within minutes\n"
            "🎈 Select your ticket type below to get started\n"
            "🛡️ One ticket per issue for optimal service\n\n"
            "💎 *We're here to deliver excellence, every time!*"
        ),
        color=discord.Color.purple()
    )

    embed.set_image(url="https://media.discordapp.net/attachments/1406117175974039602/1490014504891715736/standard_1.gif?ex=69d283a5&is=69d13225&hm=9003f130a1587e999c5d8932e7c2b473e81e5ccc60a63f31851e562801d5ae4d&=&width=550&height=309")
    embed.set_footer(text=f"{BOT_NAME} ⚡ | Ultimate Tickets")

    await ctx.send(embed=embed, view=TicketView())

# =========================
# READY
# =========================
@bot.event
async def on_ready():
    print(f"🔥 Logged in as {bot.user} | {BOT_NAME}")
    await bot.tree.sync()

# =========================
# RUN
# =========================
bot.run(TOKEN)
