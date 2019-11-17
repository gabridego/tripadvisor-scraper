import csv
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


driver = webdriver.Chrome()

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def restroScrape(url):
    driver.get(url)
    restaurantName = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[4]/div/div[1]/h1').text
    print("Starting for restaurant: {}".format(restaurantName))
    fileName = 'reviews/' + restaurantName + '.csv'
    csvFile = open(fileName, 'a+')
    csvWriter = csv.writer(csvFile)
    page = driver.find_element_by_css_selector('a.pageNum.last.taLnk')
    page_number = int(page.text) + 1
    print("Pages are {}".format(page_number - 1))

    for i in range(0, page_number):

        if check_exists_by_xpath("//span[@class='taLnk ulBlueLinks']") is True:
            # to expand the review 
            driver.find_element_by_xpath("//span[@class='taLnk ulBlueLinks']").click()
            time.sleep(5)

        container = driver.find_elements_by_xpath("//div[@class='review-container']")

        num_page_items = len(container)
        for j in range(num_page_items):

            string = container[j].find_element_by_xpath(".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class")
            data = string.split("_")

            rating = int(data[3]) / 10
            print(data)

            title = container[j].find_element_by_xpath(".//span[@class='noQuotes']").text.replace("\n", "")
            print("Review Title: {}".format(title))

            date = container[j].find_element_by_xpath(".//span[@class='ratingDate']").text.replace("\n", "")
            date = date.replace('Reviewed ', '')
            print("Review Date is : {}".format(date))

            review = container[j].find_element_by_xpath(".//p[@class='partial_entry']").text.replace("\n", "")
            print("Review is : {}".format(review))

            print("\n")
            csvWriter.writerow([rating, date, review, title, "TripAdvisor"])

        
        xpath = '/html/body/div[2]/div[2]/div[2]/div[5]/div/div[1]/div[3]/div/div[5]/div/div[14]/div/div/a[2]'
        if not check_exists_by_xpath(xpath):
            xpath = '/html/body/div[2]/div[2]/div[2]/div[5]/div/div[1]/div[3]/div/div[5]/div/div[15]/div/div/a[2]'

        if i == page_number - 2:
            return
        driver.find_element_by_xpath(xpath).click()
        time.sleep(5)
    driver.back()

driver.get("https://www.tripadvisor.in/Restaurants-g659786-Siliguri_Darjeeling_District_West_Bengal.html")
restaurants = driver.find_elements_by_class_name('restaurants-list-ListCell__cellContainer--2mpJS')

page = driver.find_element_by_xpath('//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/div/a[6]')
page_number = int(page.text) + 1
print("There are {} pages".format(page_number - 1))

for i in range(0, page_number):

    for j in range(len(restaurants)):
        url = restaurants[j].find_element_by_xpath(".//a[@class='restaurants-list-ListCell__restaurantName--2aSdo']").get_attribute("href")
        try:
            restroScrape(url)
        except Exception as e:
            print(e)
        
        driver.get("https://www.tripadvisor.in/Restaurants-g659786-Siliguri_Darjeeling_District_West_Bengal.html")
        restaurants = driver.find_elements_by_class_name('restaurants-list-ListCell__cellContainer--2mpJS')
        time.sleep(10)
    
    xpath = '/html/body/div[4]/div[3]/div[2]/div[2]/div[2]/div/div[2]/div[5]/div[2]/div[5]/div[2]/div/a[2]'   
    if not check_exists_by_xpath(xpath):
        xpath = '/html/body/div[4]/div[3]/div[2]/div[2]/div[2]/div/div[2]/div[5]/div[2]/div[5]/div[2]/div/a'
        
    try:
        driver.find_element_by_xpath(xpath).click()
    except Exception as e:
        print(e)

time.sleep(25)

driver.close()