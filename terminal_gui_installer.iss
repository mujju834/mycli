[Setup]
AppName=Mujju Command Terminal
AppVersion=1.0
DefaultDirName={pf}\MujuuCommandTerminal
DefaultGroupName=MujjuCommandTerminal
OutputBaseFilename=MujjuCommandTerminalInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\terminal_gui.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Mujuu Command Terminal"; Filename: "{app}\terminal_gui.exe"
Name: "{group}\Uninstall Mujju Command Terminal"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\terminal_gui.exe"; Description: "Launch Mujju Command Terminal"; Flags: nowait postinstall
