#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then 
    echo "Python 3 is not installed. Please install Python 3 to continue."
    exit
fi

echo 
echo "████╗   ████╗  ████╗  █████╗  ███╗  ████╗ █████╗ █╗  ████╗ █████╗"
echo "█╔══█╗ █╔═══█╗ █╔══█╗ █╔═══╝ █╔══█╗ █╔══█╗╚═█╔═╝ █║ █╔═══╝ █╔═══╝"
echo "████╔╝ █║   █║ ████╔╝ ███╗   █████║ ████╔╝  █║   █║ █║     █████╗"
echo "█╔══█╗ █║   █║ █╔══█╗ █╔═╝   █╔══█║ █╔══█╗  █║   █║ █║     ╚═══█║"
echo "█║  █║ ╚████╔╝ ████╔╝ █████╗ █║  █║ █║  █║  █║   █║ ╚████╗ █████║"
echo "╚╝  ╚╝  ╚═══╝  ╚═══╝  ╚════╝ ╚╝  ╚╝ ╚╝  ╚╝  ╚╝   ╚╝  ╚═══╝ ╚════╝"
echo 
echo " _                                                         "
echo "/   _  ._ _|_  _.  _ _|_    |_|  _. ._    _   _ _|_  _  ._"
echo "\_ (_) | | |_ (_| (_  |_    | | (_| | \/ (/_ _>  |_ (/_ | "

curl -sSL -o scraper.py "https://raw.githubusercontent.com/LinHong149/robeartics-contact-harvester/main/scraper.py"

pip3 install requests beautifulsoup4

python3 scraper.py