#!/bin/bash
# Start Backend
source venv/Scripts/activate
python start_backend.py &

# Wait for backend
sleep 3

# Start Frontend
cd frontend
npm run dev
