#!/bin/bash
# Build script for Render deployment
# Builds the frontend and copies it to the backend static directory

set -e

echo "=== Installing Backend Dependencies ==="
cd backend
pip install -r requirements.txt

echo "=== Installing Frontend Dependencies ==="
cd ../frontend
npm install --legacy-peer-deps

echo "=== Building Frontend ==="
npm run build

echo "=== Copying Frontend Build to Backend ==="
rm -rf ../backend/static
cp -r dist ../backend/static

echo "=== Build Complete ==="
ls -la ../backend/static/
