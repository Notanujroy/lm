###################################################
import os
import asyncio
from telethon.sync import TelegramClient, events, functions
from telethon.sessions import StringSession
from datetime import datetime
from Config import ACC_STRMAIN, API_ID, API_HASH
from telethon.tl.functions.messages import SendReactionRequest, SetTypingRequest
from telethon.tl.types import SendMessageGamePlayAction
from telethon.errors import ChatAdminRequiredError, PeerIdInvalidError, UserDeletedError
from telethon import types
from itertools import cycle
###################################################
account_id = None
user_reactions = {}
auto_reaction_data = {}
typing_tasks = {}
client_global = None
###################################################
async def send_typing_message(client, peer):
    try:
        await client(SetTypingRequest(peer=peer, action=SendMessageGamePlayAction()))
    except ChatAdminRequiredError:
        print("Error: Admin privileges required - Skipping chat")
    except PeerIdInvalidError:
        print("Error: Invalid peer - Skipping chat")
    except UserDeletedError:
        print("Error: User deleted - Skipping chat")
    except Exception as e:
        print(f"Error sending typing message: {e}")

async def typing_task(client, chat_id):
    while True:
        try:
            await send_typing_message(client, chat_id)
        except (ChatAdminRequiredError, PeerIdInvalidError, UserDeletedError) as specific_error:
            print(f"Error: {specific_error} - Stopping typing in chat {chat_id}")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

async def initialize_account_id(client):
    global account_id
    try:
        account_id = (await client.get_me()).id
    except Exception as e:
        print(f"Error getting account ID: {e}")
        return

async def start_userbot():
    async with TelegramClient(StringSession(ACC_STRMAIN), API_ID, API_HASH) as client:
        print("Userbot has started.")
        await initialize_account_id(client)

###################################################
        @client.on(events.NewMessage(pattern=r"#alive"))
        async def alive_command(event):
            try:
                if event.sender_id == account_id:
                    start = datetime.now()
                    end = datetime.now()
                    ms = (end - start).microseconds / 1000
                    await event.edit(f"🤖 I Aᴍ Aʟɪᴠᴇ !!!!\nPɪɴɢ : `{ms}` 𝗺𝘀")
            except Exception as e:
                print(f"Error handling alive command: {e}")
                
################################################### 
        @client.on(events.NewMessage(pattern=r"#cp"))
        async def copy_message(event):
            try:
                if event.sender_id == account_id and event.is_reply:
                    original_message = await event.get_reply_message()
                    if original_message:
                        await event.edit(f"```{original_message.text}```")
            except Exception as e:
                print(f"Error handling #cp command: {e}")
                
###################################################
        @client.on(events.NewMessage(pattern=r"#react (.+)"))
        async def react_message(event):
            try:
                if event.sender_id == account_id and event.is_reply:
                    original_message = await event.get_reply_message()
                    if original_message:
                        emoji = event.pattern_match.group(1)
                        await client(SendReactionRequest(
                            peer=await event.get_input_chat(),
                            msg_id=original_message.id,
                            reaction=[types.ReactionEmoji(emoticon=emoji)]
                        ))
                    else:
                        await event.reply("Rᴇᴘʟʏ Tᴏ Mᴇꜱꜱᴀɢᴇ")
            except Exception as exc:
                print(f"Error: {exc}")
                
###################################################
        @client.on(events.NewMessage(pattern=r"#areact (.+)"))
        async def enable_auto_reaction(event):
            global auto_reaction_data
            if event.sender_id == account_id and event.is_reply:
                replied_to_message = await event.get_reply_message()
                user_entity = await event.client.get_entity(replied_to_message.sender_id)
                user_name = f"{user_entity.first_name} {user_entity.last_name}" if user_entity.last_name else user_entity.first_name
                user_to_enable = replied_to_message.sender_id
                emoji = event.pattern_match.group(1)
                auto_reaction_data[user_to_enable] = emoji
                await event.edit(f"Aᴜᴛᴏ-Rᴇᴀᴄᴛɪᴏɴ Eɴᴀʙʟᴇᴅ Fᴏʀ {user_name}")

###################################################
        @client.on(events.NewMessage(pattern=r"#sreact"))
        async def disable_auto_reaction(event):
            global auto_reaction_data
            if event.sender_id == account_id and event.is_reply:
                replied_to_message = await event.get_reply_message()
                user_to_disable = replied_to_message.sender_id
                user_entity = await event.client.get_entity(replied_to_message.sender_id)
                user_name = f"{user_entity.first_name} {user_entity.last_name}" if user_entity.last_name else user_entity.first_name
                if user_to_disable in auto_reaction_data:
                    del auto_reaction_data[user_to_disable]
                    await event.edit(f"Aᴜᴛᴏ-Rᴇᴀᴄᴛɪᴏɴ Dɪꜱᴀʙʟᴇᴅ Fᴏʀ {user_name}")

        @client.on(events.NewMessage(incoming=True))
        async def auto_react_to_messages(event):
            global auto_reaction_data
            user_id = event.sender_id
            if user_id in auto_reaction_data:
                emoji = auto_reaction_data[user_id]
                try:
                    await client(SendReactionRequest(
                        peer=await event.get_input_chat(),
                        msg_id=event.id,
                        reaction=[types.ReactionEmoji(emoticon=emoji)]
                    ))
                except Exception as exc:
                    await event.reply(f"Error: {exc}")

###################################################
        @client.on(events.NewMessage(pattern=r"#creact"))
        async def continuous_reaction(event):
            try:
                if event.sender_id == account_id and event.is_reply:
                    original_message = await event.get_reply_message()
                    if original_message:
                        reactions = cycle(["👍", "🔥", "❤️️","🥰","💯"])
                        for reaction in reactions:
                            try:
                                await client(SendReactionRequest(
                                    peer=await event.get_input_chat(),
                                    msg_id=original_message.id,
                                    reaction=[types.ReactionEmoji(emoticon=reaction)]
                                ))
                            except Exception as e:
                                print(f"Error giving reaction {reaction}: {e}")
                                continue
                            await asyncio.sleep(8) ##fukada u can change this
            except Exception as e:
                print(f"Error handling #creact command: {e}")

        @client.on(events.NewMessage(pattern=r"#stopcreact"))
        async def stop_continuous_reaction(event):
            if event.sender_id == account_id and event.is_reply:
                replied_to_message = await event.get_reply_message()
                if replied_to_message:
                    original_user_id = replied_to_message.from_id.user_id if replied_to_message.from_id else None
                    if original_user_id in auto_reaction_data:
                        del auto_reaction_data[original_user_id]
                        await event.edit(f"Cᴏɴᴛɪɴᴜᴏᴜꜱ Rᴇᴀᴄᴛɪᴏɴ Dɪꜱᴀʙʟᴇᴅ Fᴏʀ {original_user_id}")
                    else:
                        await event.edit("Cᴏɴᴛɪɴᴜᴏᴜꜱ Rᴇᴀᴄᴛɪᴏɴ ɴᴏᴛ ꜰᴏᴜɴᴅ")
                else:
                    await event.edit("Rᴇᴘʟʏ Tᴏ Mᴇꜱꜱᴀɢᴇ")

###################################################
        @client.on(events.NewMessage(pattern=r"#playing"))
        async def start_typing(event):
            bot_id = (await client.get_me()).id
            if event.sender_id == bot_id:
                chat_id = event.chat_id
                if chat_id not in typing_tasks:
                    typing_tasks[chat_id] = asyncio.ensure_future(typing_task(client, chat_id))
                    await event.edit("Pʟᴀʏɪɴɢ Sᴛᴀᴛᴜꜱ Aᴄᴛɪᴠᴀᴛᴇᴅ")

###################################################
        @client.on(events.NewMessage(pattern=r"#splaying"))
        async def stop_typing(event):
            bot_id = (await client.get_me()).id
            if event.sender_id == bot_id:
                chat_id = event.chat_id
                if chat_id in typing_tasks:
                    typing_tasks[chat_id].cancel()
                    del typing_tasks[chat_id]
                    await event.edit("Pʟᴀʏɪɴɢ Sᴛᴀᴛᴜꜱ Dᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ")

###################################################
        @client.on(events.NewMessage(pattern=r"#count"))
        async def count_command(event):
            try:
                if event.sender_id == account_id:
                    start = datetime.now()
                    u = 0  # number of users
                    g = 0  # number of basic groups
                    c = 0  # number of super groups
                    bc = 0  # number of channels
                    b = 0   # number of bots
                    await event.edit("Retrieving Telegram Count(s)")
                    async for d in client.iter_dialogs(limit=None):
                        if d.is_user:
                            if d.entity.bot:
                                b += 1
                            else:
                                u += 1
                        elif d.is_channel:
                            if d.entity.broadcast:
                                bc += 1
                            else:
                                c += 1
                        elif d.is_group:
                            g += 1
                        else:
                            print(d.stringify())
                    end = datetime.now()
                    ms = (end - start).seconds
                    await event.edit("""┏━━━━━━━━━━━━━━
┣Tᴏᴏᴋ "{}" Sᴇᴄᴏɴᴅs.
┣Uꜱᴇʀꜱ :\t{}
┣Gʀᴏᴜᴘꜱ :\t{}
┣Sᴜᴘᴇʀ Gʀᴏᴜᴘꜱ :\t{}
┣Cʜᴀɴɴᴇʟs :\t{}
┣Bᴏᴛꜱ :\t{}
┗━━━━━━━━━━━━━━""".format(ms, u, g, c, bc, b))
            except Exception as e:
                print(f"Error handling count command: {e}")

###################################################
        @client.on(events.NewMessage(pattern=r"#usernames", outgoing=True))
        async def list_usernames(event):
            try:
                if event.sender_id == account_id:
                    result = await client(functions.channels.GetAdminedPublicChannelsRequest())
                    output_str = ""
                    for channel_obj in result.chats:
                        output_str += f"- {channel_obj.title} @{channel_obj.username} \n"
                    await event.edit(output_str)
            except Exception as e:
                print(f"Error handling listmyusernames command: {e}")

###################################################
        @client.on(events.NewMessage(pattern=r"#tagall"))
        async def tag_all(event):
            if event.fwd_from:
                return

            mentions = "@tagall"
            chat = await event.get_input_chat()

            async for participant in client.iter_participants(chat, 1000):
                mentions += f"[\u2063](tg://user?id={participant.id})"

            await event.reply(mentions)
            await event.delete()

###################################################
        @client.on(events.NewMessage(pattern=r"#exe"))
        async def execute_command(event):
            user_id = event.sender_id
            if user_id == (await client.get_me()).id:
                command = event.raw_text.split(" ", 1)[1].strip()
                try:
                    result = os.popen(command).read()
                    message = f"Command executed successfully:\n{result}"
                except Exception as e:
                    message = f"Error executing the command: {str(e)}"
                await event.reply(message)
                
###################################################
        await client.run_until_disconnected()
loop = asyncio.get_event_loop()
loop.run_until_complete(start_userbot())
###################################################