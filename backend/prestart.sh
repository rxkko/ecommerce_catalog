#!/bin/bash

echo "Checking for alembic.ini..."
if [ -f alembic.ini ]; then
    echo "Running migrations..."
    alembic upgrade head || echo "Migrations failed"
fi

echo "Starting server..."
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4