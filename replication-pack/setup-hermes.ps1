# setup-hermes.ps1 - One-Click Persistence Setup for Hermes AI Stack (Windows)
# Version: 1.0.0

Write-Host "====================================================" -ForegroundColor Green
Write-Host "       HERMES AI LOCAL SETUP (WINDOWS)              " -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Green

# 1. Dependency Checks
Write-Host "`n[1/5] Checking dependencies..." -ForegroundColor Cyan

$docker = Get-Command docker -ErrorAction SilentlyContinue
if (!$docker) {
    Write-Host "Error: docker is not installed." -ForegroundColor Red
    exit 1
}

$python = Get-Command python -ErrorAction SilentlyContinue
if (!$python) {
    Write-Host "Error: python is not installed." -ForegroundColor Red
    exit 1
}

Write-Host "Dependencies OK." -ForegroundColor Green

# 2. Environment Configuration
Write-Host "`n[2/5] Configuring environment..." -ForegroundColor Cyan

if (!(Test-Path .env)) {
    Write-Host "Creating .env from template..." -ForegroundColor Yellow
    Copy-Item .env.template .env
    Write-Host ".env created." -ForegroundColor Green
} else {
    Write-Host "Existing .env found. Skipping template copy."
}

# 3. Database Bootstrap
Write-Host "`n[3/5] Bootstrapping PostgreSQL via Docker Compose..." -ForegroundColor Cyan

docker compose up -d

Write-Host "Waiting for database to be ready..."
$maxRetries = 30
$count = 0
while ($true) {
    $check = docker exec engram-db pg_isready -U gentleman 2>$null
    if ($LASTEXITCODE -eq 0) {
        break
    }
    Start-Sleep -Seconds 2
    $count++
    if ($count -ge $maxRetries) {
        Write-Host "Error: PostgreSQL failed to start in time. Check if Docker Desktop is running!" -ForegroundColor Red
        exit 1
    }
    Write-Host -NoNewline "."
}

Write-Host "`nPostgreSQL is ready." -ForegroundColor Green

# 4. Python Environment Setup
Write-Host "`n[4/5] Setting up Python Virtual Environment..." -ForegroundColor Cyan

if (!(Test-Path venv)) {
    python -m venv venv
    Write-Host "Virtual environment created." -ForegroundColor Green
} else {
    Write-Host "Existing venv found. Updating dependencies."
}

.\venv\Scripts\activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Write-Host "Python environment setup completed." -ForegroundColor Green

# 5. Bridge Verification
Write-Host "`n[5/5] Verifying Persistence Bridge..." -ForegroundColor Cyan

$verifyScript = @"
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

try:
    url = os.getenv('DATABASE_URL')
    print(f'Connecting to: {url.split("@")[1] if "@" in url else "Postgres"}')
    conn = psycopg2.connect(url)
    cur = conn.cursor()
    cur.execute('SELECT version();')
    version = cur.fetchone()
    print(f'SUCCESS: Connected to PostgreSQL! Version: {version[0]}')
    cur.close()
    conn.close()
except Exception as e:
    print(f'ERROR: Could not connect to database. {e}')
    exit(1)
"@

$verifyScript | Out-File -FilePath verify_bridge.py -Encoding utf8
python verify_bridge.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n====================================================" -ForegroundColor Green
    Write-Host "   SETUP COMPLETE: HERMES IS NOW PERSISTENT ON PC!  " -ForegroundColor Green
    Write-Host "====================================================" -ForegroundColor Green
    Write-Host "To start Hermes, run: .\venv\Scripts\activate.ps1; hermes-ai"
    Remove-Item verify_bridge.py
} else {
    Write-Host "Setup completed with verification errors." -ForegroundColor Red
    exit 1
}
