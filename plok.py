import subprocess

def run_command_on_vps(host, command):
    try:
        # Prompt user for credentials
        username = ("itsmerood")
        password = ("@Qwerty123@Rood")

        # Construct SSH command
        ssh_command = f'sshpass -p {password} ssh {username}@{host} "{command}"'

        # Run command on VPS
        result = subprocess.run(ssh_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Print command output and potential errors
        print(f"Output from {host}:")
        print(result.stdout)
        print("Error (if any):")
        print(result.stderr)

    except Exception as e:
        print(f"Error connecting to {host}: {e}")

# Replace with your VPS details
vps_host = '20.167.49.217'

# Prompt user for the command to run
command_to_run = input("Enter the command to run on the VPS: ")

# Run the command on the VPS
run_command_on_vps(vps_host, command_to_run)