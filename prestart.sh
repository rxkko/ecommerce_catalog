#!/bin/bash

if [ -f alembic.ini ]; then
    alembic upgrade head
fi

uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4