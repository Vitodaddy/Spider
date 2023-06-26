# # import requests
# # from bs4 import BeautifulSoup

# # response = requests.get('https://www.sec.gov/cgi-bin/viewer?action=view&cik=320193&accession_number=0000320193-23-000064&xbrl_type=v')
# # soup = BeautifulSoup(response.text,'html.parser')

# # excel_url = soup.find_all('a',class_='xbrlviewer')[1]

# # base_url = 'https://www.sec.gov/'


import re
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urljoin
import requests
import os
import time
from selenium.webdriver.common.by import By

# Specify the url
def download_excel():
    urlpage = 'https://www.sec.gov/cgi-bin/viewer?action=view&cik=320193&accession_number=0000320193-23-000006&xbrl_type=v'

    options = uc.ChromeOptions()
    download_dir = r'C:\Users\Administrator\Desktop\SA_Spider\sec-excel'
    options.add_experimental_option('prefs', {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })
    driver = uc.Chrome(options=options)

    driver.get(urlpage)
    # click button
    # excel_button = driver.find_element("link text", 'View Excel Document')
    # excel_button.click()
    # time.sleep(10)
    # 'https://www.sec.gov/Archives/edgar/data/320193/000032019323000006/Financial_Report.xlsx'
    # # Extract the link to the Excel document
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    

    entity_name = soup.find_all('td',class_='text')[59].text.strip()
    year = soup.find_all('td',class_='text')[6].text.strip()[-4:]
    quater = soup.find_all('td',class_='text')[47].text.strip()
    document_type = soup.find_all('td',class_='text')[2].text.strip()
    document_date = soup.find_all('td',class_='text')[6].text.strip()

    # Create filename
    filename = f"{entity_name} - {document_type} - {document_date}.xlsx"
    filename = filename.replace('/', '-').replace(' ','')  # Replace / in date with -
    old_file = os.path.join(download_dir, 'Financial_Report.xlsx')
    new_file = os.path.join(download_dir, filename)

    os.rename(old_file, new_file)
    driver.quit()

def get_report_list():
    report_url_list = 'https://www.sec.gov/edgar/browse/?CIK=66740&owner=exclude'

    driver = uc.Chrome()
    driver.get(report_url_list)
    time.sleep(10)
    
    # Find and click on '10-K (annual reports) and 10-Q (quarterly reports)'
    driver.find_element(By.CSS_SELECTOR, '#filingsStart > div:nth-child(2) > div:nth-child(3) > h5').click();

    time.sleep(2)

    # Find and click on 'View all 10-Ks and 10-Qs'
    driver.find_element(By.CSS_SELECTOR, '#filingsStart > div:nth-child(2) > div:nth-child(3) > div > button.btn.btn-sm.btn-info.js-selected-view-all').click();

    time.sleep(2)
    
    soup = BeautifulSoup(driver.page_source,'html.parser')
    odd_row = soup.find_all('tr',class_='odd')
    even_row = soup.find_all('tr',class_='even')
    for i in odd_row:
        print(i)
        date = re.findall(r'class="sorting_1">([^<]*)', i)
        print(date)
    # baseUrl = 'https://www.sec.gov/cgi-bin/viewer?action=view&cik=320193&accession_number={id}&xbrl_type=v'
    driver.quit()

def main():
    get_report_list()
    
    
if __name__ == '__main__':
    main()
    
