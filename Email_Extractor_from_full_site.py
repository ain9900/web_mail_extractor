import requests
from bs4 import BeautifulSoup
import re
from openpyxl import Workbook
from urllib.parse import urlparse

# Regular expression pattern to match email addresses
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Function to scrape email addresses from a given URL
def scrape_emails(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    emails = re.findall(email_pattern, soup.get_text())
    return emails

# Function to find all links on a page from the same domain
def find_links(url, domain):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('http'):
            parsed_url = urlparse(href)
            if parsed_url.netloc == domain:
                links.append(href)
    return links

# Function to visit each link and scrape email addresses
def visit_links(url):
    visited = set()
    queue = [url]
    domain = urlparse(url).netloc
    visited_count = 0

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Emails'
    row = 1

    while queue:
        current_url = queue.pop(0)
        visited.add(current_url)
        visited_count += 1
        print("Links visited:", visited_count)

        email_list = scrape_emails(current_url)
        if email_list:
            for email in email_list:
                sheet.cell(row=row, column=1, value=email)
                row += 1

        new_links = find_links(current_url, domain)
        for link in new_links:
            if link not in visited and link not in queue:
                queue.append(link)

    workbook.save('emails.xlsx')

# Starting URL
starting_url = 'https://www.ssgbd.com'

# Call the function to visit links and scrape email addresses
visit_links(starting_url)
