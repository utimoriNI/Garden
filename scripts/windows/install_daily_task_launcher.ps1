param([string]$VaultPath = (Split-Path -Parent (Split-Path -Parent $PSScriptRoot)))
$ErrorActionPreference = 'Stop'
$taskInstallFolder = Join-Path $env:LOCALAPPDATA 'GardenTools/ObsidianTaskLauncher'
[IO.Directory]::CreateDirectory($taskInstallFolder) | Out-Null
$taskCompiler = Join-Path $env:WINDIR 'Microsoft.NET/Framework64/v4.0.30319/csc.exe'
$taskExecutable = Join-Path $taskInstallFolder 'ObsidianTaskLauncher.exe'
& $taskCompiler /nologo /target:winexe /optimize+ "/out:$taskExecutable" /reference:System.Windows.Forms.dll /reference:System.Drawing.dll /reference:System.Web.Extensions.dll (Join-Path $PSScriptRoot 'ObsidianTaskLauncher.cs')
if ($LASTEXITCODE -ne 0) { throw 'Compilation failed' }
$taskUtf8 = New-Object Text.UTF8Encoding($false)
[IO.File]::WriteAllText((Join-Path $taskInstallFolder 'vault-path.txt'), [IO.Path]::GetFullPath($VaultPath), $taskUtf8)
$taskShortcutPath = Join-Path ([Environment]::GetFolderPath('Programs')) 'Obsidian タスク追加.lnk'
$taskShell = New-Object -ComObject WScript.Shell
$taskShortcut = $taskShell.CreateShortcut($taskShortcutPath)
$taskShortcut.TargetPath = $taskExecutable
$taskShortcut.Arguments = ''
$taskShortcut.WorkingDirectory = $VaultPath
$taskShortcut.Description = '今日のデイリーノートへタスクを追加'
$taskShortcut.Save()
Write-Output $taskExecutable
Write-Output $taskShortcutPath
