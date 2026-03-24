#!/usr/bin/env bash
set -euo pipefail

# Resolve the plugin root directory (parent of scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

COLLECTION_NAME="minimalist-entrepreneur"
QMD_INDEX="${HOME}/.config/qmd/index.yml"
DATA_DIR="${PLUGIN_DIR}/data/book"

# 1. Check if qmd is installed
if ! command -v qmd &>/dev/null; then
  echo "qmd is not installed. Install it from https://github.com/tobi/qmd and re-run this script."
  exit 0
fi

# 2. Verify data directory exists
if [[ ! -d "${DATA_DIR}" ]]; then
  echo "ERROR: Data directory not found at ${DATA_DIR}"
  echo "Ensure data/book/ contains the markdown files before running setup."
  exit 1
fi

# 3. Check if collection already exists in qmd index
if [[ -f "${QMD_INDEX}" ]] && grep -q "^  ${COLLECTION_NAME}:" "${QMD_INDEX}" 2>/dev/null; then
  echo "Collection '${COLLECTION_NAME}' already exists in ${QMD_INDEX}. Skipping registration."
else
  echo "Adding '${COLLECTION_NAME}' collection to qmd index..."

  # Ensure the config directory and file exist
  mkdir -p "$(dirname "${QMD_INDEX}")"
  if [[ ! -f "${QMD_INDEX}" ]]; then
    echo "collections:" > "${QMD_INDEX}"
  fi

  # 4. Append collection to index.yml
  cat >> "${QMD_INDEX}" <<YAML
  ${COLLECTION_NAME}:
    path: ${PLUGIN_DIR}/data/book
    pattern: "**/*.md"
    context:
      "": "The Minimalist Entrepreneur by Sahil Lavingia — full book text indexed by chapter and page. Use for grounding business advice in specific book passages, quotes, and case studies."
YAML

  echo "Collection registered at path: ${PLUGIN_DIR}/data/book"
fi

# 5. Run qmd update and embed
echo "Indexing and embedding files..."
qmd update
qmd embed

# 6. Report results
FILE_COUNT=$(find "${DATA_DIR}" -name '*.md' -type f | wc -l | tr -d ' ')
echo "Setup complete. Indexed ${FILE_COUNT} markdown file(s) from data/book/."
