; ==============================
; Keyboard Blocker Setup Script
; Author: Whisper of Indigo
; Version: 1.2.1
; ==============================

#define MyAppName "Keyboard Blocker"
#define MyAppVersion "1.2.1"
#define MyAppPublisher "Whisper of Indigo"
#define MyAppURL "https://github.com/whisperofindigo"
#define MyAppExeName "KeyboardBlocker.exe"

[Setup]
; Основные параметры
AppId={{8F9A7B2C-3D4E-5F6A-7B8C-9D0E1F2A3B4C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases

; Установка
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Вывод
OutputDir=Output
OutputBaseFilename=KeyboardBlockerSetup
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

; Сжатие
Compression=lzma2/max
SolidCompression=yes

; Интерфейс
WizardStyle=modern
WizardSizePercent=100,100

; Языки - теперь всегда показывается диалог выбора языка (если нужен всегда язык системы: ShowLanguageDialog=auto)
ShowLanguageDialog=yes

; Остановка процессов
CloseApplications=yes
CloseApplicationsFilter=*.exe

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "autostart"; Description: "Запускать при входе в систему / Run at system startup"; GroupDescription: "Дополнительные опции / Additional options:"; Flags: unchecked

[Files]
Source: "dist\KeyboardBlocker.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\UpdateHelper.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

; README (опционально, если есть)
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist

[Icons]
; Меню Пуск
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"
Name: "{group}\Удалить {#MyAppName}"; Filename: "{uninstallexe}"

; Рабочий стол
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon

; Панель быстрого запуска
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Registry]
; Автозапуск (опционально)
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "{#MyAppName}"; ValueData: """{app}\{#MyAppExeName}"""; Flags: uninsdeletevalue; Tasks: autostart

[Run]
; Запустить после установки
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent runascurrentuser shellexec

[UninstallDelete]
; Удаляем все файлы и папки при деинсталляции
Type: files; Name: "{app}\keyboard_blocker.log"
Type: files; Name: "{app}\settings.json"
Type: filesandordirs; Name: "{app}"

[Code]
// Проверка запущенных процессов перед установкой
function PrepareToInstall(var NeedsRestart: Boolean): String;
var
  ResultCode: Integer;
begin
  Result := '';
  
  // Пытаемся закрыть процесс
  if CheckForMutexes('Global\KeyboardBlockerSingleInstance') then
  begin
    // Процесс запущен, пытаемся закрыть
    Exec('taskkill', '/F /IM KeyboardBlocker.exe', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
    Sleep(1000);
    
    if CheckForMutexes('Global\KeyboardBlockerSingleInstance') then
    begin
      Result := 'Не удалось закрыть запущенную копию Keyboard Blocker. ' +
                'Пожалуйста, закройте программу вручную и повторите попытку.' + #13#10#13#10 +
                'Could not close running instance of Keyboard Blocker. ' +
                'Please close the program manually and try again.';
    end;
  end;
end;

// Удаление старых версий перед установкой
function InitializeSetup(): Boolean;
var
  UninstallString: String;
  ResultCode: Integer;
begin
  Result := True;
  
  // Проверяем наличие старой версии
  if RegQueryStringValue(HKLM, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{8F9A7B2C-3D4E-5F6A-7B8C-9D0E1F2A3B4C}_is1',
     'UninstallString', UninstallString) then
  begin
    if MsgBox('Обнаружена предыдущая версия Keyboard Blocker. Удалить её перед установкой?' + #13#10#13#10 +
              'Previous version of Keyboard Blocker detected. Uninstall it before installation?',
              mbConfirmation, MB_YESNO) = IDYES then
    begin
      // Запускаем деинсталлятор в тихом режиме
      Exec(RemoveQuotes(UninstallString), '/SILENT', '', SW_SHOW, ewWaitUntilTerminated, ResultCode);
      Sleep(1000);
    end;
  end;
end;

// Сообщение после успешной установки
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Можно добавить дополнительные действия после установки
  end;
end;

// Закрытие программы перед удалением
function InitializeUninstall(): Boolean;
var
  ResultCode: Integer;
  ErrorCode: Integer;
  RetryCount: Integer;
begin
  Result := True;
  RetryCount := 0;
  
  while (RetryCount < 3) do
  begin
    if CheckForMutexes('Global\KeyboardBlockerSingleInstance') then
    begin
      Exec('taskkill', '/F /IM KeyboardBlocker.exe', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
      Sleep(1500);
      
      if not CheckForMutexes('Global\KeyboardBlockerSingleInstance') then
        Exit;
      
      RetryCount := RetryCount + 1;
    end
    else
      Exit;
  end;
  
  if CheckForMutexes('Global\KeyboardBlockerSingleInstance') then
  begin
    ErrorCode := MsgBox(
      'Keyboard Blocker сейчас запущена. Пожалуйста, закройте программу вручную (из трея), затем нажмите OK.' + #13#10#13#10 +
      'Keyboard Blocker is currently running. Please close the program manually (from tray), after click OK.' + #13#10#13#10 +
      'Нажмите Cancel для отмены удаления / Click Cancel to abort uninstall.',
      mbError, MB_OKCANCEL);
    
    if ErrorCode = IDCANCEL then
    begin
      Result := False;
      Exit;
    end;
    
    Sleep(2000);
    
    if CheckForMutexes('Global\KeyboardBlockerSingleInstance') then
    begin
      MsgBox(
        'Программа все еще запущена. Деинсталляция отменена.' + #13#10#13#10 +
        'The program is still running. Uninstall cancelled.',
        mbError, MB_OK);
      Result := False;
    end;
  end;
end;

// Очистка оставшихся файлов
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  AppDir: String;
  ResultCode: Integer;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    AppDir := ExpandConstant('{app}');
    Exec('cmd.exe', '/c timeout /t 2 && rd /s /q "' + AppDir + '"', '', SW_HIDE, ewNoWait, ResultCode);
  end;
end;

[CustomMessages]
russian.LaunchProgram=Запустить %1
english.LaunchProgram=Launch %1