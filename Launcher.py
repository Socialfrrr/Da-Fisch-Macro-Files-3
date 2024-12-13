import os
import subprocess
import logging
import requests
import sys
import ctypes
import tempfile

def install_requirements():
    temp_req = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
    requirements = '''
requests
'''.strip()
    temp_req.write(requirements.encode())
    temp_req.close()
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', temp_req.name])
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install requirements: {e}")
    finally:
        os.unlink(temp_req.name)

def create_elevated_script():
    temp = tempfile.NamedTemporaryFile(delete=False, suffix='.vbs')
    script = '''
Set Shell = CreateObject("Shell.Application")
Set File = CreateObject("Scripting.FileSystemObject")
command = "cmd /c " & WScript.Arguments(0)
Shell.ShellExecute "cmd.exe", "/c " & command, "", "runas", 0
    '''
    temp.write(script.encode())
    temp.close()
    return temp.name

def main():
    print("Made by Social")
    
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    
    logging.debug("Installing requirements...")
    install_requirements()
    
    url = "https://github.com/AutoHotkey/AutoHotkey/releases/download/v1.1.37.02/AutoHotkey_1.1.37.02_setup.exe"
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads", "AutoHotkey_Setup.exe")
    logging.debug("Downloading AutoHotkey...")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(downloads_path, 'wb') as file:
            file.write(response.content)
        logging.debug("Download complete")
        
        logging.debug("Launching AutoHotkey installer...")
        elevation_script = create_elevated_script()
        subprocess.run(['cscript.exe', elevation_script, downloads_path])
        os.unlink(elevation_script)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        
        while True:
            response = input("Did you finish the AutoHotkey setup? (yes/no): ").lower()
            if response == 'yes':
                break
            elif response == 'no':
                print("Please complete the setup before continuing...")
            else:
                print("Please answer 'yes' or 'no'")
        
        macro_url = "https://raw.githubusercontent.com/Socialfrrr/Da-Fisch-Macro-Files-3/main/Fisch%20Macro.ahk"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        macro_path = os.path.join(current_dir, "Fisch Macro.ahk")
        
        logging.debug("Downloading Fisch Macro...")
        response = requests.get(macro_url, timeout=30)
        response.raise_for_status()
        
        with open(macro_path, 'wb') as file:
            file.write(response.content)
        
        ahk_path = r"C:\Program Files\AutoHotkey\AutoHotkey.exe"
        subprocess.Popen([ahk_path, macro_path])
        logging.debug("Macro launched successfully")
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Download failed: {e}")
        input("Failed to download required files. Press any key to exit...")
        return
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        input("Press any key to exit...")
        return

if __name__ == "__main__":
    main()
