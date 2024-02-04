#!/usr/bin/env python3
import requests
import re
import sys

import webbrowser
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, unquote
import csv
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

contactInfo = {}
domain_endings = ['.com', '.ca', '.to', 'us', 'uk', 'org', 'net', 'info', 'biz']

def updateInfoSheet():
    with open('companyInfoSheet.csv', 'w', newline='') as file:
        # Step 4: Using csv.writer to write the list to the CSV file
        writer = csv.writer(file)
        for key in contactInfo.keys():
            contactInfo[key] = list(set(contactInfo[key]))
            if len(contactInfo[key]):
                writer.writerow([key, contactInfo[key][0]])
                for value in range(1, len(contactInfo[key])):
                    writer.writerow(["", contactInfo[key][value]])
            else:
                writer.writerow([key])
    
    webbrowser.open("file://" + os.path.realpath("companyInfoSheet.csv"))

def findContactInfo(companyName, companyLink):
    domain_endings_pattern = '|'.join(domain_endings)
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:" + domain_endings_pattern + r")"
    URL = companyLink

    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        response = requests.get(URL, timeout=10)
        
    except requests.exceptions.ConnectTimeout:
        contactInfo[companyName] = []
        print(f"Connection to {URL} timed out.")
        return
    except requests.exceptions.ConnectionError as e:
        contactInfo[companyName] = []
        print(f"Connection error occurred (invalid link): {e}")
        return
    except requests.exceptions.ReadTimeout:
        contactInfo[companyName] = []
        print(f"Read timeout occurred for {URL}")   
        return
    except requests.exceptions.TooManyRedirects:
        contactInfo[companyName] = []
        print(f"Too many redirects occurred for {URL}")
        return
    except requests.exceptions.RequestException as e:
        contactInfo[companyName] = []
        print(f"Request exception for {URL}: {e}")
        contactInfo[companyName] = ["Request exception"]
        return

    
    response.encoding = "utf-8"

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        inContactPage = False

        contactInfo[companyName] = []
        # print(response.url)
        print("Searching for contact info")

        for a_tag in soup.findAll("a"):
            link = a_tag.get("href")
            # print(link)
            if link is not None:
                if "https://www.instagram.com/" in link:
                    if link.endswith("/"):
                        link = link[:-1]
                    contactInfo[companyName].append("Insta @" + str(link.replace("https://www.instagram.com/", "")))
                    print("Insta @" + str(link.replace("https://www.instagram.com/", "")))


                if inContactPage == False and "contact" in link:
                    inContactPage = True
                    URL = urljoin(URL, link)
                    # print(URL)

                    response = requests.get(URL)
                    if "Form" in response.text or "form" in response.text:
                        contactInfo[companyName].append(URL)
                        print("Form " + URL)
                    
                    # print(response.text)
                    if "@" in response.text:
                        emails = re.findall(email_pattern, response.text)
                        for email in emails:
                            contactInfo[companyName].append(email)
                            print("Email " + email)
    
    else:
        print("Webscraper unable to access website")

    print("finished finding contact info")

def search_yahoo(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    search_url = "https://search.yahoo.com/search"
    params = {"p": query}
    response = requests.get(search_url, headers=headers, params=params)
    domainPassed = False

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Update the class/id based on Yahoo's search result structure
        result = soup.find('div', class_='Sr')

        try:
            yahoo_url = result.find('span').text if result.find('span') else 'No Title'
        except:
            contactInfo[query] = []
            print("unable to scrape link from yahoo")
            return

        if "instagram" in yahoo_url or "youtube" in yahoo_url or "wikipedia" in yahoo_url or "linkedin" in yahoo_url or "snapchat" in yahoo_url or "facebook" in yahoo_url or "reddit" in yahoo_url or "yahoo" in yahoo_url:
            contactInfo[query] = []
            print("not their website")
            return
        
        if " " in yahoo_url:
            yahoo_url = yahoo_url[:yahoo_url.index(" ")]

        for ending in domain_endings:
            end_index = yahoo_url.find(ending)
            if end_index != -1:
                # Extract up to the domain ending and add it back
                if yahoo_url.startswith("https://www."):
                    yahoo_url = yahoo_url[:end_index + len(ending)]
                elif yahoo_url.startswith("www."):
                    yahoo_url = "https://" + yahoo_url[:end_index + len(ending)]
                else:
                    yahoo_url = "https://www." + yahoo_url[:end_index + len(ending)]
                domainPassed = True
                break
                
        if domainPassed == False:
            contactInfo[query] = []
            print("domain not passed")
        elif yahoo_url != 'No Title':
            print(query, "website url", yahoo_url)
            findContactInfo(query, yahoo_url)

company_list = []

print("running scraper...")

while True:
    company = input()
    if company == "END" or company == "end" or company == "End":
        for i in company_list:
            search_yahoo(i)
        
        print(contactInfo)
        updateInfoSheet()   
        sys.exit()
        
    if company != "":
        company_list.append(company)
