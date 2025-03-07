#!/bin/bash

# Run database initialization
python database.py

# Start the Flask application
gunicorn -w 4 -b 0.0.0.0:10000 app:app
