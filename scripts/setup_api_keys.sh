#!/bin/bash
# Setup API keys for E2E testing
# This script ensures ANTHROPIC_API_KEY is available in app/server/.env

ENV_FILE="app/server/.env"

# If ANTHROPIC_API_KEY is in environment, add it to .env
if [ -n "$ANTHROPIC_API_KEY" ]; then
    # Remove any existing ANTHROPIC_API_KEY lines
    grep -v "^ANTHROPIC_API_KEY=" "$ENV_FILE" > "${ENV_FILE}.tmp" 2>/dev/null || touch "${ENV_FILE}.tmp"
    # Add the key from environment
    echo "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY" >> "${ENV_FILE}.tmp"
    mv "${ENV_FILE}.tmp" "$ENV_FILE"
    echo "[OK] Added ANTHROPIC_API_KEY from environment to $ENV_FILE"
else
    echo "[WARNING] ANTHROPIC_API_KEY not found in environment"
    echo "E2E tests may fail without a valid API key"
    echo "Please export ANTHROPIC_API_KEY or add it manually to $ENV_FILE"
fi
