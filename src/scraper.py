from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from transfer_data import *
from datetime import datetime
from csv_functions import make_dir_if_nonexistent, reset_csv, write_to_csv


# Have: RAPTOR of current season
# To do:
#   Automate grabbing the main table in https://projects.fivethirtyeight.com/nba-player-ratings/
#   One big grab at all the players' pre-season projections.
#   https://projects.fivethirtyeight.com/2022-nba-player-projections/{firstname}-{lastname}/


shortDate = datetime.today().strftime('%Y-%m-%d')
shortDate_nodash = shortDate.replace("-","")

mkdir = ("C:/Users/Roger/Documents/GitHub/RAPTOR-Delta/data")
make_dir_if_nonexistent(mkdir)




def preseason_scraper():
    pass



def active_scraper():
    fileName = (f"{mkdir}/RAPTORdata_{shortDate}.csv")

    driver = webdriver.Chrome(executable_path = 'C:/Users/Roger/Documents/env/chromedriver_win32/chromedriver.exe')
    driver.get("https://projects.fivethirtyeight.com/nba-player-ratings/")

    dataTable = driver.find_elements(By.XPATH, '/html/body/div[3]/table/tbody')

    for item in dataTable:
        print(item.text)
        #write_to_csv(fileName, df)
    



    driver.close()


    # raptorPage = requests.get('https://projects.fivethirtyeight.com/nba-player-ratings/')
    # raptorSoup = BeautifulSoup(raptorPage.content, "html.parser", from_encoding="utf-8")
    # raptorTable = raptorSoup.find('div', class_ = 'container').find('table')
    
    # print(raptorTable)
    # raptorCols = raptorTable.find_all("td")


    

def main():
    active_scraper()

if __name__ == "__main__":
    main()
