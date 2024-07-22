import os
import subprocess

# Define paths
source_file = '/home/swieyeinthesky/bluehillproject/test.csv'  # The source file path
repo_directory = '/home/swieyeinthesky/bluehillproject'  # Path to the cloned repository

# Check if the source file exists
if not os.path.isfile(source_file):
    print(f"Source file '{source_file}' does not exist.")
else:
    # Define the git commands to be executed
    commands = [
        ['git', 'status'],  # Check the current status of the repository
        ['git', 'add', '-A'],  # Ensure all changes are staged
        ['git', 'status'],  # Check the status again after staging changes
        ['git', 'commit', '-m', 'Add or update test.csv'],
        ['git', 'push', 'origin', 'main']  # Replace 'main' with your branch name if different
    ]

    # Execute each git command
    for command in commands:
        result = subprocess.run(command, cwd=repo_directory, capture_output=True, text=True)
        print(f"Running command: {' '.join(command)}")
        print(f"Output: {result.stdout}")
        if result.returncode != 0:
            print(f"Error running command {' '.join(command)}: {result.stderr}")
            break
        else:
            print(f"Successfully ran command: {' '.join(command)}")
