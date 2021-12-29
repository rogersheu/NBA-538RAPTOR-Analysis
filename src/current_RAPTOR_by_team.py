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
def main():    
    combine_with_preseason()
    #current_RAPTOR_by_team()

if __name__ == '__main__':
    main()