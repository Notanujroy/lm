import paramiko
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

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

# Define the command handler for the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Send me commands, and I will execute them on the server.')

# Define the command handler for executing commands
def execute_command(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if user_id not in allow_user:
        update.message.reply_text('You are not allowed to execute commands.')
        return

    command = update.message.text[8:]  # Removing the '/execute ' prefix
    try:
        # Connect to the server
        client.connect(hostname, port, username, password)
        
        # Execute the command on the server
        stdin, stdout, stderr = client.exec_command(command)
        response = stdout.read().decode()
        update.message.reply_text(f"Command output:\n{response}")

    except Exception as e:
        update.message.reply_text(f"An error occurred: {str(e)}")

    finally:
        # Close the SSH connection
        client.close()

# Define the main function
def main() -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater(telegram_bot_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register the command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("execute", execute_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
