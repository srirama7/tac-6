#!/bin/bash
# Update .env with ANTHROPIC_API_KEY from environment
cd app/server
if [ -n "$ANTHROPIC_API_KEY" ]; then
    # Remove placeholder if it exists
    sed -i '/ANTHROPIC_API_KEY=sk-ant-api03-test-key-for-e2e-testing-placeholder/d' .env
    # Add the real key
    echo "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY" >> .env
    echo "✓ Added ANTHROPIC_API_KEY to .env"
else
    echo "✗ ANTHROPIC_API_KEY not found in environment"
    echo "Please set it: export ANTHROPIC_API_KEY='your-key-here'"
    exit 1
fi
