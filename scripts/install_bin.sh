#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="/usr/local/bin"
SOURCE_DIR="$(dirname "$0")/../ec_tools_cli/bin"

echo "🔍 Checking if $TARGET_DIR exists..."
if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ ERROR: $TARGET_DIR does not exist on this system."
    exit 1
fi

echo "📂 Copying shell scripts from $SOURCE_DIR to $TARGET_DIR..."
if compgen -G "$SOURCE_DIR/*.sh" > /dev/null; then
    for file in "$SOURCE_DIR"/*.sh; do
        echo "➡️  Installing $(basename "$file")"
        sudo cp "$file" "$TARGET_DIR/"
        sudo chmod +x "$TARGET_DIR/$(basename "$file")"
    done
    echo "✅ Installation completed."
else
    echo "⚠️ No .sh files found in $SOURCE_DIR"
fi
