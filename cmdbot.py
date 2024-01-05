import asyncio
from telethon.sync import TelegramClient, events

# Replace these values with your own
api_id = '26931099'
api_hash = '065c347bfa40c8923faf2650cd934198'
bot_token = '6336844692:AAF4O08Vu4bj-bF26HXla7xL_fCpvrWg_Oo'
allowed_users = [2092103173, 765669282]

# Variable to store the running process
running_process = None

# Function to execute commands asynchronously and send partial responses
async def execute_command(command, event):
    global running_process

    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    running_process = process  # Store the process globally

    while process.returncode is None:
        stdout, stderr = await process.communicate()
        response = stdout.decode() if process.returncode == 0 else stderr.decode()
        await event.respond(response)
        await asyncio.sleep(1)

    # Send the final response
    stdout, stderr = await process.communicate()
    response = stdout.decode() if process.returncode == 0 else stderr.decode()
    await event.respond(response)

    running_process = None  # Reset the global variable after command completes

# Initialize the Telegram client
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# Event handler for incoming messages
@client.on(events.NewMessage(pattern=r'#(.+)', chats=allowed_users))
async def handle_command(event):
    command = event.pattern_match.group(1)
    await execute_command(command, event)

# Event handler to stop the ongoing command
@client.on(events.NewMessage(pattern=r'#stop', chats=allowed_users))
async def stop_command(event):
    global running_process

    if running_process:
        running_process.terminate()  # Terminate the running process
        await event.respond('Command stopped.')
        # Fetch and send the remaining output of the command
        remaining_output, _ = await running_process.communicate()
        await event.respond(remaining_output.decode())
        running_process = None  # Reset the global variable after command completes
    else:
        await event.respond('No command is currently running.')

# Start the event loop
client.run_until_disconnected()