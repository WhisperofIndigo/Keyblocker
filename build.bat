@echo off
echo ========================================
echo KeyboardBlocker Build Script with Signing
echo Author: Whisper of Indigo
echo ========================================
echo.

REM Удаляем старые файлы сборки
echo Cleaning old builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

REM Создаем файл версии
echo Creating version file...
(
echo VSVersionInfo^(
echo   ffi=FixedFileInfo^(
echo     filevers=^(1, 0, 0, 0^),
echo     prodvers=^(1, 0, 0, 0^),
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
echo         StringStruct^(u'FileVersion', u'1.0.0.0'^),
echo         StringStruct^(u'InternalName', u'KeyboardBlocker'^),
echo         StringStruct^(u'LegalCopyright', u'© 2024 Whisper of Indigo'^),
echo         StringStruct^(u'OriginalFilename', u'KeyboardBlocker.exe'^),
echo         StringStruct^(u'ProductName', u'Keyboard Blocker'^),
echo         StringStruct^(u'ProductVersion', u'1.0.0.0'^)]^)
echo       ]^), 
echo     VarFileInfo^([VarStruct^(u'Translation', [1033, 1200]^)]^)
echo   ]
echo ^)
) > version_info.txt

REM Создаем иконку если её нет
if not exist icon.ico (
    echo Creating icon...
    python create_icon.py
)

REM Собираем exe
echo.
echo Building executable...
pyinstaller --noconsole ^
            --onefile ^
            --uac-admin ^
            --icon=icon.ico ^
            --name="KeyboardBlocker" ^
            --version-file=version_info.txt ^
            --distpath="dist" ^
            --workpath="build" ^
            --clean ^
            keyboard_blocker.py

if exist dist\KeyboardBlocker.exe (
    echo.
    echo Build successful!
    
    REM Подписываем если есть сертификат
    if exist WhisperOfIndigo.pfx (
        echo.
        echo Signing executable...
        signtool sign /f WhisperOfIndigo.pfx /p YourPassword123 ^
                      /t http://timestamp.digicert.com ^
                      /d "Keyboard Blocker" ^
                      /du "https://github.com/whisperofindigo" ^
                      dist\KeyboardBlocker.exe
        
        if %ERRORLEVEL% == 0 (
            echo Signing successful!
        ) else (
            echo Signing failed, but exe is created
        )
    )
    
    echo.
    echo ========================================
    echo Build complete!
    echo Output: dist\KeyboardBlocker.exe
    echo Author: Whisper of Indigo
    echo ========================================
) else (
    echo.
    echo ========================================
    echo Build failed!
    echo ========================================
)

REM Удаляем временные файлы
if exist version_info.txt del version_info.txt

echo.
pause
