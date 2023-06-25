import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent


def get_company_website():
    urls = []
    sheet = pd.read_excel(io='/Users/liurunsen/Documents/VITO Company Tickers.xlsx')
    company_names = sheet.iloc[:,1]
    for com in  company_names:
        urls.append(f'https://seekingalpha.com/symbol/{com}/earnings/transcripts')
    return urls

def get_button_href(url):

    # Path to your chromedriver (update it according to your setup)
    webdriver_service = Service('path/to/your/chromedriver')

    #Generatge random user-agent
    
    options=Options()
    ua=UserAgent()
    userAgent = ua.random
    options.add_argument(f'user-agent={userAgent}')
    

    # initiate the webdriver for Chrome browser
    driver = webdriver.Chrome(options= options,service=webdriver_service)

    #Change viewport
    #driver.set_window_size(100, 100)

    # navigate to the target URL
    driver.get(url)

    # wait until the required buttons are loaded
    wait = WebDriverWait(driver, 10)
    
    # list to hold the unique hrefs
    hrefs = set()
    try:
        while True:
            time.sleep(2)

            # find all buttons with the given text
            buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(text(), "Earnings Call Transcript")]')))
            
            new_hrefs_found = False

            for button in buttons:
                href = button.get_attribute('href')
                if href not in hrefs:
                    hrefs.add(href)
                    new_hrefs_found = True
                    #print(f"Found new href: {href}")
            
            # if no new hrefs found, stop scrolling
            if not new_hrefs_found:
                break

            # Scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # adding sleep to let the new content load
            time.sleep(random.randint(3,8))
    except Exception as e:
        print("An error occurred: ", str(e))

    # don't forget to close the driver
    driver.quit()

    return hrefs
    
    


def get_audio_id(hrefs):
    audio_ids = []
    for href in hrefs:
        audio_ids.append(href[33:].split('-')[0])
        
    return audio_ids



    
def download_audio(url):
    

    filename = url.split("/")[-1]

    # send GET request
    response = requests.get(url, stream=True)

    # check if the request is successful
    if response.status_code == 200:
        # open the file in write-binary mode
        with open(filename, 'wb') as file:
            # write the contents of the response to the file
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"The MP3 file has been downloaded as {filename}.")
    else:
        print("Failed to download the file.")


def main():
    urls = get_company_website()
    for url in urls:
        hrefs=get_button_href(url)
        audio_ids = get_audio_id(hrefs)   
        if audio_ids == [] :
            continue
        for id in audio_ids:
            base_url = f'https://static.seekingalpha.com/cdn/s3/transcripts_audio/{id}.mp3'
            download_audio(base_url)
            #sleep before each download
            time.sleep(5)
        

    
if __name__ == '__main__':
    main()