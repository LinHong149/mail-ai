#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then 
    echo "Python 3 is not installed. Please install Python 3 to continue."
    exit
fi

curl -sSL -o scraper.py "https://raw.githubusercontent.com/LinHong149/mail-ai/main/your_script.py"

pip3 install requests beautifulsoup4

python3 scraper.py