import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from entry import Entry


def findLinkByHref(driver, value):
    elements = driver.find_elements(By.TAG_NAME, "a")
    for e in elements:
        if e.get_attribute("href") == value:
            return e

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(service=Service(PATH))

driver.get("https://rateyourmusic.com/")
driver.maximize_window()

def search_for_artist(name):
    header = driver.find_element(By.ID, "page_header")
    inner = header.find_element(By.TAG_NAME, "div")
    inner2 = inner.find_element(By.CLASS_NAME, "header_search")
    inner3 = inner2.find_element(By.ID, "ui_search_frame_outer_main_search")
    inner4 = inner3.find_element(By.ID, "ui_search_frame_main_search")
    inner5 = inner4.find_element(By.CLASS_NAME, "ui_search_frame_inner")
    inner6 = inner5.find_element(By.ID, "ui_search_main_search")
    form = inner6.find_element(By.TAG_NAME, "form")
    search = form.find_element(By.TAG_NAME, "input")

    search.send_keys(name)
    search.send_keys(Keys.RETURN)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "content_wrapper_outer"))
        )
        artist = element.find_element(By.XPATH, "//tr[@class='infobox']")
        link = artist.find_element(By.XPATH, "//a[@class='searchpage']")
        print(artist.text)
        link.click()
        
        time.sleep(5)
    finally:
        return 0


def find_albums(main):
    recs = {}

    albums = main.find_element(By.XPATH, "//div[@id='disco_type_s']")
    albums_list = albums.find_elements(By.CLASS_NAME, "disco_release")

    for album in albums_list:
        rating = album.find_element(By.XPATH, "./div[3]")
        title_box = album.find_element(By.XPATH, ".//div[@class='disco_mainline']")
        title = title_box.text


        image = album.find_element(By.XPATH, "./div[@class='disco_info']/a")
        image_link = "https:" + image.get_attribute('innerHTML').split('"')[7]
        print(title + " has a rating of " + rating.text)
        if rating.text != "":
            if rating.get_attribute('class') == "disco_avg_rating enough_data":
                if len(title_box.find_elements(By.TAG_NAME, "b")) > 0 or float(rating.text) >= 3:   
                    print(title + " is RECOMMENDED")
                    print("\n")
                recs[title] = Entry(title, float(rating.text), image_link)
    return sorted(recs.items(), key=lambda x:x[1].rating, reverse=True)


def find_singles(main):
    recs = {}

    singles = main.find_element(By.XPATH, "//div[@id='disco_type_i']")
    #print(singles.text)
    singles_list = singles.find_elements(By.CLASS_NAME, "disco_release")

    for single in singles_list:
        rating = single.find_element(By.XPATH, "./div[3]")
        title_box = single.find_element(By.XPATH, ".//div[@class='disco_mainline']")
        title = title_box.text
        
        image = single.find_element(By.XPATH, "./div[@class='disco_info']/a")
        image_link = "https:" + image.get_attribute('innerHTML').split('"')[7]
        print(title + " has a rating of " + rating.text)
        if rating.get_attribute('class') == "disco_avg_rating enough_data":
            if len(title_box.find_elements(By.TAG_NAME, "b")) > 0 or float(rating.text) >= 3:
                print(title + " is RECOMMENDED")
                print("\n")
            recs[title] = recs[title] = Entry(title, float(rating.text), image_link)
    return sorted(recs.items(), key=lambda x:x[1].rating, reverse=True)


def get_recommendations():
    recs = {}
    try:
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "content_wrapper_outer"))
        )
        recs["Singles"] = (find_singles(main))
        recs["Albums"] = (find_albums(main))
    finally:
        return recs


def get_top_recs(n, recs):
    singles_list = []
    print('\nSINGLES:')
    singles = recs['Singles']
    max = min(len(singles), n)
    for i in range(max):
        print(f'{i + 1}. {singles[i][0]}, {singles[i][1].rating} Stars, image: {singles[i][1].image}')
        singles_list.append(singles[i][1])


    albums_list = []
    print('\nALBUMS: ')
    albums = recs['Albums']
    max = min(len(albums), n)
    for i in range(max):
        print(f'{i + 1}. {albums[i][0]}, {albums[i][1].rating} Stars, image: {albums[i][1].image}')
        albums_list.append(albums[i][1])

    return {"Singles": singles_list, "Albums": albums_list}



if __name__ == "__main__":
    search_for_artist("Taylor Swift")
    recs = (get_recommendations())
    print(recs)
    get_top_recs(3, recs)
