# ContactHarvester

## Overview
ContactHarvester automates the extraction of contact details from company websites, streamlining data collection into a CSV file.

## Features
- Automated scraping of emails, phone numbers, and social media links from websites.
- Outputs collected data into an organized CSV file for easy analysis.
- Supports a wide range of domains with high accuracy.
- Simple installation and execution, requiring minimal user input.

## Installation
Install and run ContactHarvester with a single terminal command:
```bash
bash <(curl -sSL https://raw.githubusercontent.com/LinHong149/mail-ai/main/install_and_run.sh)
```

## Usage
After the successful installation of ContactHarvester, the tool will automatically begin to scrape for contact information from the specified list of company websites. The extracted data, including email addresses, phone numbers, and social media profiles, will be saved into a CSV file named `companyInfoSheet.csv` in the current working directory.

For advanced usage and options, refer to the comprehensive documentation provided within the application.

## Requirements
- **Python**: Requires version 3.6 or later for full compatibility with the script's dependencies and features.
- **Libraries**: Essential libraries such as `requests` for handling HTTP requests and `beautifulsoup4` for parsing HTML are necessary. These will be automatically installed by the installation script if not present.
- **Internet Connection**: A stable internet connection is needed to download necessary dependencies, access target websites for data scraping, and receive script updates.

## Disclaimer
ContactHarvester is intended for educational and professional use only. Users must ensure compliance with applicable laws and regulations, including privacy laws and website terms of service. Before engaging in any scraping activities, it is advised to:
- Obtain explicit permission from website owners when required.
- Adhere to directives in robots.txt files and HTTP headers regarding scraping.
- Employ the data collected in a responsible and ethical manner.
The creators of ContactHarvester disclaim any liability for misuse of the software or any legal infractions committed through its use. Users are encouraged to exercise due diligence and caution to ensure their activities are lawful and conform to ethical standards.
