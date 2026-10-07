param([string]$VaultPath = (Split-Path -Parent (Split-Path -Parent $PSScriptRoot)))
$ErrorActionPreference = 'Stop'
$taskInstallFolder = Join-Path (Split-Path -Parent $VaultPath) 'Garden-tools/ObsidianTaskLauncher'
[IO.Directory]::CreateDirectory($taskInstallFolder) | Out-Null
$taskCompiler = Join-Path $env:WINDIR 'Microsoft.NET/Framework64/v4.0.30319/csc.exe'
$taskExecutable = Join-Path $taskInstallFolder 'ObsidianTaskLauncher.exe'
& $taskCompiler /nologo /target:winexe /optimize+ "/out:$taskExecutable" /reference:System.Windows.Forms.dll /reference:System.Drawing.dll /reference:System.Web.Extensions.dll (Join-Path $PSScriptRoot 'ObsidianTaskLauncher.cs')
if ($LASTEXITCODE -ne 0) { throw 'Compilation failed' }
$taskUtf8 = New-Object Text.UTF8Encoding($false)
[IO.File]::WriteAllText((Join-Path $taskInstallFolder 'vault-path.txt'), [IO.Path]::GetFullPath($VaultPath), $taskUtf8)
$taskShortcutPath = Join-Path ([Environment]::GetFolderPath('Programs')) 'task - Obsidian タスク追加.lnk'
$taskShell = New-Object -ComObject WScript.Shell
$taskShortcut = $taskShell.CreateShortcut($taskShortcutPath)
$taskShortcut.TargetPath = $taskExecutable
$taskShortcut.Arguments = ''
$taskShortcut.WorkingDirectory = $VaultPath
$taskShortcut.Description = '今日のデイリーノートへタスクを追加'
$taskShortcut.Save()
$taskLegacyShortcutPath = Join-Path ([Environment]::GetFolderPath('Programs')) 'Obsidian タスク追加.lnk'
if (Test-Path -LiteralPath $taskLegacyShortcutPath) {
    $taskLegacyShortcut = $taskShell.CreateShortcut($taskLegacyShortcutPath)
    $taskLegacyShortcut.TargetPath = $taskExecutable
    $taskLegacyShortcut.Arguments = ''
    $taskLegacyShortcut.Save()
}
$taskCmdPalData = Join-Path $env:LOCALAPPDATA 'Packages/Microsoft.CommandPalette_8wekyb3d8bbwe/LocalState'
$taskBookmarkPath = Join-Path $taskCmdPalData 'bookmarks.json'
if (Test-Path -LiteralPath $taskBookmarkPath) {
    $taskBookmarkConfig = Get-Content -LiteralPath $taskBookmarkPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $taskBookmarkBackup = Join-Path $taskInstallFolder ('bookmarks-before-' + (Get-Date).ToString('yyyyMMdd-HHmmss') + '.json')
    Copy-Item -LiteralPath $taskBookmarkPath -Destination $taskBookmarkBackup
    $taskPreviousExecutable = Join-Path $env:LOCALAPPDATA 'GardenTools/ObsidianTaskLauncher/ObsidianTaskLauncher.exe'
    $taskOwnBookmark = @($taskBookmarkConfig.Data | Where-Object { $_.Bookmark -eq $taskExecutable -or $_.Bookmark -eq $taskPreviousExecutable })
    if ($taskOwnBookmark.Count -eq 0) {
        $taskOwnBookmark = @([pscustomobject]@{
            Id = [Guid]::NewGuid().ToString()
            Name = 'task'
            Bookmark = $taskExecutable
        })
        $taskBookmarkConfig.Data = @($taskBookmarkConfig.Data) + $taskOwnBookmark
    }
    foreach ($taskEntry in $taskOwnBookmark) {
        $taskEntry.Name = 'task'
        $taskEntry.Bookmark = $taskExecutable
    }
    [IO.File]::WriteAllText($taskBookmarkPath, ($taskBookmarkConfig | ConvertTo-Json -Depth 20), $taskUtf8)
    $taskSettingsPath = Join-Path $taskCmdPalData 'settings.json'
    if (Test-Path -LiteralPath $taskSettingsPath) {
        $taskSettings = Get-Content -LiteralPath $taskSettingsPath -Raw -Encoding UTF8 | ConvertFrom-Json
        $taskCommandId = 'Bookmarks.Launch.' + $taskOwnBookmark[0].Id
        if (-not $taskSettings.Aliases) {
            $taskSettings | Add-Member -NotePropertyName Aliases -NotePropertyValue ([pscustomobject]@{}) -Force
        }
        $taskExistingAlias = $taskSettings.Aliases.PSObject.Properties['task']
        if ($taskExistingAlias -and $taskExistingAlias.Value.CommandId -ne $taskCommandId) {
            throw 'The task alias is already assigned to another command. The bookmark is installed; configure its alias in Command Palette settings.'
        }
        $taskSettingsBackup = Join-Path $taskInstallFolder ('settings-before-task-alias-' + (Get-Date).ToString('yyyyMMdd-HHmmss') + '.json')
        Copy-Item -LiteralPath $taskSettingsPath -Destination $taskSettingsBackup
        foreach ($taskAliasEntry in @($taskSettings.Aliases.PSObject.Properties)) {
            if ($taskAliasEntry.Value.CommandId -eq $taskCommandId -and $taskAliasEntry.Value.Alias -eq 'task') {
                $taskSettings.Aliases.PSObject.Properties.Remove($taskAliasEntry.Name)
            }
        }
        $taskSettings.Aliases | Add-Member -NotePropertyName task -NotePropertyValue ([pscustomobject]@{
            CommandId = $taskCommandId
            Alias = 'task'
            IsDirect = $true
        }) -Force
        [IO.File]::WriteAllText($taskSettingsPath, ($taskSettings | ConvertTo-Json -Depth 50), $taskUtf8)
    }
}
Write-Output $taskExecutable
Write-Output $taskShortcutPath
