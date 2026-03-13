import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View, Select
import json
import os
import random
import time
import asyncio
from datetime import datetime
from typing import Optional

# ═══════════════════════════════════════════════════════════
#  Bot Configuration - Works on all platforms
# ═══════════════════════════════════════════════════════════
PREFIX = "!"
TOKEN = os.environ.get("TOKEN") or os.environ.get("DISCORD_TOKEN") or "YOUR_TOKEN_HERE"
LIME_COLOR = 0x00FF00

WELCOME_CHANNEL_ID = 1470539807074549850
GOODBYE_CHANNEL_ID = 1470539840314671134
YOUTUBE_CHANNEL_ID = 1470540807663517838
AUTO_ROLE_ID = 1471338474652045403
LEVEL_CHANNEL_ID = 1482151770426970292

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# Data Management
def load_data():
    try:
        if os.path.exists("data.json"):
            with open("data.json", "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return {}

def save_data(data):
    try:
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except:
        pass

def get_user(data, user_id):
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"mood": 0, "xp": 0, "level": 1, "last_collect": 0, "last_work": 0, "inventory": [], "warnings": []}
    return data[uid]

# Shop Items (60+ items!)
SHOP_ITEMS = [
    # Food
    {"id": "burger", "name": "🍔 Burger", "price": 150, "cat": "Food"},
    {"id": "pizza", "name": "🍕 Pizza", "price": 300, "cat": "Food"},
    {"id": "shawarma", "name": "🌯 Shawarma", "price": 200, "cat": "Food"},
    {"id": "couscous", "name": "🍲 Couscous", "price": 500, "cat": "Food"},
    {"id": "sushi", "name": "🍣 Sushi", "price": 800, "cat": "Food"},
    {"id": "kebab", "name": "🍢 Kebab", "price": 400, "cat": "Food"},
    {"id": "steak", "name": "🥩 Steak", "price": 900, "cat": "Food"},
    {"id": "ramen", "name": "🍜 Ramen", "price": 700, "cat": "Food"},
    {"id": "tacos", "name": "🌮 Tacos", "price": 250, "cat": "Food"},
    
    # Electronics
    {"id": "phone", "name": "📱 Phone", "price": 15000, "cat": "Electronics"},
    {"id": "iphone", "name": "📱 iPhone", "price": 35000, "cat": "Electronics"},
    {"id": "laptop", "name": "💻 Laptop", "price": 50000, "cat": "Electronics"},
    {"id": "macbook", "name": "💻 MacBook", "price": 80000, "cat": "Electronics"},
    {"id": "tv", "name": "📺 TV", "price": 20000, "cat": "Electronics"},
    {"id": "ps5", "name": "🎮 PS5", "price": 25000, "cat": "Electronics"},
    {"id": "xbox", "name": "🎮 Xbox", "price": 25000, "cat": "Electronics"},
    {"id": "camera", "name": "📷 Camera", "price": 40000, "cat": "Electronics"},
    {"id": "vr", "name": "🥽 VR", "price": 30000, "cat": "Electronics"},
    
    # Vehicles
    {"id": "bike", "name": "🏍️ Motorcycle", "price": 80000, "cat": "Vehicles"},
    {"id": "scooter", "name": "🛴 Scooter", "price": 15000, "cat": "Vehicles"},
    {"id": "car", "name": "🚗 Car", "price": 300000, "cat": "Vehicles"},
    {"id": "suv", "name": "🚙 SUV", "price": 500000, "cat": "Vehicles"},
    {"id": "sports", "name": "🏎️ Sports Car", "price": 900000, "cat": "Vehicles"},
    {"id": "ferrari", "name": "🏎️ Ferrari", "price": 2000000, "cat": "Vehicles"},
    {"id": "lambo", "name": "🏎️ Lamborghini", "price": 2500000, "cat": "Vehicles"},
    {"id": "bugatti", "name": "🏎️ Bugatti", "price": 5000000, "cat": "Vehicles"},
    {"id": "limo", "name": "🚙 Limo", "price": 1500000, "cat": "Vehicles"},
    {"id": "truck", "name": "🚚 Truck", "price": 600000, "cat": "Vehicles"},
    
    # Real Estate
    {"id": "apartment", "name": "🏠 Apartment", "price": 1000000, "cat": "Real Estate"},
    {"id": "villa", "name": "🏰 Villa", "price": 5000000, "cat": "Real Estate"},
    {"id": "mansion", "name": "🏛️ Mansion", "price": 15000000, "cat": "Real Estate"},
    {"id": "island", "name": "🏝️ Island", "price": 50000000, "cat": "Real Estate"},
    
    # Luxury
    {"id": "watch", "name": "⌚ Watch", "price": 100000, "cat": "Luxury"},
    {"id": "ring", "name": "💍 Ring", "price": 500000, "cat": "Luxury"},
    {"id": "yacht", "name": "🛥️ Yacht", "price": 10000000, "cat": "Luxury"},
    {"id": "pjet", "name": "🛩️ Private Jet", "price": 25000000, "cat": "Luxury"},
]

# Tickets
class TicketSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Support", emoji="🛠️", value="support"),
            discord.SelectOption(label="Application", emoji="📝", value="app"),
            discord.SelectOption(label="Report", emoji="⚠️", value="report"),
            discord.SelectOption(label="Complaint", emoji="📢", value="complaint"),
            discord.SelectOption(label="join game", emoji="📢", value="join"
        ]
        super().__init__(placeholder="Select type", options=options)
    
    async def callback(self, i: discord.Interaction):
        await i.response.defer(ephemeral=True)
        cat = discord.utils.get(i.guild.categories, name="📩 Tickets")
        if not cat:
            cat = await i.guild.create_category("📩 Tickets")
        
        for ch in cat.text_channels:
            if ch.topic and str(i.user.id) in ch.topic:
                return await i.followup.send(f"❌ You have an open ticket!\n{ch.mention}", ephemeral=True)
        
        num = len(cat.text_channels) + 1
        overwrites = {
            i.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            i.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            i.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        ch = await cat.create_text_channel(f"ticket-{num}", overwrites=overwrites, topic=str(i.user.id))
        
        e = discord.Embed(title=f"🎫 Ticket #{num}", description=f"Welcome {i.user.mention}!\nDescribe your issue.", color=LIME_COLOR)
        close_btn = Button(label="🔒 Close", style=discord.ButtonStyle.danger)
        
        async def close_cb(ii):
            await ii.response.send_message("🗑️ Deleting...")
            await asyncio.sleep(2)
            await ch.delete()
        
        close_btn.callback = close_cb
        v = View(timeout=None)
        v.add_item(close_btn)
        await ch.send(embed=e, view=v)
        await i.followup.send(f"✅ {ch.mention}", ephemeral=True)

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

# XO Game
class XOButton(Button):
    def __init__(self, x, y):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x, self.y = x, y
    
    async def callback(self, i: discord.Interaction):
        v = self.view
        if i.user != v.cp:
            return await i.response.send_message("❌ Not your turn!", ephemeral=True)
        if self.label != "\u200b":
            return await i.response.send_message("❌ Taken!", ephemeral=True)
        
        self.label = v.cm
        self.style = discord.ButtonStyle.primary if v.cm == "X" else discord.ButtonStyle.danger
        v.board[self.y][self.x] = v.cm
        
        if v.check_winner():
            for c in v.children:
                c.disabled = True
            return await i.response.edit_message(content=f"🎉 {v.cp.mention} wins!", view=v)
        
        if all(all(c != " " for c in r) for r in v.board):
            for c in v.children:
                c.disabled = True
            return await i.response.edit_message(content="🤝 Draw!", view=v)
        
        v.cp = v.p2 if v.cp == v.p1 else v.p1
        v.cm = "O" if v.cm == "X" else "X"
        await i.response.edit_message(content=f"{v.cp.mention}'s turn ({v.cm})", view=v)

class XOView(View):
    def __init__(self, p1, p2):
        super().__init__(timeout=300)
        self.p1, self.p2, self.cp, self.cm = p1, p2, p1, "X"
        self.board = [[" "]*3 for _ in range(3)]
        for y in range(3):
            for x in range(3):
                self.add_item(XOButton(x, y))
    
    def check_winner(self):
        for r in self.board:
            if r[0] == r[1] == r[2] != " ": return True
        for c in range(3):
            if self.board[0][c] == self.board[1][c] == self.board[2][c] != " ": return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ": return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ": return True
        return False

# Events
@bot.event
async def on_ready():
    if not hasattr(bot, '_synced'):
        bot._synced = True
        print(f"✅ {bot.user} online!")
        try:
            bot.tree.clear_commands(guild=None)
            await bot.tree.sync()
            print("✅ Commands synced")
        except Exception as e:
            print(f"❌ {e}")
        bot.add_view(TicketView())
@bot.event
async def on_member_join(m):
    r = m.guild.get_role(AUTO_ROLE_ID)
    if r:
        try:
            await m.add_roles(r)
        except:
            pass
    ch = bot.get_channel(WELCOME_CHANNEL_ID)
    if ch:
        e = discord.Embed(title="🎉 Welcome!", description=f"{m.mention} joined! 🌟", color=LIME_COLOR)
        e.set_thumbnail(url=m.display_avatar.url)
        e.set_footer(text=f"Total members: {m.guild.member_count}")
        await ch.send(embed=e)

@bot.event
async def on_member_remove(m):
    ch = bot.get_channel(GOODBYE_CHANNEL_ID)
    if ch:
        await ch.send(f"👋 {m.name} left")

@bot.event
async def on_message(msg):
    if msg.author.bot:
        return
    
    c = msg.content.strip().lower()
    
    # Arabic greetings only
    if c in ["هلا", "اهلا", "أهلا", "هلا اهلا"]:
        await msg.channel.send(f"هلا كيفك {msg.author.mention} 👋😊")
    elif c in ["سلام عليكم", "السلام عليكم", "سلام عليكم ورحمة الله وبركاته", "السلام عليكم ورحمة الله وبركاته"]:
        await msg.channel.send(f"وعليكم السلام ورحمة الله وبركاته {msg.author.mention}")
    elif c in ["hi", "hello"]:
        await msg.channel.send(f"hi, what's up {msg.author.mention}")
    
    # XP
    data = load_data()
    u = get_user(data, msg.author.id)
    u["xp"] += random.randint(5, 15)
    if u["xp"] >= u["level"] * 100:
        u["xp"] -= u["level"] * 100
        u["level"] += 1
        await msg.channel.send(f"🎉 {msg.author.mention} → Level **{u['level']}**!")
    save_data(data)
    await bot.process_commands(msg)

# ═══════════════════════════════════════════════════════════
#  ECONOMY COMMANDS - Both / and !
# ═══════════════════════════════════════════════════════════
@bot.tree.command(name="collect")
async def slash_collect(i: discord.Interaction):
    """Collect m00d every 30 min"""
    data = load_data()
    u = get_user(data, i.user.id)
    now = time.time()
    if now - u["last_collect"] < 1800:
        m = int((1800 - (now - u["last_collect"])) // 60)
        return await i.response.send_message(f"⏳ Wait {m} min", ephemeral=True)
    amt = random.randint(100, 1000)
    u["mood"] += amt
    u["last_collect"] = now
    save_data(data)
    e = discord.Embed(title="💰 Collected!", description=f"+{amt:,} m00d\n\n💵 Balance: {u['mood']:,} m00d", color=LIME_COLOR)
    await i.response.send_message(embed=e)

@bot.command(name="collect")
async def collect(ctx):
    """!collect"""
    data = load_data()
    u = get_user(data, ctx.author.id)
    now = time.time()
    if now - u["last_collect"] < 1800:
        m = int((1800 - (now - u["last_collect"])) // 60)
        return await ctx.send(f"⏳ Wait {m} min")
    amt = random.randint(100, 1000)
    u["mood"] += amt
    u["last_collect"] = now
    save_data(data)
    e = discord.Embed(title="💰 Collected!", description=f"+{amt:,} m00d\n💵 {u['mood']:,} m00d", color=LIME_COLOR)
    await ctx.send(embed=e)

@bot.tree.command(name="work")
async def slash_work(i: discord.Interaction):
    """Work and earn 10K-100K"""
    data = load_data()
    u = get_user(data, i.user.id)
    now = time.time()
    if now - u.get("last_work", 0) < 3600:
        m = int((3600 - (now - u["last_work"])) // 60)
        return await i.response.send_message(f"⏳ Rest {m} min", ephemeral=True)
    jobs = [("👨‍🍳 Chef", "Cooked"), ("🚗 Driver", "Drove"), ("💻 Coder", "Coded")]
    job, desc = random.choice(jobs)
    amt = random.randint(10000, 100000)
    u["mood"] += amt
    u["last_work"] = now
    save_data(data)
    e = discord.Embed(title=f"💼 {job}", description=f"{desc}\n+{amt:,} m00d\n\n💵 {u['mood']:,} m00d", color=LIME_COLOR)
    await i.response.send_message(embed=e)

@bot.command(name="work")
async def work(ctx):
    """!work"""
    data = load_data()
    u = get_user(data, ctx.author.id)
    now = time.time()
    if now - u.get("last_work", 0) < 3600:
        m = int((3600 - (now - u["last_work"])) // 60)
        return await ctx.send(f"⏳ Rest {m} min")
    jobs = [("👨‍🍳 Chef", "Cooked"), ("🚗 Driver", "Drove"), ("💻 Coder", "Coded")]
    job, desc = random.choice(jobs)
    amt = random.randint(10000, 100000)
    u["mood"] += amt
    u["last_work"] = now
    save_data(data)
    e = discord.Embed(title=f"💼 {job}", description=f"{desc}\n+{amt:,} m00d\n💵 {u['mood']:,} m00d", color=LIME_COLOR)
    await ctx.send(embed=e)

@bot.tree.command(name="balance")
async def slash_bal(i: discord.Interaction, member: Optional[discord.Member] = None):
    """Check balance"""
    m = member or i.user
    data = load_data()
    u = get_user(data, m.id)
    e = discord.Embed(title=f"💳 {m.display_name}", description=f"**{u['mood']:,} m00d**", color=LIME_COLOR)
    await i.response.send_message(embed=e)

@bot.command(name="balance", aliases=["bal"])
async def balance(ctx, member: discord.Member = None):
    """!balance"""
    m = member or ctx.author
    data = load_data()
    u = get_user(data, m.id)
    e = discord.Embed(title=f"💳 {m.display_name}", description=f"**{u['mood']:,} m00d**", color=LIME_COLOR)
    await ctx.send(embed=e)

@bot.tree.command(name="leaderboard")
async def slash_lb(i: discord.Interaction):
    """Top richest"""
    data = load_data()
    members = {str(m.id): m for m in i.guild.members}
    top = sorted([(uid, d) for uid, d in data.items() if uid in members], key=lambda x: x[1].get("mood", 0), reverse=True)[:10]
    e = discord.Embed(title="🏆 Richest", color=LIME_COLOR)
    medals = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
    desc = ""
    for idx, (uid, d) in enumerate(top):
        m = members.get(uid)
        name = m.display_name if m else f"User#{uid}"
        desc += f"{medals[idx]} **{name}** — {d.get('mood',0):,} m00d\n"
    e.description = desc or "No data"
    await i.response.send_message(embed=e)

@bot.command(name="leaderboard", aliases=["lb"])
async def leaderboard(ctx):
    """!leaderboard"""
    data = load_data()
    members = {str(m.id): m for m in ctx.guild.members}
    top = sorted([(uid, d) for uid, d in data.items() if uid in members], key=lambda x: x[1].get("mood", 0), reverse=True)[:10]
    e = discord.Embed(title="🏆 Richest", color=LIME_COLOR)
    medals = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
    desc = ""
    for idx, (uid, d) in enumerate(top):
        m = members.get(uid)
        name = m.display_name if m else f"User#{uid}"
        desc += f"{medals[idx]} **{name}** — {d.get('mood',0):,} m00d\n"
    e.description = desc or "No data"
    await ctx.send(embed=e)

# ═══════════════════════════════════════════════════════════
#  SHOP - Both / and !
# ═══════════════════════════════════════════════════════════
@bot.tree.command(name="shop")
async def slash_shop(i: discord.Interaction, category: Optional[str] = None):
    """Browse shop"""
    cats = {}
    for item in SHOP_ITEMS:
        c = item["cat"]
        if c not in cats:
            cats[c] = []
        cats[c].append(item)
    
    if not category:
        e = discord.Embed(title="🏪 Shop", color=LIME_COLOR)
        for c in cats:
            e.add_field(name=f"📂 {c}", value=f"`/shop category:{c}`", inline=True)
        return await i.response.send_message(embed=e)
    
    items = cats.get(category, [])
    if not items:
        return await i.response.send_message("❌ Not found!", ephemeral=True)
    
    e = discord.Embed(title=f"🏪 {category}", color=LIME_COLOR)
    for item in items[:25]:
        e.add_field(name=item["name"], value=f"{item['price']:,} m00d\n`/buy item:{item['id']}`", inline=True)
    await i.response.send_message(embed=e)

@bot.command(name="shop")
async def shop_cmd(ctx, *, category: str = None):
    """!shop [category]"""
    cats = {}
    for item in SHOP_ITEMS:
        c = item["cat"]
        if c not in cats:
            cats[c] = []
        cats[c].append(item)
    
    if not category:
        e = discord.Embed(title="🏪 Shop", color=LIME_COLOR)
        for c in cats:
            e.add_field(name=f"📂 {c}", value=f"`!shop {c}`", inline=True)
        return await ctx.send(embed=e)
    
    items = cats.get(category, [])
    if not items:
        return await ctx.send("❌ Not found!")
    
    e = discord.Embed(title=f"🏪 {category}", color=LIME_COLOR)
    for item in items[:25]:
        e.add_field(name=item["name"], value=f"{item['price']:,} m00d\n`!buy {item['id']}`", inline=True)
    await ctx.send(embed=e)

@bot.tree.command(name="buy")
async def slash_buy(i: discord.Interaction, item: str):
    """Buy item"""
    obj = next((x for x in SHOP_ITEMS if x["id"] == item), None)
    if not obj:
        return await i.response.send_message("❌ Not found!", ephemeral=True)
    data = load_data()
    u = get_user(data, i.user.id)
    if u["mood"] < obj["price"]:
        return await i.response.send_message(f"❌ Need {obj['price'] - u['mood']:,} more!", ephemeral=True)
    u["mood"] -= obj["price"]
    u["inventory"].append(item)
    save_data(data)
    e = discord.Embed(title="✅ Purchased!", description=f"{obj['name']}\n💵 {u['mood']:,} m00d", color=LIME_COLOR)
    await i.response.send_message(embed=e)

@bot.command(name="buy")
async def buy_cmd(ctx, item_id: str):
    """!buy <item>"""
    obj = next((x for x in SHOP_ITEMS if x["id"] == item_id), None)
    if not obj:
        return await ctx.send("❌ Not found!")
    data = load_data()
    u = get_user(data, ctx.author.id)
    if u["mood"] < obj["price"]:
        return await ctx.send(f"❌ Need {obj['price'] - u['mood']:,} more!")
    u["mood"] -= obj["price"]
    u["inventory"].append(item_id)
    save_data(data)
    e = discord.Embed(title="✅ Purchased!", description=f"{obj['name']}\n💵 {u['mood']:,} m00d", color=LIME_COLOR)
    await ctx.send(embed=e)

@bot.tree.command(name="inventory")
async def slash_inv(i: discord.Interaction, member: Optional[discord.Member] = None):
    """View inventory"""
    m = member or i.user
    data = load_data()
    u = get_user(data, m.id)
    inv = u.get("inventory", [])
    if not inv:
        return await i.response.send_message(f"🎒 {m.display_name}'s inventory is empty!")
    counts = {}
    for x in inv:
        counts[x] = counts.get(x, 0) + 1
    desc = ""
    for iid, cnt in counts.items():
        obj = next((x for x in SHOP_ITEMS if x["id"] == iid), None)
        if obj:
            desc += f"{obj['name']} x{cnt}\n"
    e = discord.Embed(title=f"🎒 {m.display_name}", description=desc, color=LIME_COLOR)
    await i.response.send_message(embed=e)

@bot.command(name="inventory", aliases=["inv"])
async def inventory(ctx, member: discord.Member = None):
    """!inventory"""
    m = member or ctx.author
    data = load_data()
    u = get_user(data, m.id)
    inv = u.get("inventory", [])
    if not inv:
        return await ctx.send(f"🎒 {m.display_name}'s inventory is empty!")
    counts = {}
    for x in inv:
        counts[x] = counts.get(x, 0) + 1
    desc = ""
    for iid, cnt in counts.items():
        obj = next((x for x in SHOP_ITEMS if x["id"] == iid), None)
        if obj:
            desc += f"{obj['name']} x{cnt}\n"
    e = discord.Embed(title=f"🎒 {m.display_name}", description=desc, color=LIME_COLOR)
    await ctx.send(embed=e)

# ═══════════════════════════════════════════════════════════
#  GAMES - Both / and !
# ═══════════════════════════════════════════════════════════
@bot.tree.command(name="xo")
async def slash_xo(i: discord.Interaction, opponent: discord.Member):
    """Play XO"""
    if opponent.bot or opponent == i.user:
        return await i.response.send_message("❌ Invalid opponent!", ephemeral=True)
    v = XOView(i.user, opponent)
    await i.response.send_message(f"🎮 XO Game!\n{i.user.mention} (X) vs {opponent.mention} (O)\n{i.user.mention}'s turn", view=v)

@bot.command(name="xo")
async def xo_cmd(ctx, opponent: discord.Member):
    """!xo @user"""
    if opponent.bot or opponent == ctx.author:
        return await ctx.send("❌ Invalid!")
    v = XOView(ctx.author, opponent)
    await ctx.send(f"🎮 XO!\n{ctx.author.mention} (X) vs {opponent.mention} (O)\n{ctx.author.mention}'s turn", view=v)

@bot.tree.command(name="guess")
async def slash_guess(i: discord.Interaction):
    """Guess number game"""
    num = random.randint(1, 100)
    await i.response.send_message("🎲 Guess 1-100! 6 attempts")
    
    def check(m):
        return m.author == i.user and m.channel == i.channel and m.content.isdigit()
    
    attempts = 0
    while attempts < 6:
        try:
            msg = await bot.wait_for("message", check=check, timeout=30)
            guess = int(msg.content)
            attempts += 1
            
            if guess == num:
                data = load_data()
                u = get_user(data, i.user.id)
                u["mood"] += 5000
                save_data(data)
                return await i.channel.send(f"🎉 Correct! {num}\n+5000 m00d")
            elif guess < num:
                await i.channel.send(f"📈 Higher! ({6-attempts} left)")
            else:
                await i.channel.send(f"📉 Lower! ({6-attempts} left)")
        except asyncio.TimeoutError:
            return await i.channel.send(f"⏰ Time's up! {num}")
    
    await i.channel.send(f"❌ Lost! {num}")

@bot.command(name="guess")
async def guess_cmd(ctx):
    """!guess"""
    num = random.randint(1, 100)
    await ctx.send("🎲 Guess 1-100! 6 attempts")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()
    
    attempts = 0
    while attempts < 6:
        try:
            msg = await bot.wait_for("message", check=check, timeout=30)
            guess = int(msg.content)
            attempts += 1
            
            if guess == num:
                data = load_data()
                u = get_user(data, ctx.author.id)
                u["mood"] += 5000
                save_data(data)
                return await ctx.send(f"🎉 Correct! {num}\n+5000 m00d")
            elif guess < num:
                await ctx.send(f"📈 Higher! ({6-attempts} left)")
            else:
                await ctx.send(f"📉 Lower! ({6-attempts} left)")
        except asyncio.TimeoutError:
            return await ctx.send(f"⏰ Time's up! {num}")
    
    await ctx.send(f"❌ Lost! {num}")

@bot.tree.command(name="coinflip")
async def slash_coin(i: discord.Interaction, bet: int, side: str):
    """Flip coin and bet m00d"""
    if side.lower() not in ["heads", "tails"]:
        return await i.response.send_message("❌ Choose heads or tails!", ephemeral=True)
    data = load_data()
    u = get_user(data, i.user.id)
    if bet < 100 or bet > u["mood"]:
        return await i.response.send_message(f"❌ Bet 100-{u['mood']:,} m00d!", ephemeral=True)
    
    result = random.choice(["heads", "tails"])
    if result == side.lower():
        u["mood"] += bet
        save_data(data)
        e = discord.Embed(title=f"🪙 {result.upper()}!", description=f"✅ You won!\n+{bet:,} m00d\n\n💵 {u['mood']:,} m00d", color=LIME_COLOR)
    else:
        u["mood"] -= bet
        save_data(data)
        e = discord.Embed(title=f"🪙 {result.upper()}!", description=f"❌ You lost!\n-{bet:,} m00d\n\n💵 {u['mood']:,} m00d", color=0xFF5555)
    await i.response.send_message(embed=e)

@bot.command(name="coinflip", aliases=["coin"])
async def coin_cmd(ctx, bet: int, side: str):
    """!coinflip <bet> <heads/tails>"""
    if side.lower() not in ["heads", "tails"]:
        return await ctx.send("❌ heads or tails!")
    data = load_data()
    u = get_user(data, ctx.author.id)
    if bet < 100 or bet > u["mood"]:
        return await ctx.send(f"❌ Bet 100-{u['mood']:,}!")
    
    result = random.choice(["heads", "tails"])
    if result == side.lower():
        u["mood"] += bet
        save_data(data)
        e = discord.Embed(title=f"🪙 {result.upper()}!", description=f"✅ Won! +{bet:,}\n💵 {u['mood']:,} m00d", color=LIME_COLOR)
    else:
        u["mood"] -= bet
        save_data(data)
        e = discord.Embed(title=f"🪙 {result.upper()}!", description=f"❌ Lost! -{bet:,}\n💵 {u['mood']:,} m00d", color=0xFF5555)
    await ctx.send(embed=e)

# ═══════════════════════════════════════════════════════════
#  MODERATION - Both / and !
# ═══════════════════════════════════════════════════════════
@bot.tree.command(name="ban")
@app_commands.checks.has_permissions(ban_members=True)
async def slash_ban(i: discord.Interaction, member: discord.Member, reason: Optional[str] = "No reason"):
    """Ban member"""
    await member.ban(reason=reason)
    await i.response.send_message(f"🔨 Banned {member.mention}\n{reason}")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban_cmd(ctx, member: discord.Member, *, reason: str = "No reason"):
    """!ban @user [reason]"""
    await member.ban(reason=reason)
    await ctx.send(f"🔨 Banned {member.mention}\n{reason}")

@bot.tree.command(name="kick")
@app_commands.checks.has_permissions(kick_members=True)
async def slash_kick(i: discord.Interaction, member: discord.Member, reason: Optional[str] = "No reason"):
    """Kick member"""
    await member.kick(reason=reason)
    await i.response.send_message(f"👢 Kicked {member.mention}\n{reason}")

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick_cmd(ctx, member: discord.Member, *, reason: str = "No reason"):
    """!kick @user [reason]"""
    await member.kick(reason=reason)
    await ctx.send(f"👢 Kicked {member.mention}\n{reason}")

@bot.tree.command(name="clear")
@app_commands.checks.has_permissions(manage_messages=True)
async def slash_clear(i: discord.Interaction, amount: int):
    """Clear messages"""
    if amount < 1 or amount > 100:
        return await i.response.send_message("❌ 1-100!", ephemeral=True)
    await i.response.defer(ephemeral=True)
    deleted = await i.channel.purge(limit=amount)
    await i.followup.send(f"🗑️ Deleted {len(deleted)}", ephemeral=True)

@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear_cmd(ctx, amount: int):
    """!clear <amount>"""
    if amount < 1 or amount > 100:
        return await ctx.send("❌ 1-100!")
    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🗑️ Deleted {len(deleted)-1}", delete_after=3)

# ═══════════════════════════════════════════════════════════
#  ADMIN - Both / and !
# ═══════════════════════════════════════════════════════════
@bot.tree.command(name="setup")
@app_commands.checks.has_permissions(administrator=True)
async def setup(i: discord.Interaction, channel: discord.TextChannel):
    """Setup tickets"""
    e = discord.Embed(title="🎫 Tickets", description="Select type below", color=LIME_COLOR)
    await channel.send(embed=e, view=TicketView())
    await i.response.send_message(f"✅ Done! {channel.mention}", ephemeral=True)

@bot.command(name="setup")
@commands.has_permissions(administrator=True)
async def setup_cmd(ctx, channel: discord.TextChannel):
    """!setup #channel"""
    e = discord.Embed(title="🎫 Tickets", description="Select type", color=LIME_COLOR)
    await channel.send(embed=e, view=TicketView())
    await ctx.send(f"✅ {channel.mention}")

@bot.tree.command(name="add")
@app_commands.checks.has_permissions(administrator=True)
async def slash_add(i: discord.Interaction, member: discord.Member, amount: int):
    """Add m00d"""
    data = load_data()
    u = get_user(data, member.id)
    u["mood"] += amount
    save_data(data)
    await i.response.send_message(f"✅ +{amount:,} → {member.mention}\n💵 {u['mood']:,} m00d")

@bot.command(name="add")
@commands.has_permissions(administrator=True)
async def add_cmd(ctx, member: discord.Member, amount: int):
    """!add @user <amount>"""
    data = load_data()
    u = get_user(data, member.id)
    u["mood"] += amount
    save_data(data)
    await ctx.send(f"✅ +{amount:,} → {member.mention}\n💵 {u['mood']:,} m00d")

@bot.tree.command(name="remove")
@app_commands.checks.has_permissions(administrator=True)
async def slash_remove(i: discord.Interaction, member: discord.Member, amount: int):
    """Remove m00d"""
    data = load_data()
    u = get_user(data, member.id)
    u["mood"] = max(0, u["mood"] - amount)
    save_data(data)
    await i.response.send_message(f"✅ -{amount:,} → {member.mention}\n💵 {u['mood']:,} m00d")

@bot.command(name="remove")
@commands.has_permissions(administrator=True)
async def remove_cmd(ctx, member: discord.Member, amount: int):
    """!remove @user <amount>"""
    data = load_data()
    u = get_user(data, member.id)
    u["mood"] = max(0, u["mood"] - amount)
    save_data(data)
    await ctx.send(f"✅ -{amount:,} → {member.mention}\n💵 {u['mood']:,} m00d")

@bot.tree.command(name="help")
async def help_slash(i: discord.Interaction):
    """Bot commands"""
    e = discord.Embed(title="📖 Commands", description="Use / or !", color=LIME_COLOR)
    e.add_field(name="💰 Economy", value="`/collect` `/work` `/balance` `/leaderboard`", inline=False)
    e.add_field(name="🏪 Shop", value="`/shop` `/buy` `/inventory`", inline=False)
    e.add_field(name="🎮 Games", value="`/xo` `/guess` `/coinflip`", inline=False)
    e.add_field(name="🛡️ Mod", value="`/ban` `/kick` `/clear`", inline=False)
    e.add_field(name="👑 Admin", value="`/setup` `/add` `/remove`", inline=False)
    await i.response.send_message(embed=e)

@bot.command(name="help")
async def help_cmd(ctx):
    """!help"""
    e = discord.Embed(title="📖 Commands", description="Use / or !", color=LIME_COLOR)
    e.add_field(name="💰 Economy", value="`!collect` `!work` `!balance` `!leaderboard`", inline=False)
    e.add_field(name="🏪 Shop", value="`!shop` `!buy` `!inventory`", inline=False)
    e.add_field(name="🎮 Games", value="`!xo` `!guess` `!coinflip`", inline=False)
    e.add_field(name="🛡️ Mod", value="`!ban` `!kick` `!clear`", inline=False)
    e.add_field(name="👑 Admin", value="`!setup` `!add` `!remove`", inline=False)
    await ctx.send(embed=e)

# ═══════════════════════════════════════════════════════════
#  Party Games System (with - to join)
# ═══════════════════════════════════════════════════════════
active_games = {}

class JoinGameView(View):
    def __init__(self, game_id, host):
        super().__init__(timeout=60)
        self.game_id = game_id
        self.host = host
        self.players = [host]
    
    @discord.ui.button(label="➕ Join Game", style=discord.ButtonStyle.green, custom_id="join_game")
    async def join_btn(self, interaction: discord.Interaction, button: Button):
        if interaction.user in self.players:
            return await interaction.response.send_message("❌ Already joined!", ephemeral=True)
        
        self.players.append(interaction.user)
        await interaction.response.send_message(f"✅ Joined! Total players: {len(self.players)}", ephemeral=True)

@bot.tree.command(name="trivia")
async def trivia(i: discord.Interaction):
    """Trivia quiz game"""
    questions = [
        {"q": "What is 2+2?", "a": ["4", "four"]},
        {"q": "Capital of France?", "a": ["paris"]},
        {"q": "Who created Discord?", "a": ["jason citron", "jason"]},
        {"q": "What year is it?", "a": ["2026"]},
        {"q": "Largest planet?", "a": ["jupiter"]},
    ]
    
    question = random.choice(questions)
    await i.response.send_message(f"❓ **Trivia**: {question['q']}\nType `-answer <your answer>` to respond!")
    
    def check(m):
        return m.channel == i.channel and m.content.startswith("-answer ")
    
    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        answer = msg.content[8:].strip().lower()
        
        if answer in question['a']:
            data = load_data()
            user = get_user(data, msg.author.id)
            user["mood"] += 1000
            save_data(data)
            await i.channel.send(f"🎉 {msg.author.mention} got it right! +1000 m00d")
        else:
            await i.channel.send(f"❌ Wrong! Answer: {question['a'][0]}")
    except asyncio.TimeoutError:
        await i.channel.send(f"⏰ Time's up! Answer: {question['a'][0]}")

@bot.command(name="trivia")
async def trivia_cmd(ctx):
    """!trivia"""
    questions = [
        {"q": "What is 2+2?", "a": ["4", "four"]},
        {"q": "Capital of France?", "a": ["paris"]},
        {"q": "Who created Discord?", "a": ["jason citron", "jason"]},
        {"q": "What year is it?", "a": ["2026"]},
        {"q": "Largest planet?", "a": ["jupiter"]},
    ]
    
    question = random.choice(questions)
    await ctx.send(f"❓ **Trivia**: {question['q']}\nType `-answer <your answer>`!")
    
    def check(m):
        return m.channel == ctx.channel and m.content.startswith("-answer ")
    
    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        answer = msg.content[8:].strip().lower()
        
        if answer in question['a']:
            data = load_data()
            user = get_user(data, msg.author.id)
            user["mood"] += 1000
            save_data(data)
            await ctx.send(f"🎉 {msg.author.mention} correct! +1000 m00d")
        else:
            await ctx.send(f"❌ Wrong! Answer: {question['a'][0]}")
    except asyncio.TimeoutError:
        await ctx.send(f"⏰ Time's up! Answer: {question['a'][0]}")

@bot.tree.command(name="coinflip")
async def coinflip(i: discord.Interaction):
    """Flip a coin"""
    result = random.choice(["Heads", "Tails"])
    await i.response.send_message(f"🪙 **Coin Flip**: {result}!")

@bot.command(name="coinflip", aliases=["flip"])
async def coinflip_cmd(ctx):
    """!coinflip"""
    result = random.choice(["Heads", "Tails"])
    await ctx.send(f"🪙 {result}!")

@bot.tree.command(name="dice")
async def dice(i: discord.Interaction, sides: int = 6):
    """Roll a dice"""
    result = random.randint(1, sides)
    await i.response.send_message(f"🎲 Rolled a **{result}** (d{sides})")

@bot.command(name="dice", aliases=["roll"])
async def dice_cmd(ctx, sides: int = 6):
    """!dice [sides]"""
    result = random.randint(1, sides)
    await ctx.send(f"🎲 {result} (d{sides})")

@bot.tree.command(name="8ball")
async def eightball(i: discord.Interaction, question: str):
    """Ask the magic 8ball"""
    answers = ["Yes", "No", "Maybe", "Definitely", "Absolutely not", "Ask again later", "Probably", "Unlikely"]
    await i.response.send_message(f"🎱 **{question}**\n{random.choice(answers)}")

@bot.command(name="8ball")
async def eightball_cmd(ctx, *, question: str):
    """!8ball <question>"""
    answers = ["Yes", "No", "Maybe", "Definitely", "Absolutely not", "Ask again later", "Probably", "Unlikely"]
    await ctx.send(f"🎱 {random.choice(answers)}")

@bot.tree.command(name="rps")
async def rps(i: discord.Interaction, choice: str):
    """Rock Paper Scissors"""
    choices = ["rock", "paper", "scissors"]
    if choice.lower() not in choices:
        return await i.response.send_message("❌ Choose: rock, paper, scissors", ephemeral=True)
    
    bot_choice = random.choice(choices)
    player = choice.lower()
    
    if player == bot_choice:
        result = "🤝 Draw!"
    elif (player == "rock" and bot_choice == "scissors") or \
         (player == "paper" and bot_choice == "rock") or \
         (player == "scissors" and bot_choice == "paper"):
        result = "🎉 You win!"
        data = load_data()
        user = get_user(data, i.user.id)
        user["mood"] += 500
        save_data(data)
    else:
        result = "❌ You lose!"
    
    await i.response.send_message(f"**You**: {player}\n**Bot**: {bot_choice}\n\n{result}")

@bot.command(name="rps")
async def rps_cmd(ctx, choice: str):
    """!rps <rock/paper/scissors>"""
    choices = ["rock", "paper", "scissors"]
    if choice.lower() not in choices:
        return await ctx.send("❌ Choose: rock, paper, scissors")
    
    bot_choice = random.choice(choices)
    player = choice.lower()
    
    if player == bot_choice:
        result = "🤝 Draw!"
    elif (player == "rock" and bot_choice == "scissors") or \
         (player == "paper" and bot_choice == "rock") or \
         (player == "scissors" and bot_choice == "paper"):
        result = "🎉 Win! +500 m00d"
        data = load_data()
        user = get_user(data, ctx.author.id)
        user["mood"] += 500
        save_data(data)
    else:
        result = "❌ Lose!"
    
    await ctx.send(f"You: {player} | Bot: {bot_choice}\n{result}")

@bot.tree.command(name="slots")
async def slots(i: discord.Interaction):
    """Slot machine"""
    symbols = ["🍒", "🍋", "🍊", "💎", "7️⃣"]
    result = [random.choice(symbols) for _ in range(3)]
    
    data = load_data()
    user = get_user(data, i.user.id)
    
    if result[0] == result[1] == result[2]:
        prize = 5000
        user["mood"] += prize
        save_data(data)
        await i.response.send_message(f"🎰 {' '.join(result)}\n🎉 JACKPOT! +{prize} m00d")
    elif result[0] == result[1] or result[1] == result[2]:
        prize = 500
        user["mood"] += prize
        save_data(data)
        await i.response.send_message(f"🎰 {' '.join(result)}\n✅ Match! +{prize} m00d")
    else:
        await i.response.send_message(f"🎰 {' '.join(result)}\n❌ No match!")

@bot.command(name="slots")
async def slots_cmd(ctx):
    """!slots"""
    symbols = ["🍒", "🍋", "🍊", "💎", "7️⃣"]
    result = [random.choice(symbols) for _ in range(3)]
    
    data = load_data()
    user = get_user(data, ctx.author.id)
    
    if result[0] == result[1] == result[2]:
        prize = 5000
        user["mood"] += prize
        save_data(data)
        await ctx.send(f"🎰 {' '.join(result)}\n🎉 JACKPOT! +{prize} m00d")
    elif result[0] == result[1] or result[1] == result[2]:
        prize = 500
        user["mood"] += prize
        save_data(data)
        await ctx.send(f"🎰 {' '.join(result)}\n✅ +{prize} m00d")
    else:
        await ctx.send(f"🎰 {' '.join(result)}\n❌ No match!")

# Run
if __name__ == "__main__":
    if not TOKEN or TOKEN == "YOUR_TOKEN_HERE":
        print("❌ TOKEN not found!")
    else:
        bot.run(TOKEN)
