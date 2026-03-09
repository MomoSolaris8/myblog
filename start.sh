#!/bin/bash
# Start both Jekyll and the save server together
# Usage: bash start.sh

BLOG_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Starting save server on :4001..."
python3 "$BLOG_DIR/save-server.py" &
SAVE_PID=$!

echo "Starting Jekyll on :4000..."
cd "$BLOG_DIR"
~/.rbenv/versions/3.2.0/bin/bundle exec ~/.rbenv/versions/3.2.0/bin/jekyll serve

# When Jekyll stops (Ctrl+C), stop the save server too
kill $SAVE_PID 2>/dev/null
