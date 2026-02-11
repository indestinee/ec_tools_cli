#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="/usr/local/bin"
SOURCE_DIR="$(dirname "$0")/../ec_tools_cli/bin"

echo "🔍 Checking if $TARGET_DIR exists..."
if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ ERROR: $TARGET_DIR does not exist on this system."
    exit 1
fi

echo "🧹 Removing installed shell scripts from $TARGET_DIR..."
if compgen -G "$SOURCE_DIR/*.sh" > /dev/null; then
    for file in "$SOURCE_DIR"/*.sh; do
        target="$TARGET_DIR/$(basename "$file")"
        if [ -f "$target" ]; then
            echo "🗑️  Deleting $target"
            sudo rm -f "$target"
        else
            echo "⚠️  $target not found, skipping"
        fi
    done
    echo "✅ Uninstall completed."
else
    echo "⚠️ No .sh files found in $SOURCE_DIR"
fi
