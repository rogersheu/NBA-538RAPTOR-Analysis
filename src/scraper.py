import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from transfer_data import *
from datetime import datetime
from csv_functions import make_dir_if_nonexistent, reset_csv, write_to_csv
import re


# Have: RAPTOR of current season
# To do:
#   Automate grabbing the main table in https://projects.fivethirtyeight.com/nba-player-ratings/
#   One big grab at all the players' pre-season projections.
#   https://projects.fivethirtyeight.com/2022-nba-player-projections/{firstname}-{lastname}/


shortDate = datetime.today().strftime('%Y-%m-%d')
shortDate_nodash = shortDate.replace("-","")

mkdir = ("C:/Users/Roger/Documents/GitHub/RAPTOR-Delta/data")
make_dir_if_nonexistent(mkdir)

# Capture Group 1: Name
# Capture Group 2: Team
# Capture Group 3: Position(s)
# 4: MP
# 5-7: BOX RAPTOR
# 8-10: ON/OFF RAPTOR
# 11-13: RAPTOR
# 14: RAPTOR WAR
player_regex = re.compile(r"[0-9]*\s*([a-zA-Z-'.]+ [a-zA-Z-'. ]+)(?:'21-'22) ([a-zA-Z0-9\s]+) ((?:(?:, ){0,1}(?:PG|SG|SF|PF|C))+) ([0-9,]+) ([+-]*[0-9]+.[0-9]+) ([+-]*[0-9]+.[0-9]+) ([+-]*[0-9]+.[0-9]+) ([+-]*[0-9]+.[0-9]+) ([+-]*[0-9]+.[0-9]+) ([+-]*[0-9]+.[0-9]+) ([+-]*[0-9]+.[0-9]+) ([+-]*[0-9]+.[0-9]+) ([+-]*[0-9]+.[0-9]+) ([+-]*[0-9]+.[0-9]+)")

def preseason_scraper():
    pass



def active_scraper():
    fileName = (f"{mkdir}/RAPTORdata_{shortDate}.csv")
    reset_csv(fileName)
    write_to_csv(fileName, ['Name','Team','Position(s)','MP','Box Offense','Box Defense','Box Total','OnOff Offense','OnOff Defense','OnOff Total','RAPTOR Offense','RAPTOR Defense','RAPTOR Total','RAPTOR WAR'])

    driver = webdriver.Chrome(executable_path = 'C:/Users/Roger/Documents/env/chromedriver_win32/chromedriver.exe')
    driver.get("https://projects.fivethirtyeight.com/nba-player-ratings/")

    # Minutes slider
    slider = driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/div[1]/div[3]/div[4]/input")
    
    # Targets the "Season Type" drop-down menu to the left of the minutes slider
    targetDestination = driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/div[1]/div[2]/form/select")

    # Adjust slider to minimum of 1 minute
    actions = ActionChains(driver)
    actions.click_and_hold(slider)
    actions.move_to_element(targetDestination)
    actions.release()
    actions.perform()

    # Sorts by last name
    nameforSort = driver.find_element(By.XPATH, "/html/body/div[3]/table/thead/tr[2]/th[2]")
    actions.click(nameforSort)
    actions.perform()
    dataTable = driver.find_elements(By.XPATH, '/html/body/div[3]/table/tbody')

    dataList = []

    for item in dataTable:
        dataList.append(item.text.split('\n'))

    dataList = dataList[0]

    for player in dataList:
        print(player)
        playerMatch = re.match(player_regex, player)
        name, team, position, MP = playerMatch.group(1, 2, 3, 4)
        boxOFF, boxDEF, boxTOT = playerMatch.group(5, 6, 7)
        onoffOFF, onoffDEF, onoffTOT = playerMatch.group(8, 9, 10)
        raptorOFF, raptorDEF, raptorTOT = playerMatch.group(11, 12, 13)
        war = playerMatch.group(14)
        write_to_csv(fileName, [name, team, position, MP, boxOFF, boxDEF, boxTOT, onoffOFF, onoffDEF, onoffTOT, raptorOFF, raptorDEF, raptorTOT, war])
    
    driver.close()    

def main():
    active_scraper()

if __name__ == "__main__":
    main()
