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

# Maintain command session state for each user
user_sessions = {}

# Define the Telethon client
telethon_client = TelegramClient('ssh_bot', api_id='26931099', api_hash='065c347bfa40c8923faf2650cd934198')

# Define the command handler for executing commands
@telethon_client.on(events.NewMessage(pattern='/execute'))
async def execute_command(event):
    global user_sessions

    user_id = event.message.sender_id

    if user_id not in allow_user:
        await event.respond('You are not allowed to execute commands.')
        return

    command = event.message.text[9:]  # Removing the '/execute ' prefix

    try:
        # Get or create a session for the user
        session = user_sessions.get(user_id, {'current_directory': '/'})
        
        # Execute the command on the server
        user_directory = session['current_directory']
        compound_command = f'bash -c "cd {user_directory} && {command}"'
        stdin, stdout, stderr = client.exec_command(compound_command)
        response = stdout.read().decode()

        if stderr:
            response += "\nError Output:\n" + stderr.read().decode()

        # Update the session state
        user_sessions[user_id] = {'current_directory': user_directory}

        await event.respond(f"Command output:\n{response}")

    except Exception as e:
        await event.respond(f"An error occurred: {str(e)}")

# Start the Telethon client
telethon_client.start()

# Run the client until Ctrl+C is pressed
telethon_client.run_until_disconnected()

# Close the SSH connection
client.close()
