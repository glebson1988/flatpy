#!/bin/bash
echo "Running all tests..."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python3 -m unittest discover -s src -p "test_*.py" -v
