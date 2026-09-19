$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
if (-not (Test-Path -LiteralPath '.venv/Scripts/python.exe')) {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Virtual environment creation failed' }
}
& .venv/Scripts/python.exe -m pip install -e '.[mcp,dev]'
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed' }
& .venv/Scripts/python.exe -m modelatlas coverage
if ($LASTEXITCODE -ne 0) { throw 'Knowledge-base validation failed' }
Write-Host 'Ready. Run .venv/Scripts/python.exe -m modelatlas paper2overview path/to/paper.pdf'
