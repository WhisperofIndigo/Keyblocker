import os
import sys
import time
import requests
import subprocess
import ctypes
from ctypes import windll

def is_admin():
    """Проверка прав администратора"""
    try:
        return windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin(cmd):
    """Запуск от имени администратора"""
    try:
        windll.shell32.ShellExecuteW(None, "runas", cmd, None, None, 1)
        return True
    except:
        return False

def download_file(url, dest):
    """Скачивание файла с прогрессом"""
    print(f"Downloading from: {url}")
    try:
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            downloaded = 0
            
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"Progress: {percent:.1f}%", end='\r')
            print("\nDownload complete!")
            return True
    except Exception as e:
        print(f"Download error: {e}")
        return False

def kill_process(process_name):
    """Завершить процесс по имени"""
    try:
        subprocess.run(['taskkill', '/F', '/IM', process_name], 
                      capture_output=True, timeout=5)
        time.sleep(2)
        return True
    except:
        return False

def main():
    print("=" * 60)
    print("Keyboard Blocker Update Helper")
    print("=" * 60)
    
    # Проверка прав администратора
    if not is_admin():
        print("Requesting administrator rights...")
        if run_as_admin(sys.executable + " " + " ".join(sys.argv)):
            sys.exit(0)
        else:
            print("ERROR: Administrator rights required!")
            input("Press Enter to exit...")
            sys.exit(1)
    
    # Проверка аргументов
    if len(sys.argv) < 2:
        print("ERROR: Installer URL not provided!")
        input("Press Enter to exit...")
        sys.exit(1)
    
    installer_url = sys.argv[1]
    temp_path = os.path.join(os.getenv("TEMP"), "KeyboardBlocker_Update.exe")
    
    # Удаляем старый установщик если есть
    if os.path.exists(temp_path):
        try:
            os.remove(temp_path)
        except:
            pass
    
    # Закрываем основную программу
    print("\nClosing Keyboard Blocker...")
    kill_process("KeyboardBlocker.exe")
    
    # Скачиваем новую версию
    print("\nDownloading new version...")
    if not download_file(installer_url, temp_path):
        print("\nERROR: Failed to download update!")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Проверяем что файл скачался
    if not os.path.exists(temp_path) or os.path.getsize(temp_path) < 1000:
        print("\nERROR: Downloaded file is invalid!")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Запускаем установщик
    print("\nLaunching installer...")
    try:
        subprocess.Popen([temp_path, '/SILENT', '/CLOSEAPPLICATIONS'], 
                        shell=False)
        print("\nInstaller launched successfully!")
        print("The installer will complete the update.")
        time.sleep(2)
    except Exception as e:
        print(f"\nERROR launching installer: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        input("Press Enter to exit...")
        sys.exit(1)