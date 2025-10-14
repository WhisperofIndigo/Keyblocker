; ==============================
; Keyboard Blocker Setup Script
; Author: Whisper of Indigo
; ==============================

[Setup]
AppName=Keyboard Blocker
AppVersion=1.0.0
AppPublisher=Whisper of Indigo
AppPublisherURL=https://github.com/whisperofindigo
AppSupportURL=https://github.com/whisperofindigo
DefaultDirName={autopf}\Keyboard Blocker
DefaultGroupName=Keyboard Blocker
UninstallDisplayIcon={app}\KeyboardBlocker.exe
OutputBaseFilename=KeyboardBlockerSetup
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

; Языки
LanguageDetectionMethod=uilanguage

[Languages]
Name: "ru"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "en"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\KeyboardBlocker.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Keyboard Blocker"; Filename: "{app}\KeyboardBlocker.exe"; WorkingDir: "{app}"
Name: "{autodesktop}\Keyboard Blocker"; Filename: "{app}\KeyboardBlocker.exe"; WorkingDir: "{app}"

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

