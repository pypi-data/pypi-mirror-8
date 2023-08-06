#define PyDir "{app}\python-2.7.6"
#define ScriptDir "{app}\python-2.7.6\Scripts"

[Setup]
AppId={{55D6EC72-D14D-4A19-AE26-EECC1A6EF1EA}
AppName=Photini
AppVerName=Photini
AppPublisher=Jim Easterbrook
AppPublisherURL=https://github.com/jim-easterbrook/Photini
DefaultDirName={pf}\Photini
DefaultGroupName=Photini
AllowNoIcons=yes
OutputBaseFilename=photini-win32-setup
OutputDir=installers
Compression=lzma
SolidCompression=yes
LicenseFile=..\..\LICENSE.txt
InfoBeforeFile=info.txt
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\icon.ico
ExtraDiskSpaceRequired=7221248
SignTool=normal

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "WinPython\python-2.7.6\*"; DestDir: "{#PyDir}"; Excludes: "*.pyc,appdirs*,gdata*,photini*,Lib\test,gnome\share,PyQt4\doc,PyQt4\examples,PyQt4\sip,PyQt4\qsci,\Doc,\include,\Logs,\share,\tcl,\Tools"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Photini"; Filename: "{#PyDir}\pythonw.exe"; Parameters: "-m photini.editor"; Comment: "Photo metadata editor"; IconFileName: {app}\icon.ico
Name: "{group}\Photini documentation"; Filename: "http://jim-easterbrook.github.io/Photini/doc/html/"
Name: "{group}\upgrade Photini"; Filename: "{#ScriptDir}\pip.exe"; Parameters: "install -U photini"
Name: "{commondesktop}\Photini"; Filename: "{#PyDir}\pythonw.exe"; Parameters: "-m photini.editor"; Comment: "Photo metadata editor"; IconFileName: {app}\icon.ico; Tasks: desktopicon

[Run]
Filename: "{#ScriptDir}\pip.exe"; Parameters: "install appdirs gdata photini"; StatusMsg: "Installing PyPI packages..."
Filename: "{#PyDir}\pythonw.exe"; Parameters: "-m photini.editor"; Description: "{cm:LaunchProgram,Photini}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{#PyDir}"
