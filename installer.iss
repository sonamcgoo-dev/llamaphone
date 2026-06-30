; LlamaPhone Installer Script for Inno Setup
; ==========================================
; Download Inno Setup from: https://jrsoftware.org/isinfo.php
; Compile this script with Inno Setup Compiler
;
; To add an icon:
; 1. Create an icon file (icon.ico)
; 2. Place it in the assets folder
; 3. Uncomment the SetupIconFile line below

#define MyAppName "LlamaPhone"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "LlamaPhone"
#define MyAppURL "https://github.com/sonamcgoo-dev/llamaphone"
#define MyAppExeName "LlamaPhone.exe"

[Setup]
; Basic Info
AppId={{A8B9C7D6-E5F4-1234-5678-9ABCDEF01234}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; Output settings
OutputDir=installer
OutputBaseFilename=LlamaPhone_Setup_{#MyAppVersion}
; Compression
Compression=lzma2
SolidCompression=yes
; Visual
WizardStyle=modern
; SetupIconFile=assets\icon.ico  ; Uncomment after adding icon file
; Privileges
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog
; Architecture
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Main executable (from PyInstaller dist folder)
Source: "dist\LlamaPhone\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; Qt6 DLLs and dependencies
Source: "dist\LlamaPhone\*.dll"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Python DLLs
Source: "dist\LlamaPhone\*.pyd"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Data files
Source: "dist\LlamaPhone\data\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs createallsubdirs; Check: DirExists(ExpandConstant('{src}\dist\LlamaPhone\data'))
; Assets
Source: "dist\LlamaPhone\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs; Check: DirExists(ExpandConstant('{src}\dist\LlamaPhone\assets'))

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function DirExists(DirName: String): Boolean;
begin
  Result := DirExists(DirName);
end;

procedure InitializeWizard();
begin
  // Custom initialization if needed
end;
