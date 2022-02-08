# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 18:10:59 2022

@author: cns

Responding to UpWork post

I need all of the result subpages from this website:

https://www.bcorporation.net/en-us/find-a-b-corp/search?refinement=countries%3DUnited%20Kingdom&refinement=countries%3DAustralia&refinement=countries%3DBelgium&refinement=countries%3DCanada&refinement=countries%3DChina&refinement=countries%3DDenmark&refinement=countries%3DFrance&refinement=countries%3DGermany&refinement=countries%3DIreland&refinement=countries%3DItaly&refinement=countries%3DNetherlands%20The&refinement=countries%3DMexico&refinement=countries%3DNew%20Zealand&refinement=countries%3DPortugal&refinement=countries%3DSpain&refinement=countries%3DSweden&refinement=countries%3DSwitzerland&refinement=countries%3DUnited%20States

to be scraped into .csv with such columns:
ID || Headquarters || Certified Since || Sector || Countries of Operations || Website || Descripton

"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
    
import pandas as pd
import os

def scrape_links (filepath_chromedriver, url, n_pages):
    
    # Function to scrape the list of profile links required to go get the actual information required
    ser = Service(filepath_chromedriver)
    op = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ser, options=op)
    driver.get("https://www.bcorporation.net/en-us/find-a-b-corp/search?refinement=countries%3DUnited%20Kingdom&refinement=countries%3DAustralia&refinement=countries%3DBelgium&refinement=countries%3DCanada&refinement=countries%3DChina&refinement=countries%3DDenmark&refinement=countries%3DFrance&refinement=countries%3DGermany&refinement=countries%3DIreland&refinement=countries%3DItaly&refinement=countries%3DNetherlands%20The&refinement=countries%3DMexico&refinement=countries%3DNew%20Zealand&refinement=countries%3DPortugal&refinement=countries%3DSpain&refinement=countries%3DSweden&refinement=countries%3DSwitzerland&refinement=countries%3DUnited%20States")

    # Create empty list of links
    final_links_list = []
    
    # Iterate through desired n_pages
    for page in n_pages:
        
        # Fetch the profile links on that page, append it to the final links list page
        current_page_links = driver.find_elements(By.CSS_SELECTOR, "[data-testid=profile-link]")
        for link in current_page_links: final_links_list.append(link.get_attribute('href'))
        
        # Button click to go through to the next page. Wait for next page to load
        time.sleep(1)
        driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/main/div[1]/div[2]/div/div[2]/div[3]/nav/button[2]').click()
        time.sleep(1)
        
        # Close the driver session after getting links from last page
        if page == len(n_pages):
            driver.quit()
        
    return final_links_list

def scrape_profile_info(filepath_chromedriver, link):
    
    # Open up a driver session to the website
    ser = Service('C:/Users/cns/Documents/PythonCode/selenium_chrome_driver/chromedriver')
    op = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ser, options=op)
    driver.get(f"{link}")
        
    # Get the summary info, split string by "\n". THen fetch summary paragraph and append to the list
    ID = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/main/div[1]/div[3]/div[3]/h1').text
    Headquarters = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/main/div[1]/div[3]/div[2]/div[1]/div/p').text
    Certified = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/main/div[1]/div[3]/div[2]/div[2]/div/p').text
    Sector = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/main/div[1]/div[3]/div[2]/div[3]/div/p').text
    Countries = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/main/div[1]/div[3]/div[2]/div[4]/div/div').text
    Website = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/main/div[1]/div[3]/div[2]/div[5]/div/a').text
    Descripton = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/main/div[1]/div[3]/div[3]/p').text
    
    driver.quit()
    
    profile_results = [ID, Headquarters, Certified, Sector, Countries, Website, Descripton]
    return pd.DataFrame([profile_results], columns=["ID", "Headquarters", "Certified", "Sector", "Countries", "Website", "Descripton"])
    
def main (url, working_dir, n_pages, filepath_chromedriver):
    
    list_of_links = scrape_links(filepath_chromedriver, url, n_pages)
    
    results_df = pd.DataFrame()
    
    for link in list_of_links:
        results_df = results_df.append(scrape_profile_info(filepath_chromedriver=filepath_chromedriver, 
                                                           link=link), ignore_index=True)
    
    results_df.to_csv(f"{working_dir}example_companies_list.tsv", sep="\t", index=False)
    
if __name__ == "__main__":
    
    n_pages = range(1)
    url = "https://www.bcorporation.net/"
    
    # Change to your own working_dir and filepath to webdriver for selenium
    working_dir = "C:/Users/cns/Documents/PythonCode/companies_webscraper/"
    filepath_chromedriver = 'C:/Users/cns/Documents/PythonCode/selenium_chrome_driver/chromedriver'
    
    #os.getcwd()
    os.chdir(working_dir)
    
    main(url, working_dir, n_pages, filepath_chromedriver)
