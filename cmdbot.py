import asyncio
from telethon.sync import TelegramClient, events

api_id = '26931099'
api_hash = '065c347bfa40c8923faf2650cd934198'
bot_token = '6336844692:AAF4O08Vu4bj-bF26HXla7xL_fCpvrWg_Oo'
allowed_users = [2092103173, 765669282]

running_process = None

async def execute_command(command, event):
    global running_process

    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    running_process = process

    while process.returncode is None:
        stdout, stderr = await process.communicate()
        response = stdout.decode() if process.returncode == 0 else stderr.decode()
        await event.respond(response)
        await asyncio.sleep(1)

    stdout, stderr = await process.communicate()
    response = stdout.decode() if process.returncode == 0 else stderr.decode()
    await event.respond(response)

    running_process = None

client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern=r'#exe (.+)', chats=allowed_users))
async def handle_command(event):
    command = event.pattern_match.group(1)
    await execute_command(command, event)

@client.on(events.NewMessage(pattern=r'#stop', chats=allowed_users))
async def stop_command(event):
    global running_process

    if running_process:
        running_process.terminate()
        await event.respond('Command stopped.')
        remaining_output, _ = await running_process.communicate()
        await event.respond(remaining_output.decode())
        running_process = None
    else:
        await event.respond('No command is currently running.')

client.run_until_disconnected()