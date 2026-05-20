#!/bin/bash
# Usage: create_desktop_symlinks.sh <project_id>
PROJECT_ID="$1"
WORKSPACE="/Users/danieldanut/Agentic Workspace"
DESKTOP="$HOME/Desktop"

DOCS_SRC="$WORKSPACE/Youtube/Output/3. Pre-production Materials/$PROJECT_ID"
RAW_SRC="$WORKSPACE/Youtube/Output/4. Editing/$PROJECT_ID/originals"
DOCS_LINK="$DESKTOP/${PROJECT_ID}-docs"
RAW_LINK="$DESKTOP/${PROJECT_ID}-raw"

[ -L "$DOCS_LINK" ] && rm "$DOCS_LINK"
[ -L "$RAW_LINK" ] && rm "$RAW_LINK"

ln -s "$DOCS_SRC" "$DOCS_LINK"
ln -s "$RAW_SRC" "$RAW_LINK"

echo "Desktop symlinks created: ${PROJECT_ID}-docs and ${PROJECT_ID}-raw"
