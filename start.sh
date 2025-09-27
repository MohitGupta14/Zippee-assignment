#!/bin/bash
# start.sh - Enhanced with better debugging

set -e  # Exit on any error

echo "=== Starting application initialization ==="

# --- 1. Wait for Database ---
echo "Running database health check..."
python3 wait_for_db.py

if [ $? -ne 0 ]; then
  echo "FATAL: Database connection failed during wait script. Stopping startup."
  exit 1
fi

echo "Database connection successful!"

# --- 2. Check Flask-Migrate setup ---
echo "=== Checking Flask-Migrate setup ==="

# Check if migrations folder exists
if [ ! -d "migrations" ]; then
    echo "No migrations folder found. Initializing Flask-Migrate..."
    python3 -m flask db init
    if [ $? -ne 0 ]; then
        echo "FATAL: Failed to initialize Flask-Migrate"
        exit 1
    fi
fi

# Check if there are any migration files
if [ -z "$(find migrations/versions -name '*.py' 2>/dev/null)" ]; then
    echo "No migration files found. Creating initial migration..."
    python3 -m flask db migrate -m "Initial migration"
    if [ $? -ne 0 ]; then
        echo "FATAL: Failed to create initial migration"
        exit 1
    fi
fi

# --- 3. Apply database migrations ---
echo "=== Applying database migrations ==="
python3 -m flask db upgrade

if [ $? -ne 0 ]; then
  echo "FATAL: Database migration failed. Check the output above for errors."
  exit 1
fi

echo "Database migration successful!"

# --- 4. Start the Flask app ---
echo "=== Starting Flask application ==="
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=5000
python3 run.py