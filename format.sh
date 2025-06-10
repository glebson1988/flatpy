#!/bin/bash

echo "🎯 Formatting code with Black..."
black src/

echo "📚 Sorting imports with isort..."
isort src/

echo "🔍 Checking code style with flake8..."
flake8 src/ --config=pyproject.toml

echo "✅ Done! Code formatted and checked." 
