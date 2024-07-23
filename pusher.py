import subprocess

# Define repository details
local_repo_path = "/home/swieyeinthesky/bluehillproject/"  # Replace with the path to your cloned repo
github_repo_url = "https://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@github.com/HaydenWStone/bluehillproject.git"  # Replace with your GitHub repo URL and your token

# Define the branch you want to push to
branch = "main"

def run_command(command, cwd=None):
    result = subprocess.run(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        raise Exception(f"Command failed: {command}")
    return result.stdout

try:
    # Navigate to the local repository
    print("Navigating to the local repository...")
    run_command(f"cd {local_repo_path}")

    # Add all changes
    print("Adding all changes...")
    run_command("git add -A", cwd=local_repo_path)

    # Commit the changes
    print("Committing the changes...")
    run_command('git commit -m "Force push to overwrite GitHub repo"', cwd=local_repo_path)

    # Force push to the remote GitHub repository
    print("Force pushing to the remote repository...")
    run_command(f"git push --force {github_repo_url} {branch}", cwd=local_repo_path)

    print("Force push completed successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
