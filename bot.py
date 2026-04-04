#bot.py for ticketbot By ITZ_YTANSH
from dotenv import load_dotenv
import discord
from discord.ext import commands
import json, os, io, asyncio
from datetime import datetime

# ===== ENV =====
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
BOT_NAME = os.getenv("TICKET_BOT_NAME", "Ticket Bot")

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
            discord.SelectOption(label="Support", emoji="🛠️"),
            discord.SelectOption(label="Bug Report", emoji="🐞"),
            discord.SelectOption(label="Purchase", emoji="💰"),
            discord.SelectOption(label="Other", emoji="📩"),
        ]
        super().__init__(
            placeholder="Select Ticket Category",
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

        # already ticket check
        for ch in category.channels:
            if str(user.id) in ch.name:
                await interaction.response.send_message("❌ Already ticket open!", ephemeral=True)
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
            description=f"{user.mention}, explain your issue.\nStaff will help you soon 🚀",
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
# CLOSE + CLAIM
# =========================
class CloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.claimed_by = None

    @discord.ui.button(label="👑 Claim Ticket", style=discord.ButtonStyle.primary)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await is_admin(interaction.user):
            await interaction.response.send_message("❌ Only staff!", ephemeral=True)
            return

        channel = interaction.channel

        # add ✔ to name
        if "✔" not in channel.name:
            await channel.edit(name=f"✔-{channel.name}")

        self.claimed_by = interaction.user

        await interaction.response.send_message(
            f"✅ Ticket claimed by {interaction.user.mention}"
        )

    @discord.ui.button(label="🔒 Close Ticket", style=discord.ButtonStyle.danger)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await is_admin(interaction.user):
            await interaction.response.send_message("❌ Only staff!", ephemeral=True)
            return

        channel = interaction.channel

        # get ticket user
        try:
            user_id = int(channel.name.split("-")[-1])
            ticket_user = await bot.fetch_user(user_id)
        except:
            ticket_user = None

        # transcript
        msgs = []
        async for m in channel.history(limit=200, oldest_first=True):
            msgs.append(f"{m.author}: {m.content}")

        file = discord.File(io.StringIO("\n".join(msgs)), filename=f"{channel.name}.txt")

        # DM only
        if ticket_user:
            try:
                embed = discord.Embed(
                    title="📩 Ticket Closed",
                    description=f"Your ticket `{channel.name}` has been closed.",
                    color=discord.Color.orange()
                )
                if self.claimed_by:
                    embed.add_field(name="Claimed By", value=self.claimed_by.mention)

                await ticket_user.send(embed=embed, file=file)
            except:
                pass

        await interaction.response.send_message("Closing...", ephemeral=True)
        await channel.delete()

# =========================
# AUTO CLOSE (3 DAYS)
# =========================
async def auto_close():
    await bot.wait_until_ready()

    while True:
        for guild in bot.guilds:
            data = config["servers"].get(str(guild.id), {})
            category = discord.utils.get(guild.categories, id=data.get("category_id"))

            if not category:
                continue

            for ch in category.channels:
                # skip claimed
                if "✔" in ch.name:
                    continue

                # 3 days
                if (discord.utils.utcnow() - ch.created_at).days >= 3:
                    try:
                        await ch.delete()
                    except:
                        pass

        await asyncio.sleep(3600)

# =========================
# SETUP
# =========================
@bot.tree.command(name="setup")
@commands.has_permissions(administrator=True)
async def setup(interaction: discord.Interaction, category: discord.CategoryChannel):
    config["servers"][str(interaction.guild.id)] = {
        "category_id": category.id
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
        title=f"🎟️ {BOT_NAME} Menu",
        description=(
                "✨ **Welcome to Our Professional Support Hub** ✨\n\n"

                "🔮 **Getting Started:**\n"
                "📋 Please take a moment to review our `FAQ` and Guidelines before submitting a request to ensure faster assistance\n" 
                "🚀 Our `dedicated` support team strives to respond as quickly as `possible`, typically within minutes\n"  
                "🎯 Choose the appropriate ticket category below to help us understand and resolve your issue efficiently\n"  
                "🛡️ Kindly maintain one ticket per `issue` to keep support organized and effective\n\n"  

                "💼 **Our Commitment:**\n"  
                "We are dedicated to providing reliable, high-quality support and ensuring every user receives the best possible experience.\n\n"

               "💎 *Delivering excellence with every interaction — we’re here to `help`!*\n"
    
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
    print(f"🔥 Logged in as {bot.user}")

    # 🎯 BOT STATUS
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{BOT_NAME}"
        ),
        status=discord.Status.online
    )

    bot.loop.create_task(auto_close())
    await bot.tree.sync()

# =========================
# RUN
# =========================
bot.run(TOKEN)
