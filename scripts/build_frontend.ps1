# Corvi Frontend Build Script
# This script builds the frontend and restarts the Docker service

Write-Host "🔨 Building Corvi Frontend..." -ForegroundColor Blue

# Navigate to frontend directory
$frontendDir = Join-Path $PSScriptRoot "..\corvi_frontend"
Set-Location $frontendDir

# Install dependencies (if needed)
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
npm install

# Build the application
Write-Host "🏗️  Building application..." -ForegroundColor Yellow
npm run build

# Navigate to infra directory
$infraDir = Join-Path $PSScriptRoot "..\infra"
Set-Location $infraDir

# Restart the frontend service
Write-Host "🔄 Restarting frontend service..." -ForegroundColor Yellow
docker-compose restart frontend

Write-Host "✅ Frontend build and restart complete!" -ForegroundColor Green
Write-Host "🌐 Access the application at: http://localhost" -ForegroundColor Cyan