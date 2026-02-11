#!/bin/bash

# Exit immediately if any command fails
set -e

# --- Argument Parsing & Validation ---
if [ -z "$1" ]; then
    echo "❌ ERROR: Missing root path argument."
    echo "Usage: $0 <root-path>"
    exit 1
fi

ROOT_PATH="$1"

if [ ! -d "$ROOT_PATH" ]; then
    echo "❌ ERROR: $ROOT_PATH is not a valid directory."
    exit 1
fi

echo "🔍 Scanning root path: $ROOT_PATH"

# --- Main Loop ---
for dir in "$ROOT_PATH"/*/ ; do
    [ -d "$dir" ] || continue
    echo "📂 Checking directory: $dir"
    cd "$dir"

    if [ -f "docker-compose.yml" ]; then
        echo "✅ Found docker-compose.yml"
        echo "⬇️ Running docker compose pull..."
        docker compose pull

        echo "🚀 Running docker compose up -d..."
        docker compose up -d
    else
        echo "⚠️ No docker-compose.yml found here."
    fi

    cd - > /dev/null
done

echo "✅ All done!"
