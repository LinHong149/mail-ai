import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, unquote
import csv

contactInfo = {}
domain_endings = ['.com', '.ca', '.to', 'us', 'uk', 'org', 'net', 'info', 'biz']

def updateInfoSheet():
    with open('companyInfoSheet.csv', 'w', newline='') as file:
        # Step 4: Using csv.writer to write the list to the CSV file
        writer = csv.writer(file)
        for key in contactInfo.keys():
            if len(contactInfo[key]):
                writer.writerow([key, contactInfo[key][0]])
                for value in range(1, len(contactInfo[key])):
                    writer.writerow(["", contactInfo[key][value]])
            else:
                writer.writerow([key])

def findContactInfo(companyName, companyLink):
    domain_endings_pattern = '|'.join(domain_endings)
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:" + domain_endings_pattern + r")"
    URL = companyLink
    response = requests.get(URL)
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.content, "html.parser")

    inContactPage = False

    contactInfo[companyName] = []
    # print(response.url)
    print("Searching for contact info")
    for a_tag in soup.findAll("a"):
        link = a_tag.get("href")
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
                    contactInfo[companyName].append("Form " + URL)
                    print("Form " + URL)
                
                # print(response.text)
                if "@" in response.text:
                    emails = re.findall(email_pattern, response.text)
                    for email in emails:
                        contactInfo[companyName].append("Email " + email)
                        print("Email " + email)

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

        yahoo_url = result.find('span').text if result.find('span') else 'No Title'

        for ending in domain_endings:
            end_index = yahoo_url.find(ending)
            if end_index != -1:
                # Extract up to the domain ending and add it back
                yahoo_url = "https://" + yahoo_url[:end_index + len(ending)]
                domainPassed = True
                break
                
        if domainPassed == False:
            contactInfo[query] = ["Unsupported domain"]
        elif yahoo_url != 'No Title':
            print(yahoo_url)
            findContactInfo(query, yahoo_url)

search_query = input()
while search_query != "END" and  search_query != "End" and  search_query != "end":
    search_yahoo(search_query)
    search_query = input()

# findContactInfo("bb", "https://www.burnbraefarms.com")
print(contactInfo)

updateInfoSheet()
