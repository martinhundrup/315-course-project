#!/bin/bash

echo " Creating virtual environment..."
python3 -m venv venv

echo " Activating virtual environment..."
source venv/bin/activate

echo "  Upgrading pip..."
python -m pip install --upgrade pip

echo " Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo " Running main.py (optional)..."
python main.py
