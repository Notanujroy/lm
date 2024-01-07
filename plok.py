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

# Create an SSH client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the server
client.connect(hostname, port, username, password)

# Maintain command session state for each user
user_sessions = {}

# Define the Telethon client
telethon_client = TelegramClient('ssh_bot', api_id='26931099', api_hash='065c347bfa40c8923faf2650cd934198')

# Define the command handler for executing commands
@telethon_client.on(events.NewMessage(pattern='/cmd'))
async def execute_command(event):
    user_id = event.message.sender_id
    command = event.message.text[5:]

    try:
        print(f"Received command from user {user_id}: {command}")

        # Get or create a session for the user
        user_directory = user_sessions.get(user_id, '/')

        # Execute the command on the server
        compound_command = f'cd {user_directory} && {command}'
        stdin, stdout, stderr = client.exec_command(compound_command)
        response = stdout.read().decode()

        if stderr:
            response += "\nError Output:\n" + stderr.read().decode()

        # Update user session directory
        user_sessions[user_id] = user_directory

        log_message = f"Command executed successfully. Output:\n{response}"
        print(log_message)
        await event.respond(log_message)

    except Exception as e:
        error_message = f"An error occurred while executing the command: {str(e)}"
        print(error_message)
        await event.respond(error_message)

# Start the Telethon client
telethon_client.start()

# Run the client until Ctrl+C is pressed
telethon_client.run_until_disconnected()

# Close the SSH connection
client.close()
