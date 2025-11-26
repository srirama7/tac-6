#!/usr/bin/env python3
import os

# Get the ANTHROPIC_API_KEY from environment
api_key = os.environ.get('ANTHROPIC_API_KEY')

if api_key:
    # Read current .env
    env_path = 'app/server/.env'
    with open(env_path, 'r') as f:
        lines = f.readlines()

    # Remove placeholder line
    lines = [line for line in lines if 'sk-ant-api03-test-key-for-e2e-testing-placeholder' not in line]

    # Add real key
    lines.append(f'ANTHROPIC_API_KEY={api_key}\n')

    # Write back
    with open(env_path, 'w') as f:
        f.writelines(lines)

    print('✓ Added ANTHROPIC_API_KEY to .env')
else:
    print('✗ ANTHROPIC_API_KEY not found in environment')
    print('The test may fail without a valid API key')
