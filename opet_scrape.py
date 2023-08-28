from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
import datetime

def parse_data(table_content):

    dates = []
    kursunsuz95 = []
    motorin = []


    for i in range(int(len(table_content))):

        if len(table_content[i+1].text)==0:
            break

        prices = table_content[i+1].text[20:].split("TL/LT")

        dates.append(table_content[i+1].text[:10].replace("-","/"))

        kursunsuz95.append(float(prices[0]))

        motorin.append(float(prices[1]))

        #print(f"{i+1} is done!")

    final_df = pd.DataFrame(data={"date":dates,
                                     "kursunsuz 95":kursunsuz95,
                                     "motorin":motorin})
    
    final_df["date"] = pd.to_datetime(final_df["date"],dayfirst=True)

    
    
    return final_df



def get_data(driver,ilce, months=12):
    
    '''
    driver = current WebDriver object
    months: how many months do you want to go back
    '''


    driver.get("https://www.opet.com.tr/akaryakit-fiyatlari-arsivi")
    driver.find_element(By.XPATH,"//a[contains(text(),'tümünü reddet')]").click()


    driver.find_element(By.XPATH,"//input[@aria-label='Başlangıç Tarihi']").click()

    select = Select(driver.find_element(By.XPATH,"//select[@id='DistrictCode']"))

    select.select_by_visible_text(ilce.upper()) 
    
    for i in range(months):
        driver.find_element(By.XPATH,"//div[@aria-label='Move backward to switch to the previous month.']").click()
        time.sleep(1)


    td_buttons = driver.find_elements(By.XPATH,"//td")


    for i in range(50):
        if td_buttons[i].text == "1":
            td_buttons[i].click()
            #print(f"Uzunluk: {len(td_buttons[i].text)}  --- Text: {td_buttons[i].text}")


    for i in range(months):
        driver.find_element(By.XPATH,"//div[@aria-label='Move forward to switch to the next month.']").click()
        time.sleep(1)


    td_buttons = driver.find_elements(By.XPATH,"//td")

    today = datetime.datetime.today().day

    button_counts=0
    for i in range(len(td_buttons)):
        
        if td_buttons[i].text == str(today-1):
            button_counts += 1
            if button_counts == 2:
                td_buttons[i].click()
                break

    ara_button = driver.find_element(By.XPATH,"//button[@type='submit']")
    ara_button.click()

    time.sleep(10)

    table_contents = driver.find_elements(By.XPATH,"//tr")


    final_df = parse_data(table_contents)

    driver.quit()

    return final_df


    

# Creating Instance
option = Options()
option.add_argument("window-size=1200x600")
# Working with the 'add_argument' Method to modify Driver Default Notification
option.add_argument('--disable-notifications')

# Passing Driver path alongside with Driver modified Options
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options= option)


get_data(driver,"ŞİŞLİ",10).to_csv("gasprices.csv",index=False)

print("Everything is DONE!")