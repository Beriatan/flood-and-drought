#!/usr/bin/env bash

# This script will zip the project and move it to the specified directory
cd ..
zip -r scripts/project.zip . -x "scripts/*" -x "node_modules/*" -x "project.zip" -x ".gitignore/*" -x ".git/*" -x ".DS_Store/*" -x ".idea/*" -x "terraform/*"