import discord
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.members = True  # ให้บอทเห็นสมาชิกทั้งหมด
intents.presences = True  # ให้บอทเห็นสถานะออนไลน์ของสมาชิก

bot = commands.Bot(command_prefix="!", intents=intents)

# ใส่ ID ของ 5 ห้องที่ต้องการเปลี่ยนชื่อ
channel_ids = [
    1349385282264367127,  # ห้องที่ 1
    1349429818831405117,  # ห้องที่ 2
    1349429843552505857,  # ห้องที่ 3
    1349429877908176958,  # ห้องที่ 4
    1349431493465997323,  # ห้องที่ 5
]

# กำหนดบทบาทที่ต้องการให้แสดง (แก้ชื่อให้สั้นลง)
selected_roles = {
    "Admin LZR": "〘AD〙",
    "〘SS〙ตำรวจ LZR": "〘SS〙",
    "〘PR〙เอนเตอร์เทน LZR": "〘PR〙",
    "〘CL〙 ที่ปรึกษา LZR": "〘CL〙",
    "〘LD〙หมอดูประจำดิส LZR": "〘LD〙"
}

@bot.event
async def on_ready():
    update_channel_names.start()
    print(f'Logged in as {bot.user}')

@tasks.loop(minutes=1)  # อัปเดตทุก 1 นาที
async def update_channel_names():
    guild = bot.guilds[0]  # ใช้เซิร์ฟเวอร์แรกที่บอทอยู่

    # นับจำนวนสมาชิกที่ออนไลน์ของบทบาทที่กำหนด
    role_counts = {nickname: 0 for nickname in selected_roles.values()}

    for member in guild.members:
        if member.status != discord.Status.offline:
            for role in member.roles:
                if role.name in selected_roles:  # ตรวจสอบว่าชื่อเต็มของบทบาทอยู่ใน dictionary หรือไม่
                    nickname = selected_roles[role.name]  # ใช้ชื่อเล่นแทนชื่อเต็ม
                    role_counts[nickname] += 1

    # อัปเดตชื่อห้องทั้ง 5 ห้องตามบทบาทที่กำหนด
    for i, channel_id in enumerate(channel_ids):
        channel = guild.get_channel(channel_id)
        if channel:
            role_nicknames = list(selected_roles.values())
            role_name = role_nicknames[i] if i < len(role_nicknames) else "ไม่มีข้อมูล"
            count = role_counts.get(role_name, 0)
            new_name = f"{role_name}Online『{count}』"
            await channel.edit(name=new_name)

bot.run("MTM0ODM1MzY5NTI1NDgzOTM0Nw.G2ngo1.xVtPdVN-HNAN5brmY8xJkxlNKXCMoaMlP153k0")
