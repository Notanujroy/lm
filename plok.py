import paramiko

# SSH connection details
hostname = '45.58.45.202'
port = 22
username = 'root'
password = 'N2vXsbMcAh3Dd6Cx'  # Replace with your actual password

# Create an SSH client
client = paramiko.SSHClient()

# Automatically add the server's host key (this is insecure and should be used only for testing)
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect to the server
    client.connect(hostname, port, username, password)

    # Execute commands (replace these with your own commands)
    stdin, stdout, stderr = client.exec_command('ls')
    print(stdout.read().decode())

finally:
    # Close the SSH connection
    client.close()
