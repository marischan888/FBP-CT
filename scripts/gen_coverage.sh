#!/bin/bash

# Set working dir to project root
cd "$(dirname "$0")"/..

# Define output folder
OUTPUT_DIR="coverage"
HTML_DIR="$OUTPUT_DIR/html"
DATA_FILE="$OUTPUT_DIR/.cover"

# Clear and recreate output directory
rm -rf "$OUTPUT_DIR"
mkdir -p "$HTML_DIR"

# OS detection
UNAME=$(uname)
if [[ "$UNAME" == "Darwin" ]]; then
    echo "Running on macOS..."
elif [[ "$UNAME" == "Linux" ]]; then
    echo "Running on Linux..."
else
    echo "Running on Windows or unknown system..."
fi

# Run pytest with coverage
echo "Running coverage..."
coverage run --source=test -m pytest

# Save data file into custom directory
coverage json -o "$OUTPUT_DIR/coverage.json"
cp .coverage "$DATA_FILE"

# Generate HTML report
coverage html -d "$HTML_DIR"
echo "Coverage HTML report generated in $HTML_DIR"

# Open in browser automatically
#if [[ "$UNAME" == "Darwin" ]]; then
#    open "$HTML_DIR/index.html"
#elif [[ "$UNAME" == "Linux" ]]; then
#    xdg-open "$HTML_DIR/index.html" 2>/dev/null
#fi
