import paramiko

def run_command_on_vps(host, username, password, command):
    try:
        # Connect to VPS
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)

        # Run command on VPS
        stdin, stdout, stderr = client.exec_command(command)
        
        # Print command output
        print(f"Output from {host}:")
        print(stdout.read().decode())

    except Exception as e:
        print(f"Error connecting to {host}: {e}")
    
    finally:
        client.close()

# Replace with your VPS details
vps1_host = '45.58.45.202'
vps1_username = 'root'
vps1_password = 'N2vXsbMcAh3Dd6Cx'

vps2_host = 'VPS2_IP_ADDRESS'
vps2_username = 'YOUR_USERNAME'
vps2_password = 'YOUR_PASSWORD'

# Replace with the command you want to run on both VPS instances
command_to_run = 'ls -l'

# Run the command on both VPS instances
run_command_on_vps(vps1_host, vps1_username, vps1_password, command_to_run)
run_command_on_vps(vps2_host, vps2_username, vps2_password, command_to_run)
