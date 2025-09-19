#!/usr/bin/env python3
"""
Script to initialize the database
Run this script to create the database tables
"""

from app import create_app
from db import init_db

if __name__ == '__main__':
    app = create_app()
    init_db(app)
    print("Database initialized successfully!")
