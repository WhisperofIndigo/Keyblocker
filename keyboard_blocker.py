import sys
import os
import threading
import ctypes
from ctypes import wintypes
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import time
import json
import requests
import subprocess
import tkinter as tk
from tkinter import messagebox

CURRENT_VERSION = "v1.2.0"

def check_for_updates():
    """Проверка обновлений на GitHub"""
    try:
        url = "https://api.github.com/repos/WhisperofIndigo/Keyblocker/releases/latest"
        response = requests.get(url, timeout=5)
        
        if response.status_code != 200:
            log_message(f"Update check failed: HTTP {response.status_code}")
            return
        
        data = response.json()
        latest_version = data.get("tag_name", "")
        release_url = data.get("html_url", "")
        
        # Ищем установщик
        installer_url = None
        for asset in data.get("assets", []):
            if asset["name"].endswith(".exe"):
                installer_url = asset["browser_download_url"]
                break
        
        if not installer_url:
            log_message("No installer found in latest release")
            return
        
        # Сравниваем версии
        if latest_version != CURRENT_VERSION:
            log_message(f"New version available: {latest_version} (current: {CURRENT_VERSION})")
            
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            message = (
                f"Доступна новая версия {latest_version}\n"
                f"Текущая версия: {CURRENT_VERSION}\n\n"
                f"Обновить сейчас?\n\n"
                f"Программа будет закрыта и запущен установщик."
            )
            
            result = messagebox.askyesno(
                "Доступно обновление",
                message,
                parent=root
            )
            
            if result:
                # Запускаем UpdateHelper
                updater_path = os.path.join(
                    os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__),
                    "UpdateHelper.exe"
                )
                
                if not os.path.exists(updater_path):
                    messagebox.showerror(
                        "Ошибка",
                        f"UpdateHelper.exe не найден:\n{updater_path}",
                        parent=root
                    )
                    root.destroy()
                    return
                
                try:
                    # Запускаем UpdateHelper с URL установщика
                    subprocess.Popen([updater_path, installer_url], shell=False)
                    log_message("Update helper launched, exiting...")
                    root.destroy()
                    
                    # Завершаем программу
                    if icon:
                        icon.stop()
                    os._exit(0)
                    
                except Exception as e:
                    messagebox.showerror(
                        "Ошибка",
                        f"Не удалось запустить обновление:\n{e}",
                        parent=root
                    )
            
            root.destroy()
        else:
            log_message(f"Already running latest version: {CURRENT_VERSION}")
            
    except requests.exceptions.RequestException as e:
        log_message(f"Network error checking for updates: {e}")
    except Exception as e:
        log_message(f"Error checking for updates: {e}")

def is_already_running():
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "Global\\KeyboardBlockerSingleInstance")
    last_error = ctypes.windll.kernel32.GetLastError()
    # Если код ошибки 183 — объект (mutex) уже существует → программа уже запущена
    if last_error == 183:
        ctypes.windll.user32.MessageBoxW(0, "Keyboard Blocker уже запущен.", "Keyboard Blocker", 0x40)
        sys.exit()

is_already_running()

# ===== СИСТЕМА ЛОКАЛИЗАЦИИ =====
class Localization:
    def __init__(self):
        self.current_lang = 'ru'  # Русский по умолчанию
        self.translations = {
            'ru': {
                'app_name': 'Keyboard Blocker',
                'status_active': 'Активно',
                'status_blocked': 'Заблокировано',
                'status_label': 'Статус',
                'toggle_block': 'Переключить блокировку',
                'clear_log': 'Очистить лог',
                'show_log': 'Показать лог',
                'language': 'Язык/Language',  # Специально на английском
                'exit': 'Выход',
                'keyboard_blocked': 'Клавиатура заблокирована',
                'keyboard_unblocked': 'Клавиатура разблокирована',
                'press_to_unlock': 'Нажмите Ctrl+Alt+B для разблокировки',
                'press_to_lock': 'Нажмите Ctrl+Alt+B для блокировки',
                'admin_required': 'Требуются права администратора',
                'admin_request': 'Программа требует права администратора.\nПожалуйста, подтвердите запрос на повышение прав.',
                'restarting_admin': 'Перезапускаем с правами администратора...',
                'launched_admin': '✓ Запущено с правами администратора',
                'use_hotkey': 'Используйте Ctrl+Alt+B для блокировки/разблокировки',
                'use_tray': 'Для выхода используйте меню в системном трее',
                'hook_installed': '✓ Хук клавиатуры успешно установлен',
                'hook_removed': 'Хук клавиатуры удален',
                'hook_error': '✗ Ошибка установки хука',
                'starting_loop': 'Запуск message loop...',
                'current_state': 'Текущее состояние блокировки',
                'program_closing': 'Завершение программы...',
                'log_cleared': 'Лог очищен',
                'log_clear_error': 'Ошибка при очистке лога',
                'hotkey_detected': 'Обнаружена комбинация Ctrl+Alt+B',
                'toggle_called': 'toggle_block вызван, is_blocked теперь',
                'icon_error': 'Ошибка при обновлении иконки',
                'notify_error': 'Ошибка при показе уведомления',
                'tray_starting': 'Запуск иконки в трее...',
                'tray_error': 'Ошибка в трее',
                'hook_exception': 'Ошибка в хуке',
                'loop_exception': 'Исключение в message loop',
                'loop_error': 'Ошибка в message loop',
                'loop_finished': 'Message loop завершен',
                'quit_received': 'Получен WM_QUIT',
                'critical_error': 'Критическая ошибка',
                'fatal_error': 'Фатальная ошибка',
                'error_title': 'Ошибка',
                'hook_install_error': 'Не удалось установить хук клавиатуры.\n\nПопробуйте:\n1. Перезагрузить компьютер\n2. Закрыть другие программы блокировки клавиатуры\n3. Добавить программу в исключения антивируса\n\nДетали ошибки сохранены в keyboard_blocker.log',
                'program_failed': '✗ Не удалось запустить программу',
                'user_terminated': 'Программа завершена пользователем',
                'installing_hook': 'Устанавливаем хук с h_instance',
                'initial_state': 'Начальное состояние is_blocked',
                'error_code': 'Не удалось установить хук. Код ошибки'
            },
            'en': {
                'app_name': 'Keyboard Blocker',
                'status_active': 'Active',
                'status_blocked': 'Blocked',
                'status_label': 'Status',
                'toggle_block': 'Toggle blocking',
                'clear_log': 'Clear log',
                'show_log': 'Show log',
                'language': 'Язык/Language',  # Специально на русском
                'exit': 'Exit',
                'keyboard_blocked': 'Keyboard blocked',
                'keyboard_unblocked': 'Keyboard unblocked',
                'press_to_unlock': 'Press Ctrl+Alt+B to unlock',
                'press_to_lock': 'Press Ctrl+Alt+B to lock',
                'admin_required': 'Administrator rights required',
                'admin_request': 'This program requires administrator rights.\nPlease confirm the elevation request.',
                'restarting_admin': 'Restarting with administrator rights...',
                'launched_admin': '✓ Launched with administrator rights',
                'use_hotkey': 'Use Ctrl+Alt+B to lock/unlock keyboard',
                'use_tray': 'Use tray menu to exit',
                'hook_installed': '✓ Keyboard hook successfully installed',
                'hook_removed': 'Keyboard hook removed',
                'hook_error': '✗ Hook installation error',
                'starting_loop': 'Starting message loop...',
                'current_state': 'Current blocking state',
                'program_closing': 'Closing program...',
                'log_cleared': 'Log cleared',
                'log_clear_error': 'Error clearing log',
                'hotkey_detected': 'Ctrl+Alt+B combination detected',
                'toggle_called': 'toggle_block called, is_blocked now',
                'icon_error': 'Error updating icon',
                'notify_error': 'Error showing notification',
                'tray_starting': 'Starting tray icon...',
                'tray_error': 'Tray error',
                'hook_exception': 'Hook error',
                'loop_exception': 'Message loop exception',
                'loop_error': 'Message loop error',
                'loop_finished': 'Message loop finished',
                'quit_received': 'WM_QUIT received',
                'critical_error': 'Critical error',
                'fatal_error': 'Fatal error',
                'error_title': 'Error',
                'hook_install_error': 'Failed to install keyboard hook.\n\nTry:\n1. Restart computer\n2. Close other keyboard blocking programs\n3. Add program to antivirus exceptions\n\nError details saved in keyboard_blocker.log',
                'program_failed': '✗ Failed to start program',
                'user_terminated': 'Program terminated by user',
                'installing_hook': 'Installing hook with h_instance',
                'initial_state': 'Initial is_blocked state',
                'error_code': 'Failed to install hook. Error code'
            }
        }
        self.load_settings()
    
    def get(self, key):
        """Получить перевод для текущего языка"""
        return self.translations[self.current_lang].get(key, key)
    
    def set_language(self, lang):
        """Установить язык"""
        if lang in self.translations:
            self.current_lang = lang
            self.save_settings()
            return True
        return False
    
    def save_settings(self):
        """Сохранить настройки языка"""
        settings_file = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "settings.json")
        try:
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump({'language': self.current_lang}, f)
        except:
            pass
    
    def load_settings(self):
        """Загрузить настройки языка"""
        settings_file = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "settings.json")
        try:
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.current_lang = settings.get('language', 'ru')
        except:
            pass

# Создаем глобальный объект локализации
loc = Localization()

# ===== ОСНОВНОЙ КОД =====

# Проверка прав администратора
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Запрос прав администратора
def run_as_admin():
    if is_admin():
        return True
    else:
        ctypes.windll.shell32.ShellExecuteW(
            None, 
            "runas", 
            sys.executable, 
            " ".join(sys.argv), 
            None, 
            1
        )
        return False

# Загружаем необходимые DLL
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# Правильно объявляем типы для функций Windows API
user32.SetWindowsHookExW.argtypes = [ctypes.c_int, ctypes.c_void_p, wintypes.HINSTANCE, wintypes.DWORD]
user32.SetWindowsHookExW.restype = wintypes.HHOOK

user32.CallNextHookEx.argtypes = [wintypes.HHOOK, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM]
user32.CallNextHookEx.restype = ctypes.c_int

user32.UnhookWindowsHookEx.argtypes = [wintypes.HHOOK]
user32.UnhookWindowsHookEx.restype = wintypes.BOOL

user32.GetMessageW.argtypes = [ctypes.POINTER(wintypes.MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT]
user32.GetMessageW.restype = wintypes.BOOL

user32.TranslateMessage.argtypes = [ctypes.POINTER(wintypes.MSG)]
user32.DispatchMessageW.argtypes = [ctypes.POINTER(wintypes.MSG)]

user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
user32.GetAsyncKeyState.restype = ctypes.c_short

kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
kernel32.GetModuleHandleW.restype = wintypes.HMODULE

is_blocked = False
icon = None
hook = None
stop_event = threading.Event()

# Константы Windows
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_SYSKEYDOWN = 0x0104
WM_SYSKEYUP = 0x0105
HC_ACTION = 0

VK_LCONTROL = 0xA2
VK_RCONTROL = 0xA3
VK_LMENU = 0xA4  # Left Alt
VK_RMENU = 0xA5  # Right Alt
VK_B = 0x42

class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", wintypes.DWORD),
        ("scanCode", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

def create_icon(color):
    """Создание иконки для трея"""
    image = Image.new('RGB', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Рисуем круг
    draw.ellipse([8, 8, 56, 56], fill=color, outline='white', width=2)
    
    # Рисуем символ клавиатуры
    if color == "red":
        # Замок для заблокированного состояния
        draw.rectangle([24, 28, 40, 36], fill='white')
        draw.arc([26, 20, 38, 32], 0, 180, fill='white', width=2)
    else:
        # Клавиши для разблокированного состояния
        for x in range(20, 45, 8):
            for y in range(25, 40, 7):
                draw.rectangle([x, y, x+5, y+4], fill='white')
    
    return image

def log_message(message):
    """Безопасный вывод сообщений"""
    try:
        print(message)
    except:
        pass
    
    # Всегда пишем в лог файл
    try:
        log_file = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "keyboard_blocker.log")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    except:
        pass

def keyboard_hook_proc(nCode, wParam, lParam):
    """Обработчик хука клавиатуры"""
    global is_blocked, hook
    
    # Если nCode меньше 0, мы должны передать вызов дальше
    if nCode < 0:
        return user32.CallNextHookEx(hook, nCode, wParam, lParam)
    
    if nCode == HC_ACTION:
        try:
            kb = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
            
            # Проверяем Ctrl+Alt+B для переключения блокировки
            if kb.vkCode == VK_B and (wParam == WM_KEYDOWN or wParam == WM_SYSKEYDOWN):
                ctrl = (user32.GetAsyncKeyState(VK_LCONTROL) & 0x8000) or \
                       (user32.GetAsyncKeyState(VK_RCONTROL) & 0x8000)
                alt = (user32.GetAsyncKeyState(VK_LMENU) & 0x8000) or \
                      (user32.GetAsyncKeyState(VK_RMENU) & 0x8000)
                
                if ctrl and alt:
                    log_message(loc.get('hotkey_detected'))
                    # Вызываем toggle_block в отдельном потоке
                    threading.Thread(target=toggle_block, daemon=True).start()
                    return 1  # Блокируем само нажатие B чтобы не печаталось
            
            # Если блокировка НЕ включена, пропускаем все клавиши
            if not is_blocked:
                return user32.CallNextHookEx(hook, nCode, wParam, lParam)
            
            # Если блокировка включена, обрабатываем клавиши
            if is_blocked:
                # Разрешаем Ctrl и Alt для возможности разблокировки
                if kb.vkCode in [VK_LCONTROL, VK_RCONTROL, VK_LMENU, VK_RMENU]:
                    return user32.CallNextHookEx(hook, nCode, wParam, lParam)
                
                # Для клавиши B проверяем, нажаты ли Ctrl+Alt
                if kb.vkCode == VK_B:
                    ctrl = (user32.GetAsyncKeyState(VK_LCONTROL) & 0x8000) or \
                           (user32.GetAsyncKeyState(VK_RCONTROL) & 0x8000)
                    alt = (user32.GetAsyncKeyState(VK_LMENU) & 0x8000) or \
                          (user32.GetAsyncKeyState(VK_RMENU) & 0x8000)
                    
                    if ctrl and alt:
                        # Разрешаем B если нажаты Ctrl+Alt
                        return user32.CallNextHookEx(hook, nCode, wParam, lParam)
                    else:
                        # Блокируем B если не нажаты Ctrl+Alt
                        return 1
                
                # Блокируем все остальные клавиши
                return 1
                
        except Exception as e:
            log_message(f"{loc.get('hook_exception')}: {e}")
            # При ошибке пропускаем клавишу
            try:
                return user32.CallNextHookEx(hook, nCode, wParam, lParam)
            except:
                return 0
    
    # По умолчанию передаем вызов дальше
    return user32.CallNextHookEx(hook, nCode, wParam, lParam)

# Создаем callback функцию как глобальную переменную
LowLevelKeyboardProc = ctypes.WINFUNCTYPE(
    ctypes.c_int,
    ctypes.c_int,
    wintypes.WPARAM,
    wintypes.LPARAM
)

# Сохраняем ссылку на callback
keyboard_hook_callback = LowLevelKeyboardProc(keyboard_hook_proc)

def toggle_block():
    """Переключение блокировки клавиатуры"""
    global is_blocked, icon
    
    is_blocked = not is_blocked
    
    log_message(f"{loc.get('toggle_called')}: {is_blocked}")
    
    if icon:
        try:
            if is_blocked:
                icon.icon = create_icon("red")
                icon.title = f"{loc.get('app_name')} - {loc.get('status_blocked').upper()}"
                show_notification(loc.get('keyboard_blocked'), loc.get('press_to_unlock'))
            else:
                icon.icon = create_icon("green")
                icon.title = f"{loc.get('app_name')} - {loc.get('status_active')}"
                show_notification(loc.get('keyboard_unblocked'), loc.get('press_to_lock'))
        except Exception as e:
            log_message(f"{loc.get('icon_error')}: {e}")
    
    log_message(loc.get('keyboard_blocked') if is_blocked else loc.get('keyboard_unblocked'))
    
    # Обновляем меню после изменения состояния
    update_tray_menu()

def show_notification(title, message):
    """Показать уведомление Windows"""
    try:
        if icon and icon.visible:
            icon.notify(message, title)
    except Exception as e:
        log_message(f"{loc.get('notify_error')}: {e}")

def show_error_message(title, message):
    """Показать сообщение об ошибке через Windows MessageBox"""
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)

def change_language(new_lang):
    """Изменить язык интерфейса"""
    global icon
    
    if loc.set_language(new_lang):
        log_message(f"Language changed to: {new_lang}")
        
        # Обновляем заголовок иконки
        if icon:
            status = loc.get('status_blocked') if is_blocked else loc.get('status_active')
            icon.title = f"{loc.get('app_name')} - {status}"
        
        # Обновляем меню
        update_tray_menu()
        
        # Показываем уведомление на новом языке
        if is_blocked:
            show_notification(loc.get('keyboard_blocked'), loc.get('press_to_unlock'))
        else:
            show_notification(loc.get('keyboard_unblocked'), loc.get('press_to_lock'))

def update_tray_menu():
    """Обновить меню в трее"""
    global icon
    if icon and icon.visible:
        try:
            icon.menu = create_menu()
        except:
            pass

def create_menu():
    """Создать меню для трея"""
    log_file = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "keyboard_blocker.log")
    status = loc.get('status_blocked') if is_blocked else loc.get('status_active')
    
    # Создаем подменю для выбора языка
    language_menu = pystray.Menu(
        item('🇷🇺 Русский', lambda: change_language('ru'), 
             checked=lambda item: loc.current_lang == 'ru'),
        item('🇬🇧 English', lambda: change_language('en'), 
             checked=lambda item: loc.current_lang == 'en')
    )
    
    return pystray.Menu(
        item(f"{loc.get('status_label')}: {status}", lambda: None, enabled=False),
        pystray.Menu.SEPARATOR,
        item(f"{loc.get('toggle_block')} (Ctrl+Alt+B)", lambda icon, item: toggle_block()),
        pystray.Menu.SEPARATOR,
        item(f"🌐 {loc.get('language')}", language_menu),
        pystray.Menu.SEPARATOR,
        item(loc.get('clear_log'), lambda icon, item: clear_log()),
        item(loc.get('show_log'), lambda icon, item: os.startfile(log_file) if os.path.exists(log_file) else None),
        pystray.Menu.SEPARATOR,
        item(loc.get('exit'), on_exit)
    )

def install_hook():
    """Установка хука клавиатуры"""
    global hook, is_blocked
    
    # Убеждаемся, что при запуске блокировка выключена
    is_blocked = False
    
    try:
        # Для exe файла используем None (будет преобразовано в NULL)
        h_instance = None
        if not getattr(sys, 'frozen', False):
            # Если это Python скрипт
            h_instance = kernel32.GetModuleHandleW(None)
        
        log_message(f"{loc.get('installing_hook')}: {h_instance}")
        log_message(f"{loc.get('initial_state')}: {is_blocked}")
        
        # Устанавливаем хук
        hook = user32.SetWindowsHookExW(
            WH_KEYBOARD_LL,
            keyboard_hook_callback,
            h_instance,
            0
        )
        
        if not hook:
            error = kernel32.GetLastError()
            raise Exception(f"{loc.get('error_code')}: {error}")
        
        log_message(loc.get('hook_installed'))
        return True
        
    except Exception as e:
        log_message(f"{loc.get('hook_error')}: {e}")
        return False

def uninstall_hook():
    """Удаление хука клавиатуры"""
    global hook
    if hook:
        result = user32.UnhookWindowsHookEx(hook)
        hook = None
        log_message(f"{loc.get('hook_removed')} (result: {result})")

def message_loop():
    """Главный цикл обработки сообщений Windows"""
    if not install_hook():
        return False
    
    msg = wintypes.MSG()
    try:
        log_message(loc.get('starting_loop'))
        log_message(f"{loc.get('current_state')}: {is_blocked}")
        
        while not stop_event.is_set():
            # Получаем сообщения
            bRet = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
            if bRet == 0:  # WM_QUIT
                log_message(loc.get('quit_received'))
                break
            elif bRet == -1:  # Error
                error = kernel32.GetLastError()
                log_message(f"{loc.get('loop_error')}: {error}")
                break
            else:
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
        
        log_message(loc.get('loop_finished'))
    except Exception as e:
        log_message(f"{loc.get('loop_exception')}: {e}")
    finally:
        uninstall_hook()
    
    return True

def on_exit(icon_obj, item):
    """Выход из программы"""
    global stop_event
    
    log_message(loc.get('program_closing'))
    stop_event.set()
    uninstall_hook()
    
    if icon_obj:
        icon_obj.stop()
    
    user32.PostQuitMessage(0)
    
    # Завершаем программу
    def force_exit():
        time.sleep(1)
        os._exit(0)
    
    threading.Thread(target=force_exit, daemon=True).start()

def run_tray():
    """Запуск иконки в трее"""
    global icon
    
    try:
        icon = pystray.Icon(
            "KeyBlocker",
            create_icon("green"),
            f"{loc.get('app_name')} - {loc.get('status_active')}",
            menu=create_menu()
        )
        
        # Обновление меню
        def update_menu_loop():
            while icon and icon.visible and not stop_event.is_set():
                try:
                    icon.menu = create_menu()
                except:
                    pass
                time.sleep(1)
        
        threading.Thread(target=update_menu_loop, daemon=True).start()
        
        log_message(loc.get('tray_starting'))
        icon.run()
    except Exception as e:
        log_message(f"{loc.get('tray_error')}: {e}")

def clear_log():
    """Очистить лог файл"""
    try:
        log_file = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "keyboard_blocker.log")
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {loc.get('log_cleared')}\n")
        log_message(loc.get('log_cleared'))
    except Exception as e:
        log_message(f"{loc.get('log_clear_error')}: {e}")

def main():
    """Главная функция"""
    global is_blocked
    
    #Убеждаемся, что при старте блокировка выключена
    is_blocked = False
    
    log_message("=" * 60)
    log_message(f"{loc.get('app_name')} {CURRENT_VERSION}")
    log_message("=" * 60)
    
    # Проверяем права администратора
    if not is_admin():
        log_message(f"⚠ {loc.get('admin_required')}")
        log_message(loc.get('restarting_admin'))
        
        show_error_message(
            loc.get('app_name'), 
            loc.get('admin_request')
        )
        
        if not run_as_admin():
            sys.exit(0)
        return
    
    log_message(loc.get('launched_admin'))
    check_for_updates()
    log_message(f"\n{loc.get('use_hotkey')}")
    log_message(loc.get('use_tray'))
    log_message("=" * 60)
    
    # Запускаем трей
    tray_thread = threading.Thread(target=run_tray, daemon=True)
    tray_thread.start()
    
    # Небольшая задержка для инициализации трея
    time.sleep(1)
    
    # Запускаем message loop
    try:
        if not message_loop():
            log_message(f"\n{loc.get('program_failed')}")
            
            show_error_message(
                f"{loc.get('app_name')} - {loc.get('error_title')}",
                loc.get('hook_install_error')
            )
            time.sleep(5)
    except KeyboardInterrupt:
        log_message(f"\n{loc.get('user_terminated')}")
    except Exception as e:
        log_message(f"\n✗ {loc.get('critical_error')}: {e}")
        show_error_message(f"{loc.get('app_name')} - {loc.get('critical_error')}", str(e))
        time.sleep(5)
    finally:
        if icon:
            icon.stop()
        stop_event.set()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_message(f"{loc.get('fatal_error')}: {e}")
        show_error_message(f"{loc.get('app_name')} - {loc.get('fatal_error')}", str(e))
