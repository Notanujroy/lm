import paramiko
from telethon.sync import TelegramClient
from telethon import events

# SSH connection details
hostname = '45.58.45.202'
port = 22
username = 'root'
password = 'N2vXsbMcAh3Dd6Cx'  # Replace with your actual password

# Telegram bot token
telegram_bot_token = '6336844692:AAF4O08Vu4bj-bF26HXla7xL_fCpvrWg_Oo'

# Allowed Telegram user IDs
allow_user = {2092103173, 7226255252}

# Create an SSH client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the server
client.connect(hostname, port, username, password)

# Define the Telethon client
telethon_client = TelegramClient('ssh_bot', api_id='26931099', api_hash='065c347bfa40c8923faf2650cd934198')

# Define the command handler for executing commands
@telethon_client.on(events.NewMessage(pattern='/execute'))
async def execute_command(event):
    user_id = event.message.sender_id

    if user_id not in allow_user:
        await event.respond('You are not allowed to execute commands.')
        return

    command = event.message.text[9:]  # Removing the '/execute ' prefix

    try:
        # Execute the command on the server
        stdin, stdout, stderr = client.exec_command(command)
        response = stdout.read().decode()
        await event.respond(f"Command output:\n{response}")

    except Exception as e:
        await event.respond(f"An error occurred: {str(e)}")

# Start the Telethon client
telethon_client.start()

# Run the client until Ctrl+C is pressed
telethon_client.run_until_disconnected()

# Close the SSH connection
client.close()
