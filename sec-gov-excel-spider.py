# # import requests
# # from bs4 import BeautifulSoup

# # response = requests.get('https://www.sec.gov/cgi-bin/viewer?action=view&cik=320193&accession_number=0000320193-23-000064&xbrl_type=v')
# # soup = BeautifulSoup(response.text,'html.parser')

# # excel_url = soup.find_all('a',class_='xbrlviewer')[1]

# # base_url = 'https://www.sec.gov/'

from sec_cik_mapper import StockMapper


import random
import re
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urljoin
import requests
import os
import time
from selenium.webdriver.common.by import By
import pandas as pd

# Specify the url
def download_excel(company_code,CIK,id,filing_date,reporting_date,document_type):                                            
    urlpage = f'https://www.sec.gov/cgi-bin/viewer?action=view&cik={CIK}&accession_number={id}&xbrl_type=v'

    options = uc.ChromeOptions()
    options.add_argument('--headless=new')

    download_dir = '/Users/liurunsen/Documents/sec excel'
    options.add_experimental_option('prefs', {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })

    driver = uc.Chrome(options=options)

    driver.get(urlpage)
    # click button
    excel_button = driver.find_element("link text", 'View Excel Document')
    excel_button.click()
    
    wait_for_download_to_complete(download_dir+'/Financial_Report.xlsx')
    # 'https://www.sec.gov/Archives/edgar/data/320193/000032019323000006/Financial_Report.xlsx'
    # Extract the link to the Excel document
    # soup = BeautifulSoup(driver.page_source, 'html.parser')
    
                                                                        #//*[@id="idm140221126789312"]/tbody/tr[43]/td[1]/a
   
    year = reporting_date[:4]   #//*[@id="idm140035138587824"]/tbody/tr[33]/td[2]
    quarter = 'Q' + str((int(reporting_date[5:7]) // 3))     #//*[@id="idm140221126789312"]/tbody/tr[38]/td[2]
    if(quarter == 'Q4'):
        quarter = 'FY'
    
    # Create filename
    filename_xlsx = f"{company_code}_{year}_{quarter}_{document_type}_{filing_date}_{reporting_date}.xlsx"
    filename_xls = f"{company_code}_{year}_{quarter}_{document_type}_{filing_date}_{reporting_date}.xls"

    filename_xlsx = filename_xlsx.replace('/', '-').replace(' ','')  # Replace / in date with -
    filename_xls = filename_xls.replace('/', '-').replace(' ','')  # Replace / in date with -

    try:
        if os.path.exists('/Users/liurunsen/Documents/sec excel/Financial_Report.xlsx'.strip()):
            old_file = os.path.join(download_dir, 'Financial_Report.xlsx')
            new_file = os.path.join(download_dir, filename_xlsx)
            print(filename_xlsx)
            os.rename(old_file, new_file)
        else:
            old_file = os.path.join(download_dir, 'Financial_Report.xls')
            new_file = os.path.join(download_dir, filename_xls)
            print(filename_xls)
            os.rename(old_file, new_file)
    except:
        print('Someting went wrong during changing file name')
    time.sleep(1)
    driver.quit()

def get_report_list(report_url_list):
    options = uc.ChromeOptions()
    options.add_argument('--headless=new')

    
    driver = uc.Chrome(options=options)
    driver.get(report_url_list)
    time.sleep(5)
    
    # Find and click on '10-K (annual reports) and 10-Q (quarterly reports)'
    driver.find_element(By.CSS_SELECTOR, '#filingsStart > div:nth-child(2) > div:nth-child(3) > h5').click();

    time.sleep(2)

    # Find and click on 'View all 10-Ks and 10-Qs'
    driver.find_element(By.CSS_SELECTOR, '#filingsStart > div:nth-child(2) > div:nth-child(3) > div > button.btn.btn-sm.btn-info.js-selected-view-all').click();
    # company_code = driver.find_element(By.ID,'ticker').text.split(' ')[0]
    # print(company_code)
    time.sleep(2)
    # CIK = driver.find_element(By.XPATH,'//*[@id="dataSource"]').text[3:][:-5]
    
    
    doc_count = len(driver.find_elements(By.CLASS_NAME,'even')) + len(driver.find_elements(By.CLASS_NAME,'odd'))
    info=[]
    for i in range(1,doc_count+1):
        filing_button_href = driver.find_element(By.XPATH,f'//*[@id="filingsTable"]/tbody/tr[{i}]/td[2]/div/a[2]').get_attribute('href')
        filing_date = driver.find_element(By.XPATH,f'//*[@id="filingsTable"]/tbody/tr[{i}]/td[3]').text.strip()
        reporting_date = driver.find_element(By.XPATH,f'//*[@id="filingsTable"]/tbody/tr[{i}]/td[4]/a').text.strip()
        document_type = driver.find_element(By.XPATH,f'//*[@id="filingsTable"]/tbody/tr[{i}]/td[1]').text.strip()
        id = re.search(r'\d+-\d+-\d+',filing_button_href).group(0)
        info.append((id,filing_date,reporting_date,document_type))
        # download_excel(company_code, CIK,id,filing_date,reporting_date,document_type,driver)
        # time.sleep(random.randint(4,7))
    # driver.find_element(By.XPATH,'//*[@id="filingsTable"]/tbody/tr[2]/td[3]') //*[@id="filingsTable"]/tbody/tr[1]/td[3] //*[@id="filingsTable"]/tbody/tr[2]/td[1]
    # driver.find_element(By.XPATH,'//*[@id="filingsTable"]/tbody/tr[2]/td[4]/a')
# //*[@id="filingsTable"]/tbody/tr[30]/td[2]/div //*[@id="filingsTable"]/tbody/tr[30]/td[3]
    # baseUrl = 'https://www.sec.gov/cgi-bin/viewer?action=view&cik=320193&accession_number={id}&xbrl_type=v'
    driver.quit()
    
    return info

    
    
def wait_for_download_to_complete(filePath):
    """
    Wait for the download to complete.
    """
    time_to_wait = 30
    counter = 0

    while not os.path.exists(filePath.strip()):
        time.sleep(1)
        counter+=1
        
        if(counter>time_to_wait):
            break
    # print(f'Download time: {counter}')    
    
        
def cik_lookup(code):
    mapper = StockMapper()
    return mapper.ticker_to_cik[code]

def main():
    
    sheet = pd.read_excel(io=r'/Users/liurunsen/Documents/VITO Company Tickers.xlsx')
    company_codes = sheet.iloc[:,1]
    
    for code in company_codes:
        
        CIK = cik_lookup(code)
        url = f'https://www.sec.gov/edgar/browse/?CIK={CIK}&owner=exclude'
        info = get_report_list(url)
        for id,filing_date,reporting_date,document_type in info:
            download_excel(code,CIK,id,filing_date,reporting_date,document_type,)   
            time.sleep(random.randint(2,5))
    
    
if __name__ == '__main__':
    main()
    
