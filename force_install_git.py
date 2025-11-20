import urllib.request
import subprocess
import os
import sys
import time

def install_git():
    url = "https://github.com/git-for-windows/git/releases/download/v2.52.0.windows.1/Git-2.52.0-64-bit.exe"
    installer_name = "git_installer.exe"
    
    print(f"Downloading Git from {url}...")
    try:
        urllib.request.urlretrieve(url, installer_name)
        print("Download complete.")
    except Exception as e:
        print(f"Failed to download: {e}")
        return

    print("Installing Git (Silent Mode)...")
    try:
        # Run the installer silently
        # /VERYSILENT: No windows
        # /NORESTART: Do not restart
        subprocess.run([installer_name, "/VERYSILENT", "/NORESTART"], check=True)
        print("Installation command executed.")
    except subprocess.CalledProcessError as e:
        print(f"Installation failed: {e}")
        return

    # Clean up installer
    if os.path.exists(installer_name):
        try:
            os.remove(installer_name)
            print("Installer removed.")
        except:
            pass

    print("Verifying installation...")
    
    # Check if git is in PATH (might not be updated yet for this process)
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"Success! {result.stdout.strip()}")
            return
    except:
        pass
        
    # Check default install location if PATH check fails
    default_git_path = r"C:\Program Files\Git\cmd\git.exe"
    if os.path.exists(default_git_path):
        print(f"Git found at {default_git_path}")
        print("Note: You may need to restart your terminal or computer for 'git' command to work globally.")
        
        # Try running it directly
        try:
            result = subprocess.run([default_git_path, "--version"], capture_output=True, text=True)
            print(f"Version: {result.stdout.strip()}")
        except Exception as e:
            print(f"Could not run git from absolute path: {e}")
    else:
        print("Git installation could not be verified. Please check manually.")

if __name__ == "__main__":
    install_git()
