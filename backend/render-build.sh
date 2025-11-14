#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip and install dependencies
pip install --upgrade pip setuptools wheel

# Install dependencies without cache to avoid build issues
pip install --no-cache-dir -r requirements.txt

# Run database migrations
python migrate_db.py
