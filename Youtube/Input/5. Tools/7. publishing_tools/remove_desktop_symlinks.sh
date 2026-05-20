#!/bin/bash
# Usage: remove_desktop_symlinks.sh <project_id>
PROJECT_ID="$1"
DESKTOP="$HOME/Desktop"

for suffix in "-docs" "-raw"; do
  LINK="$DESKTOP/${PROJECT_ID}${suffix}"
  if [ -L "$LINK" ]; then
    rm "$LINK"
    echo "Removed desktop symlink: ${PROJECT_ID}${suffix}"
  fi
done
