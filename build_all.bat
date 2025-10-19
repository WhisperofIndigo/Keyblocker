@echo off
chcp 65001 >nul
echo ========================================
echo KeyboardBlocker Complete Build Script
echo Author: Whisper of Indigo
echo Version: 1.2.1
echo ========================================
echo.

REM Проверяем наличие Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

REM Проверяем наличие PyInstaller
pip show pyinstaller >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Удаляем старые файлы сборки
echo Cleaning old builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

REM Создаем папку dist
if not exist dist mkdir dist

REM ==========================================
REM СБОРКА UpdateHelper.exe
REM ==========================================
echo.
echo ========================================
echo Building UpdateHelper.exe...
echo ========================================

pyinstaller --onefile ^
            --console ^
            --uac-admin ^
            --name="UpdateHelper" ^
            --distpath="dist" ^
            --workpath="build/updater" ^
            --clean ^
            UpdateHelper.py

if not exist dist\UpdateHelper.exe (
    echo ERROR: Failed to build UpdateHelper.exe!
    pause
    exit /b 1
)
echo UpdateHelper.exe built successfully!

REM ==========================================
REM СБОРКА KeyboardBlocker.exe
REM ==========================================
echo.
echo ========================================
echo Building KeyboardBlocker.exe...
echo ========================================

REM Создаем файл версии
echo Creating version file...
(
echo VSVersionInfo^(
echo   ffi=FixedFileInfo^(
echo     filevers=^(1, 2, 0, 0^),
echo     prodvers=^(1, 2, 0, 0^),
echo     mask=0x3f,
echo     flags=0x0,
echo     OS=0x40004,
echo     fileType=0x1,
echo     subtype=0x0,
echo     date=^(0, 0^)
echo   ^),
echo   kids=[
echo     StringFileInfo^(
echo       [
echo       StringTable^(
echo         u'040904B0',
echo         [StringStruct^(u'CompanyName', u'Whisper of Indigo'^),
echo         StringStruct^(u'FileDescription', u'Keyboard Blocker - Block keyboard with hotkey'^),
echo         StringStruct^(u'FileVersion', u'1.2.1.0'^),
echo         StringStruct^(u'InternalName', u'KeyboardBlocker'^),
echo         StringStruct^(u'LegalCopyright', u'© 2025 Whisper of Indigo'^),
echo         StringStruct^(u'OriginalFilename', u'KeyboardBlocker.exe'^),
echo         StringStruct^(u'ProductName', u'Keyboard Blocker'^),
echo         StringStruct^(u'ProductVersion', u'1.2.1.0'^)]^)
echo       ]^), 
echo     VarFileInfo^([VarStruct^(u'Translation', [1033, 1200]^)]^)
echo   ]
echo ^)
) > version_info.txt

REM Создаем иконку если её нет
if not exist icon.ico (
    echo WARNING: icon.ico not found!
    echo Creating default icon...
    python -c "from PIL import Image, ImageDraw; img = Image.new('RGB', (64, 64), 'blue'); draw = ImageDraw.Draw(img); draw.ellipse([8, 8, 56, 56], fill='white'); img.save('icon.ico')"
)

REM Собираем exe
pyinstaller --noconsole ^
            --onefile ^
            --uac-admin ^
            --icon=icon.ico ^
            --name="KeyboardBlocker" ^
            --version-file=version_info.txt ^
            --distpath="dist" ^
            --workpath="build/main" ^
            --clean ^
            keyboard_blocker.py

if not exist dist\KeyboardBlocker.exe (
    echo ERROR: Failed to build KeyboardBlocker.exe!
    pause
    exit /b 1
)
echo KeyboardBlocker.exe built successfully!

REM Удаляем временные файлы
if exist version_info.txt del version_info.txt

REM ==========================================
REM СБОРКА SETUP с Inno Setup
REM ==========================================
echo.
echo ========================================
echo Building Installer with Inno Setup...
echo ========================================

REM Проверяем наличие Inno Setup
set INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
if not exist "%INNO_PATH%" (
    set INNO_PATH=C:\Program Files\Inno Setup 6\ISCC.exe
)

if not exist "%INNO_PATH%" (
    echo WARNING: Inno Setup not found!
    echo Please install Inno Setup 6 from https://jrsoftware.org/isdl.php
    echo.
    echo Build files are in dist\ folder
    echo You can compile the installer manually using KeyboardBlockerSetup.iss
    goto :done
)

REM Компилируем установщик
"%INNO_PATH%" KeyboardBlockerSetup.iss

if exist Output\KeyboardBlockerSetup.exe (
    echo.
    echo Installer built successfully!
    echo Location: Output\KeyboardBlockerSetup.exe
) else (
    echo WARNING: Installer build may have failed
    echo Check for errors above
)

:done
echo.
echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo.
echo Files created:
echo   - dist\KeyboardBlocker.exe
echo   - dist\UpdateHelper.exe
if exist Output\KeyboardBlockerSetup.exe (
    echo   - Output\KeyboardBlockerSetup.exe
)
echo.
echo ========================================
echo Author: Whisper of Indigo
echo ========================================
echo.
pause