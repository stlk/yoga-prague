#!/bin/bash

# Check if Pipenv is installed
command -v pipenv >/dev/null 2>&1 || { echo >&2 "Pipenv is required, but not installed. Aborting."; exit 1; }

# Run the Python scripts using Pipenv
echo "Running scrape_dum_jogy.py"
pipenv run python scrape_dum_jogy.py

echo "Running scrape_yk.py"
pipenv run python scrape_yk.py

echo "Running combine_and_upload.py"
pipenv run python combine_and_upload.py

echo "All scripts executed successfully."
