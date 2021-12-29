import pandas as pd
from transfer_data import *
from csv_functions import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

shortDate = datetime.today().strftime('%Y-%m-%d')
# shortDate_nodash = shortDate.replace("-","")
dir = ("C:/Users/Roger/Documents/GitHub/RAPTOR-Delta/data/dailyRAPTOR")
fileName = f'{dir}/RAPTORratings_{shortDate}.csv'

def current_RAPTOR_by_team():
    reset_csv(fileName)
    write_to_csv(fileName, ['Name', 'Current Offensive +/-', 'Current Defensive +/-'])
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path = 'C:/Users/Roger/Documents/env/chromedriver_win32/chromedriver.exe', options=options)
    driver.get(f"https://projects.fivethirtyeight.com/2022-nba-predictions/")

    
    teamList = []

    for i in range(1,31):
        teamName = driver.find_element(By.XPATH, f"/html/body/article/div[2]/main/div[1]/div/div[1]/table/tbody/tr[{i}]/td[4]/a").text
        teamList.append(teamName.replace(" ", "-").lower())
    
    for team in teamList:
        driver.get(f"https://projects.fivethirtyeight.com/2022-nba-predictions/{team}")
        player_count = len(driver.find_elements(By.XPATH, "/html/body/article/div[2]/main/div[3]/div/div[2]/div[2]/table/tbody/tr"))
        for index in range(1, player_count+1):
            if driver.find_element(By.XPATH, f"/html/body/article/div[2]/main/div[3]/div/div[2]/div[2]/table/tbody/tr[{index}]").get_attribute("class") == "overall":
                break
            name = driver.find_element(By.XPATH, f"/html/body/article/div[2]/main/div[3]/div/div[2]/div[2]/table/tbody/tr[{index}]/td[1]").text.replace("*", "")
            offensive_rating = driver.find_element(By.XPATH, f"/html/body/article/div[2]/main/div[3]/div/div[2]/div[2]/table/tbody/tr[{index}]/td[9]/div").text
            defensive_rating = driver.find_element(By.XPATH, f"/html/body/article/div[2]/main/div[3]/div/div[2]/div[2]/table/tbody/tr[{index}]/td[10]/div").text
            write_to_csv(fileName, [name, offensive_rating, defensive_rating])

    sort_by_last_name(fileName)
    combine_with_preseason(fileName)

#could make argument date if necessary
def combine_with_preseason():
    dataPath = 'C:/Users/Roger/Documents/GitHub/RAPTOR-Delta/data'
    preseason_file = 'C:/Users/Roger/Documents/GitHub/RAPTOR-Delta/data/RAPTOR_preseason_predictions_2022.csv'
    df_preseason = pd.read_csv(preseason_file)

    df_curr = pd.read_csv(fileName)

    df_full = df_curr.merge(df_preseason, how = 'outer', on = 'Name', sort = True)
    df_full.to_csv(f'{dataPath}/dailyRAPTOR/fullRAPTOR_{shortDate}.csv', index = False)


def sort_by_last_name(): #Assumes a column contains names
    df = pd.read_csv(fileName, engine = 'python')
    df.sort_values(by='Name', ascending = True, inplace = True)
    df.to_csv(fileName, index = False)

def main():    
    combine_with_preseason()
    #current_RAPTOR_by_team()

if __name__ == '__main__':
    main()