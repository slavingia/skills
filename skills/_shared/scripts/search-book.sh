#!/bin/bash
# Search the Minimalist Entrepreneur book via qmd
# Usage: bash search-book.sh "query string" [num_results]
set -euo pipefail
QUERY="${1:?Usage: search-book.sh \"query\" [num_results]}"
NUM="${2:-3}"
qmd query "$QUERY" -c minimalist-entrepreneur -n "$NUM" --full 2>/dev/null || echo "qmd not available — using built-in knowledge only"
