# Devloop AI — Setup script for Windows
# Run from PowerShell: .\scripts\setup.ps1
# Or: powershell -ExecutionPolicy Bypass -File scripts\setup.ps1

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$AiDir = Join-Path $RepoRoot "ai"
$PromptDir = Join-Path $RepoRoot "prompt"
$VenvDir = Join-Path $RepoRoot ".venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"

Write-Host "Devloop AI — Setup" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
Write-Host "Repo: $RepoRoot"
Write-Host ""

# Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    if (-not (Get-Command python3 -ErrorAction SilentlyContinue)) {
        Write-Host "Python 3 is required. Install it first." -ForegroundColor Red
        exit 1
    }
    $PythonCmd = "python3"
} else {
    $PythonCmd = "python"
}

# Create venv
if (-not (Test-Path $VenvDir)) {
    Write-Host "Creating virtual environment..."
    & $PythonCmd -m venv $VenvDir
    Write-Host "  Venv created" -ForegroundColor Green
}

# Install dependencies
Write-Host "Installing dependencies..."
$PipPath = Join-Path $VenvDir "Scripts\pip.exe"
& $PipPath install -q -r (Join-Path $RepoRoot "requirements.txt")
Write-Host "  Dependencies installed" -ForegroundColor Green

# Get or create PowerShell profile
$ProfilePath = $PROFILE
$ProfileDir = Split-Path -Parent $ProfilePath

if (-not (Test-Path $ProfileDir)) {
    New-Item -ItemType Directory -Path $ProfileDir -Force | Out-Null
}

if (-not (Test-Path $ProfilePath)) {
    New-Item -ItemType File -Path $ProfilePath -Force | Out-Null
}

# Prompt for Linear API key
$Marker = "# --- Devloop AI (do not edit this line) ---"
$ExistingContent = Get-Content $ProfilePath -Raw -ErrorAction SilentlyContinue
$LinearKey = ""

if ($ExistingContent -notmatch "LINEAR_API_KEY" -and -not $env:LINEAR_API_KEY) {
    Write-Host ""
    $LinearKey = Read-Host "Enter your Linear API key (or press Enter to skip and add later)"
    $LinearKey = $LinearKey.Trim().Trim('"')
} else {
    Write-Host "LINEAR_API_KEY already in config or env. Skipping."
}

# Block to append
$Block = @"

$Marker
# Devloop AI — added by setup.ps1
`$env:PATH = "`$env:PATH;$VenvDir\Scripts"

# Aliases (functions)
function ai-go { & $VenvPython $AiDir\ai_go.py @args }
function ai-start { & $VenvPython $AiDir\ai_start.py @args }
function ai-pr { & $VenvPython $AiDir\ai_pr.py @args }
function ai-list { & $VenvPython $AiDir\ai_list.py @args }
function ai-prompt { & $VenvPython $AiDir\ai_prompt.py @args }
function ai-status { & $VenvPython $AiDir\ai_status.py @args }
function ai-done { & $VenvPython $AiDir\ai_done.py @args }
function ws-create { & $VenvPython $AiDir\ws_create.py @args }

"@

if ($LinearKey) {
    $Block += @"

`$env:LINEAR_API_KEY = "$LinearKey"
`$env:LINEAR_READY_STATE = "Ready for build"

"@
}

$Block += @"
# Warp/Claude quick commands (copy prompts to clipboard)
function wv { Get-Content "$PromptDir\warp_velocity.md" | Set-Clipboard; Write-Host "warp_velocity copied" }
function wo { Get-Content "$PromptDir\warp_orchestrator.md" | Set-Clipboard; Write-Host "warp_orchestrator copied" }
function wr { Get-Content "$PromptDir\warp_review.md" | Set-Clipboard; Write-Host "warp_review copied" }
function wd { Get-Content "$PromptDir\warp_debug.md" | Set-Clipboard; Write-Host "warp_debug copied" }
function wa { Get-Content "$PromptDir\warp_architecture.md" | Set-Clipboard; Write-Host "warp_architecture copied" }
function co { Get-Content "$PromptDir\claude_orchestrator.md" | Set-Clipboard; Write-Host "claude_orchestrator copied" }
function cs { Get-Content "$PromptDir\claude_session_bootstrap.md" | Set-Clipboard; Write-Host "claude_session_bootstrap copied" }

# --- End Devloop AI ---

"@

# Append only if not already present
if ($ExistingContent -notmatch [regex]::Escape($Marker)) {
    Add-Content -Path $ProfilePath -Value $Block
    Write-Host "  Config appended to $ProfilePath" -ForegroundColor Green
} else {
    Write-Host "Devloop AI block already in profile. Skipping."
}

# Check for cursor command
if (-not (Get-Command cursor -ErrorAction SilentlyContinue)) {
    Write-Host ""
    Write-Host "Cursor shell command not found." -ForegroundColor Yellow
    Write-Host "In Cursor: Ctrl+Shift+P -> Shell Command: Install 'cursor' command in PATH"
}

# Check for gh
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host ""
    Write-Host "GitHub CLI (gh) not found." -ForegroundColor Yellow
    Write-Host "Required for ai-pr. Install: https://cli.github.com/"
}

Write-Host ""
Write-Host "Setup complete." -ForegroundColor Green
Write-Host ""
Write-Host "Reload your profile or open a new PowerShell window:"
Write-Host "  . `$PROFILE"
Write-Host ""
Write-Host "Then try: ai-list"
