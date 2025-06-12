#!/bin/bash

echo "Building site for GitHub Pages..."
python3 -m src.main "/flatpy/"
echo "Build completed! Site built in docs/ directory." 
