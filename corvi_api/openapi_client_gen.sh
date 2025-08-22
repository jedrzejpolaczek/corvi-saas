#!/usr/bin/env bash
set -euo pipefail
API_URL="${API_URL:-http://api:8000/openapi.json}"
OUT_DIR="/workspace/corvi_frontend/src/api"
mkdir -p "$OUT_DIR"
./node_modules/.bin/openapi-typescript "$API_URL" --output "$OUT_DIR/types.d.ts"
