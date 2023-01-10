import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


possible_countries = set(['Botswana', 'Eswatini', 'Kenya', 'Lesotho', 'South Africa', 'Uganda', 'Bangladesh', 'Bhutan', 'Christmas Island', 
'India', 'Indonesia', 'Japan', 'Malaysia', 'Singapore', 'Sri Lanka', 'Thailand', 'Ireland', 'Isle of Man', 'Jersey', 'Malta', 
'United Kingdom', 'US Virgin Islands', 'Australia', 'New Zealand', 'Ghana', 'Madagascar', 'Nigeria', 'Rwanda', 'Senegal', 'Tunisia', 
'Cambodia', 'Israel', 'Jordan', 'Kyrgyzstan', 'Laos', 'Mongolia', 'Philippines', 'Russia', 'South Korea', 'Taiwan', 
'United Arab Emirates', 'Vietnam', 'Albania', 'Andorra', 'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Czech Republic', 'Denmark', 
'Estonia', 'Faroe Islands', 'Finland', 'France', 'Germany', 'Gibraltar', 'Greece', 'Hungary', 'Iceland', 'Italy', 'Latvia', 
'Lithuania', 'Luxembourg', 'Monaco', 'Montenegro', 'Netherlands', 'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 
'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'Ukraine', 'Canada', 'Curaçao', 
'Dominican Republic', 'Greenland', 'Guatemala', 'Mexico', 'Puerto Rico', 'United States', 'American Samoa', 'Guam', 
'Northern Mariana Islands', 'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Peru', 'Uruguay'])

def findLinkByHref(driver, value):
    elements = driver.find_elements(By.TAG_NAME, "a")
    for e in elements:
        if e.get_attribute("href") == value:
            return e

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(service=Service(PATH))

driver.get("https://geohints.com/")
driver.maximize_window()
main = driver.find_element(By.CLASS_NAME, "inner")


def by_driving_side():
    global possible_countries
    global main
    driving_side = input("What side do the cars drive on? \n").upper()
    link = findLinkByHref(main, "https://geohints.com/Driving.html")
    link.click()

    try:
        body = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        text = body.text
        list = text.split("\n\n")
        if driving_side == "L":
            sublist = list[1].split(": ")
            leftover_countries = sublist[1].split(", ")
        else:
            sublist = list[2].split("\n")
            sublist2 = sublist[0].split(": ")
            leftover_countries = sublist2[1].split(", ")
        print(leftover_countries)

        possible_countries = possible_countries & set(leftover_countries)

    finally:
        driver.back()


def by_gas_station():
    global possible_countries
    global main
    # Get gas station names
    gas_stations = []
    while(True):
        name = input("Enter gas station company (enter 0 to stop): \n").lower()
        if name == "0":
            break
        gas_stations.append(name)
    print(gas_stations)

    # Generate dictionary from website
    link = findLinkByHref(main, "https://geohints.com/Companies.html")
    link.click()
    try:
        body = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        inner = body.find_element(By.CLASS_NAME, "inner")
        link2 = findLinkByHref(inner, "https://geohints.com/fuelStations.html")
        link2.click()
        try:
            body2 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            list = body2.text.split("\n\n\n\n")
            #print(list[0])
            sublist = list[0].split("here.")
            #print(sublist)
            station_list = sublist[1].split("\n\n\n")
            #print(sublist2)
            station_list[0] = station_list[0].replace("\n\n", "")
            station_dict = {}
            for i in range(len(station_list)):
                station_list[i] = station_list[i].split(" - ")
                station_list[i][0] = station_list[i][0].lower()
                station_list[i][1] = station_list[i][1].split(", ")
                #print(name_dict[i])

                #Get rid of bracketed notes for countries
                for j in range(len(station_list[i][1])):
                    if '(' in station_list[i][1][j]:
                        station_list[i][1][j] = station_list[i][1][j][0:station_list[i][1][j].find('(') - 1]

                station_dict[station_list[i][0]] = station_list[i][1]
            
        finally:
            driver.back()
    finally:
        driver.back()

    for station in gas_stations:
        possible_countries = possible_countries & set(station_dict.get(station))
    
by_driving_side()
print(possible_countries)
by_gas_station()
print(possible_countries)
