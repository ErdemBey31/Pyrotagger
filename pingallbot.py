
from pyrogram import Client, filters
from pyrogram.types import Message
import os
import asyncio
from pyrogram import enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait

teletips=Client(
    "PingAllBot",
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
    bot_token = os.environ["BOT_TOKEN"]
)

chatQueue = []

stopProcess = False

@teletips.on_message(filters.command(["ping","all"]))
async def everyone(client, message):
  global stopProcess
  try: 
    try:
      sender = await teletips.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      if len(chatQueue) > 5:
        await message.reply("⛔️ | Şu anda maksimum 5 sohbetim üzerinde çalışıyorum. Lütfen kısa süre sonra tekrar deneyin.")
      else:  
        if message.chat.id in chatQueue:
          await message.reply("🚫 | Bu sohbette zaten devam eden bir süreç var. Yeni bir tane başlatmak için lütfen /stop.")
        else:  
          chatQueue.append(message.chat.id)
          if len(message.command) > 1:
            inputText = message.command[1]
          elif len(message.command) == 1:
            inputText = ""    
          membersList = []
          async for member in teletips.get_chat_members(message.chat.id):
            if member.user.is_bot == True:
              pass
            elif member.user.is_deleted == True:
              pass
            else:
              membersList.append(member.user)
          i = 0
          lenMembersList = len(membersList)
          if stopProcess: stopProcess = False
          while len(membersList) > 0 and not stopProcess :
            j = 0
            text1 = f"{inputText}\n\n"
            try:    
              while j < 10:
                user = membersList.pop(0)
                if user.username == None:
                  text1 += f"{user.mention} "
                  j+=1
                else:
                  text1 += f"@{user.username} "
                  j+=1
              try:     
                await teletips.send_message(message.chat.id, text1)
              except Exception:
                pass  
              await asyncio.sleep(10) 
              i+=10
            except IndexError:
              try:
                await teletips.send_message(message.chat.id, text1)  
              except Exception:
                pass  
              i = i+j
          if i == lenMembersList:    
            await message.reply(f"✅ | Başarıyla bahsedildi **toplam {i} üye sayısı**.\n❌ | Botlar ve silinen hesaplar reddedildi.") 
          else:
            await message.reply(f"✅ | **{i} üyeden başarıyla bahsedildi.**\n❌ | Botlar ve silinen hesaplar reddedildi."    
          chatQueue.remove(message.chat.id)
    else:
      await message.reply("👮🏻 | Sorry, **only admins** can execute this command.")  
  except FloodWait as e:
    await asyncio.sleep(e.value) 

@teletips.on_message(filters.command(["remove","clean"]))
async def remove(client, message):
  global stopProcess
  try: 
    try:
      sender = await teletips.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      bot = await teletips.get_chat_member(message.chat.id, "self")
      if bot.status == ChatMemberStatus.MEMBER:
        await message.reply("🕹 | Silinen hesapları kaldırmak için yönetici izinlerine ihtiyacım var.")  
      else:  
        if len(chatQueue) > 5 :
          await message.reply("⛔️ | Şu anda maksimum 5 sohbetim üzerinde çalışıyorum. Lütfen kısa süre sonra tekrar deneyin.")
        else:  
          if message.chat.id in chatQueue:
            await message.reply("🚫 | Bu sohbette zaten devam eden bir süreç var. Yeni bir tane başlatmak için lütfen /stop")
          else:  
            chatQueue.append(message.chat.id)  
            deletedList = []
            async for member in teletips.get_chat_members(message.chat.id):
              if member.user.is_deleted == True:
                deletedList.append(member.user)
              else:
                pass
            lenDeletedList = len(deletedList)  
            if lenDeletedList == 0:
              await message.reply("👻 | Bu sohbette silinmiş hesap yok.")
              chatQueue.remove(message.chat.id)
            else:
              k = 0
              processTime = lenDeletedList*10
              temp = await teletips.send_message(message.chat.id, f"🚨 | Toplam {lenDeletedList} silinmiş hesap tespit edildi.\n⏳ | Tahmini süre: {processTime} saniye sonra.")
              if stopProcess: stopProcess = False
              while len(deletedList) > 0 and not stopProcess:   
                deletedAccount = deletedList.pop(0)
                try:
                  await teletips.ban_chat_member(message.chat.id, deletedAccount.id)
                except Exception:
                  pass  
                k+=1
                await asyncio.sleep(10)
              if k == lenDeletedList:  
                await message.reply(f"✅ | Silinen tüm hesaplar bu sohbetten başarıyla kaldırıldı.")  
                await temp.delete()
              else:
                await message.reply(f"✅ | {k} silinmiş hesap bu sohbetten başarıyla kaldırıldı.")  
                await temp.delete()  
              chatQueue.remove(message.chat.id)
    else:
      await message.reply("👮🏻 | Üzgünüz, **yalnızca yöneticiler** bu komutu çalıştırabilir.")  
  except FloodWait as e:
    await asyncio.sleep(e.value)                               
        
@teletips.on_message(filters.command(["stop","cancel"]))
async def stop(client, message):
  global stopProcess
  try:
    try:
      sender = await teletips.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      if not message.chat.id in chatQueue:
        await message.reply("🤷🏻‍♀️ | Durdurulacak devam eden bir süreç yok.")
      else:
        stopProcess = True
        await message.reply("🛑 | Durdu.")
    else:
      await message.reply("👮🏻 | Üzgünüz, **yalnızca yöneticiler** bu komutu çalıştırabilir.")
  except FloodWait as e:
    await asyncio.sleep(e.value)

@teletips.on_message(filters.command(["admins","staff"]))
async def admins(client, message):
  try: 
    adminList = []
    ownerList = []
    async for admin in teletips.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
      if admin.privileges.is_anonymous == False:
        if admin.user.is_bot == True:
          pass
        elif admin.status == ChatMemberStatus.OWNER:
          ownerList.append(admin.user)
        else:  
          adminList.append(admin.user)
      else:
        pass   
    lenAdminList= len(ownerList) + len(adminList)  
    text2 = f"**GROUP STAFF - {message.chat.title}**\n\n"
    try:
      owner = ownerList[0]
      if owner.username == None:
        text2 += f"👑 Sahip\n└ {owner.mention}\n\n👮🏻 Admins\n"
      else:
        text2 += f"👑 Sahip\n└ @{owner.username}\n\n👮🏻 Admins\n"
    except:
      text2 += f"👑 Sahip\n└ <i>Hidden</i>\n\n👮🏻 Admins\n"
    if len(adminList) == 0:
      text2 += "└ <i>Yöneticiler gizlendi</i>"  
      await teletips.send_message(message.chat.id, text2)   
    else:  
      while len(adminList) > 1:
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"├ {admin.mention}\n"
        else:
          text2 += f"├ @{admin.username}\n"    
      else:    
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"└ {admin.mention}\n\n"
        else:
          text2 += f"└ @{admin.username}\n\n"
      text2 += f"✅ | **Toplam yönetici sayısı**: {lenAdminList}\n❌ | Botlar ve gizli yöneticiler reddedildi."  
      await teletips.send_message(message.chat.id, text2)           
  except FloodWait as e:
    await asyncio.sleep(e.value)       

@teletips.on_message(filters.command("bots"))
async def bots(client, message):  
  try:    
    botList = []
    async for bot in teletips.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BOTS):
      botList.append(bot.user)
    lenBotList = len(botList) 
    text3  = f"**BOT LİSTESİ - {message.chat.title}**\n\n🤖 Botlar\n"
    while len(botList) > 1:
      bot = botList.pop(0)
      text3 += f"├ @{bot.username}\n"    
    else:    
      bot = botList.pop(0)
      text3 += f"└ @{bot.username}\n\n"
      text3 += f"✅ | **Toplam bot sayısı**: {lenBotList}"  
      await teletips.send_message(message.chat.id, text3)
  except FloodWait as e:
    await asyncio.sleep(e.value)

@teletips.on_message(filters.command("start") & filters.private)
async def start(client, message):
  text = f'''
  Merhaba, {message.from_user.mention},
Adım **Pyro Tagger**. Sohbetinizde tüm üyelerden bahsederek herkesin dikkatini çekmenize yardımcı olmak için buradayım.

Bazı harika özelliklerim var ve ayrıca kanallarda çalışabiliyorum.

En son güncellemeler hakkında bilgi almak için [kanalıma](http://t.me/pyrotagger) katılmayı unutmayın.

Komutlarımı ve bunların kullanımını öğrenmek için /help tuşuna basın.
'''
  await teletips.send_message(message.chat.id, text, disable_web_page_preview=True)


@teletips.on_message(filters.command("help"))
async def help(client, message):
  text = '''
Hey, hadi komutlarıma hızlıca bir göz atalım.

**Komutlar**:
- /ping "giriş": <i>Tüm üyelerden bahsedin.</i>
- /remove: <i>Silinen tüm hesapları kaldırın.</i>
- /admins: <i>Tüm yöneticilerden bahsedin.</i>
- /bots: <i>Bot listesinin tamamını alın.</i>
- /stop: <i>Devam eden bir süreci durdurun.</i>

Beni nasıl kullanacağınızla ilgili sorularınız varsa [destek grubuma](https://t.me/pyrotaggerchat) sormaya çekinmeyin. 
'''
  await teletips.send_message(message.chat.id, text, disable_web_page_preview=True)

print("PingAll yaşıyor!")  
teletips.run()
 
#Copyright ©️ 2023 TeLe TiPs. All Rights Reserved 
