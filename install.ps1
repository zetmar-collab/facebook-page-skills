# Installs the fb-* skills into ~/.claude/skills and the state templates into
# ~/.claude/facebook (existing files are never overwritten).
$ErrorActionPreference = "Stop"

$Here      = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillsDir = if ($env:CLAUDE_SKILLS_DIR) { $env:CLAUDE_SKILLS_DIR } else { Join-Path $HOME ".claude\skills" }
$StateDir  = if ($env:CLAUDE_FB_STATE_DIR) { $env:CLAUDE_FB_STATE_DIR } else { Join-Path $HOME ".claude\facebook" }

if (-not (Get-Command python -ErrorAction SilentlyContinue) -and -not (Get-Command python3 -ErrorAction SilentlyContinue)) {
    Write-Warning "Python 3.8+ was not found. lint.py and beats.py need it."
}

New-Item -ItemType Directory -Force -Path $SkillsDir, $StateDir | Out-Null

Get-ChildItem (Join-Path $Here "skills") -Directory -Filter "fb-*" | ForEach-Object {
    $dest = Join-Path $SkillsDir $_.Name
    if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
    Copy-Item $_.FullName $dest -Recurse
    Write-Host "installed skill: $($_.Name)"
}

function Copy-IfAbsent($src, $dst) {
    if (Test-Path $dst) { Write-Host "kept existing:   $dst" }
    else { Copy-Item $src $dst; Write-Host "created:         $dst" }
}
Copy-IfAbsent (Join-Path $Here "templates\config.template.md") (Join-Path $StateDir "config.md")
Copy-IfAbsent (Join-Path $Here "templates\voice.template.md")  (Join-Path $StateDir "voice.md")
Copy-IfAbsent (Join-Path $Here "templates\log.template.md")    (Join-Path $StateDir "log.md")

Write-Host ""
Write-Host "Done. Next: restart Claude Code and run /fb-start"
