; Inno Setup script for SpectrogramViz (Windows)
; Build:  ISCC.exe installer\installer.iss
; Output: installer\Output\SpectrogramViz-Setup-<ver>.exe

#define MyAppName "Spectrogram Viz"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "Billy G Soundgarden"
#define MyAppExeName "SpectrogramViz.exe"
#define MyAppURL "https://github.com/albazzaztariq/Billy-G-Sound-Garden"

[Setup]
AppId={{B17A4D7E-2C1A-4F8B-9BC6-30E2F5DE1A77}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\SpectrogramViz
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=Output
OutputBaseFilename=SpectrogramViz-Setup-{#MyAppVersion}
SetupIconFile=..\assets\guitar.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\dist\SpectrogramViz\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\_internal\assets\guitar.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\_internal\assets\guitar.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
