# ═══════════════════════════════════════════════════════════════
#  Sobe a API do Atlas em modo desenvolvimento (Windows).
#
#      .\scripts\api.ps1
#      .\scripts\api.ps1 8001
#
#  Se o PowerShell recusar o script:
#      Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
#
#  ⚠️ --reload é SÓ para desenvolvimento.
# ═══════════════════════════════════════════════════════════════
param([int]$Porta = 8000)

$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

if (-not (Test-Path ".env")) {
    Write-Host "🔴 .env não encontrado." -ForegroundColor Red
    Write-Host "   copy .env.example .env"
    Write-Host "   e depois gere a chave:"
    Write-Host '   python -c "import secrets; print(secrets.token_urlsafe(48))"'
    exit 1
}

if (Select-String -Path ".env" -Pattern "^ATLAS_SECRET_KEY=gere-uma-chave" -Quiet) {
    Write-Host "🔴 ATLAS_SECRET_KEY ainda é o valor de exemplo." -ForegroundColor Red
    Write-Host '   python -c "import secrets; print(secrets.token_urlsafe(48))"'
    exit 1
}

Write-Host "▶️  http://127.0.0.1:$Porta/docs" -ForegroundColor Green
Write-Host ""

uvicorn "atlas.api.aplicacao:criar_app" --factory --reload --port $Porta
