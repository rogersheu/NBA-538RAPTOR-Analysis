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