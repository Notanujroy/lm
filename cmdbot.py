import asyncio
import os
from telethon.sync import TelegramClient, events

# Replace these values with your own
api_id = '26931099'
api_hash = '065c347bfa40c8923faf2650cd934198'
bot_token = '6336844692:AAF4O08Vu4bj-bF26HXla7xL_fCpvrWg_Oo'
allowed_users = [2092103173, 765669282]

# Variable to store the running process and current working directory
running_process = None
current_directory = os.getcwd()

# Function to execute commands asynchronously and send partial responses
async def execute_command(command, event):
    global running_process, current_directory

    # Change the directory if the command starts with '#cd'
    if command.startswith('#cd '):
        new_directory = command.split(' ', 1)[1]
        os.chdir(new_directory)
        current_directory = os.getcwd()
        await event.respond(f'Changed directory to: {current_directory}')
        return

    print(f'Executing command in directory: {current_directory}')  # Debugging line
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=current_directory  # Set the current working directory for the subprocess
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
@client.on(events.NewMessage(pattern=r'#exe (.+)', chats=allowed_users))
async def handle_command(event):
    command = event.pattern_match.group(1)
    await execute_command(command, event)

# Start the event loop
client.run_until_disconnected()