# import requests
# from bs4 import BeautifulSoup

# response = requests.get('https://www.sec.gov/cgi-bin/viewer?action=view&cik=320193&accession_number=0000320193-23-000064&xbrl_type=v')
# soup = BeautifulSoup(response.text,'html.parser')

# excel_url = soup.find_all('a',class_='xbrlviewer')[1]

# base_url = 'https://www.sec.gov/'



import undetected_chromedriver as uc

from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urljoin
import requests
import os

# Specify the url
urlpage = 'https://www.sec.gov/cgi-bin/viewer?action=view&cik=320193&accession_number=0000320193-23-000006&xbrl_type=v'

# Run Firefox WebDriver
driver = uc.Chrome()

driver.get(urlpage)

# Extract the link to the Excel document
soup = BeautifulSoup(driver.page_source, 'html.parser')
excel_link = soup.find('a', text='View Excel Document')['href']
print(excel_link)
excel_url = urljoin(urlpage, excel_link)
print(soup.find_all('td',class_='text'))
# Extract metadata for filename
entity_name = soup.find_all('td',class_='text')[12].text.strip()
document_type = soup.find_all('td',class_='text')[2].text.strip()
document_date = soup.find_all('td',class_='text')[6].text.strip()

# Create filename
filename = f"{entity_name} - {document_type} - {document_date}.xlsx"
filename = filename.replace('/', '-')  # Replace / in date with -
print(filename)

# Download the file
response = requests.get(excel_url)

# Save the content in an Excel file
with open(filename, 'wb') as output:
    output.write(response.content)


print(f'File downloaded and saved as {filename}')

