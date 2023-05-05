#!/bin/bash

# Run the Python scripts using Pipenv
echo "Running scrape_dum_jogy.py"
python scrape_dum_jogy.py

echo "Running scrape_yk.py"
python scrape_yk.py

echo "Running combine_and_upload.py"
python combine_and_upload.py

echo "All scripts executed successfully."
