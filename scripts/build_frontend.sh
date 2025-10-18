#!/bin/bash

# Corvi Frontend Build Script
# This script builds the frontend and restarts the Docker service

echo "🔨 Building Corvi Frontend..."

# Navigate to frontend directory
cd "$(dirname "$0")/../corvi_frontend"

# Install dependencies (if needed)
echo "📦 Installing dependencies..."
npm install

# Build the application
echo "🏗️  Building application..."
npm run build

# Navigate to infra directory
cd ../infra

# Restart the frontend service
echo "🔄 Restarting frontend service..."
docker-compose restart frontend

echo "✅ Frontend build and restart complete!"
echo "🌐 Access the application at: http://localhost"