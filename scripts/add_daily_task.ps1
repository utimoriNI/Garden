param(
    [string]$TaskText,
    [string]$VaultPath = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'
$interactive = -not $PSBoundParameters.ContainsKey('TaskText')
if ($interactive) {
    Add-Type -AssemblyName Microsoft.VisualBasic
    $TaskText = [Microsoft.VisualBasic.Interaction]::InputBox(
        'タスクの本文を入力してください。Enterで追加、キャンセルで終了します。',
        'Obsidian タスク追加', '')
}
if ([string]::IsNullOrWhiteSpace($TaskText)) { return }

try {
    if ($TaskText -match '[\r\n]') { throw 'タスクは1行で入力してください。' }
    $vaultRoot = [IO.Path]::GetFullPath($VaultPath).TrimEnd('\', '/')
    $settings = Get-Content -LiteralPath (Join-Path $vaultRoot '.obsidian/daily-notes.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($settings.format -and $settings.format -ne 'YYYY-MM-DD') {
        throw 'このランチャーはYYYY-MM-DD形式のデイリーノートに対応しています。'
    }
    $day = Get-Date
    $label = $day.ToString('yyyy-MM-dd')
    $folder = [IO.Path]::GetFullPath((Join-Path $vaultRoot $settings.folder))
    if (-not $folder.StartsWith($vaultRoot + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw 'デイリーノートの保存先がVaultの外になっています。'
    }
    $path = Join-Path $folder ($label + '.md')
    $encoding = New-Object Text.UTF8Encoding($false)
    $seed = ''
    if (-not (Test-Path -LiteralPath $path)) {
        if ($settings.template) {
            $templatePath = Join-Path $vaultRoot $settings.template
            if (-not [IO.Path]::GetExtension($templatePath)) { $templatePath += '.md' }
            $seed = [IO.File]::ReadAllText($templatePath, $encoding)
            # Render the date expressions used by Garden's current Daily template.
            $seed = $seed.Replace('<% tp.date.now("YYYY-MM-DD", -1, tp.file.title, "YYYY-MM-DD") %>', $day.AddDays(-1).ToString('yyyy-MM-dd'))
            $seed = $seed.Replace('<% tp.date.now("YYYY-MM-DD", 1, tp.file.title, "YYYY-MM-DD") %>', $day.AddDays(1).ToString('yyyy-MM-dd'))
            $seed = $seed.Replace('{{date}}', $label).Replace('{{time}}', $day.ToString('HH:mm')).Replace('{{title}}', $label)
            if ($seed.Contains('<%') -or $seed -match '\{\{.+?\}\}') {
                throw '未対応のテンプレート記法があります。Obsidianで今日のノートを先に作成してください。'
            }
        }
    }
    [IO.Directory]::CreateDirectory($folder) | Out-Null
    $line = '- [ ] #' + [char]::ConvertFromUtf32(0x1F4CE) + 'Task ' + $TaskText.Trim()
    # Append in place, preserving all existing bytes. Lock while writing.
    $stream = $null
    for ($attempt = 0; $attempt -lt 10; $attempt++) {
        try {
            $stream = [IO.File]::Open($path, [IO.FileMode]::OpenOrCreate, [IO.FileAccess]::ReadWrite, [IO.FileShare]::Read)
            break
        } catch [IO.IOException] {
            if ($attempt -eq 9) { throw }
            Start-Sleep -Milliseconds 100
        }
    }
    try {
        if ($stream.Length -eq 0 -and $seed) {
            $bytes = $encoding.GetBytes($seed.TrimEnd([char[]]"`r`n") + "`r`n")
            $stream.Write($bytes, 0, $bytes.Length)
        }
        $separator = ''
        if ($stream.Length -gt 0) {
            $stream.Seek(-1, [IO.SeekOrigin]::End) | Out-Null
            if ($stream.ReadByte() -ne 10) { $separator = "`r`n" }
        }
        $stream.Seek(0, [IO.SeekOrigin]::End) | Out-Null
        $bytes = $encoding.GetBytes($separator + $line + "`r`n")
        $stream.Write($bytes, 0, $bytes.Length)
        $stream.Flush()
    } finally { if ($stream) { $stream.Dispose() } }
    Write-Output $path
} catch {
    if ($interactive) {
        Add-Type -AssemblyName System.Windows.Forms
        [Windows.Forms.MessageBox]::Show($_.Exception.Message, 'タスクを追加できませんでした') | Out-Null
    } else { throw }
    exit 1
}
