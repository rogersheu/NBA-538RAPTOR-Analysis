import pandas as pd
from transfer_data import *
from csv_functions import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

fileName = 'C:/Users/Roger/Documents/GitHub/RAPTOR-Delta/data/RAPTOR_preseason_predictions_2022.csv'
shortDate = datetime.today().strftime('%Y-%m-%d')

def get_preseason_RAPTOR():
    #reset_csv(fileName)
    #write_to_csv(fileName, ['Name', 'Category','Preseason RAPTOR Offensive +/-','Preseason RAPTOR Defensive +/-','Preseason RAPTOR Total +/-','Preseason RAPTOR WAR'])
    df = pd.read_csv(f"C:/Users/Roger/Documents/GitHub/RAPTOR-Delta/data/dailyRAPTOR/RAPTORratings_{shortDate}.csv", engine = 'python')
    playerNames = list(df['Name'])


    existing_df = pd.read_csv(fileName, engine = 'python')
    existing_names = list(existing_df['Name'])

    for name in playerNames:
        if name in existing_names:
            continue
        else:
            try:
                get_player_stats(name)
            except Exception:
                continue
    



def get_player_stats(name):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    URLname = name.replace(" ", "-").replace(".", "").replace("'", "").lower()
    driver = webdriver.Chrome(executable_path = 'C:/Users/Roger/Documents/env/chromedriver_win32/chromedriver.exe', options=options)
    
    driver.get(f"https://projects.fivethirtyeight.com/2022-nba-player-projections/{URLname}/")            
    offensive_plusminus = driver.find_element(By.XPATH, "/html/body/article/div/div[5]/div[1]/div/div/table[1]/tbody/tr[1]/td[6]").text
    defensive_plusminus = driver.find_element(By.XPATH, "/html/body/article/div/div[5]/div[1]/div/div/table[1]/tbody/tr[4]/td[6]").text
    total_plusminus = driver.find_element(By.XPATH, "/html/body/article/div/div[5]/div[1]/div/div/table[1]/tbody/tr[7]/td[6]").text
    WAR = driver.find_element(By.XPATH, "/html/body/article/div/div[5]/div[1]/div/div/table[2]/tbody/tr[1]/td[6]").text
    category = driver.find_element(By.XPATH, "/html/body/article/div/div[4]/div[2]/div[1]/div[1]/div/div[1]/div[2]/div/span").text
    write_to_csv(fileName, [name, category, offensive_plusminus, defensive_plusminus, total_plusminus, WAR])


def sort_by_last_name(fileName): #Assumes a column contains names
    df = pd.read_csv(fileName, engine = 'python')
    df.sort_values(by='Name', ascending = True, inplace = True)
    df.to_csv(fileName, index = False)


def main():
    get_preseason_RAPTOR()
    sort_by_last_name(fileName)

if __name__ == '__main__':
    main()