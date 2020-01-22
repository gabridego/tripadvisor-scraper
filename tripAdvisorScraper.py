import csv
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Firefox(executable_path='geckodriver.exe')
# driver = webdriver.Chrome("chromedriver.exe")


def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def hotel_scrape(url, max_rev):
    driver.get(url)
    name = driver.find_element_by_id('HEADING').text
    # print("Starting for hotel: {}".format(name))
    filename = name + '.csv'
    csvfile = open(filename, 'w', encoding='utf-8', newline='')
    csvwriter = csv.writer(csvfile)
    page = driver.find_elements_by_css_selector('a.pageNum')[-1]
    page_number = int(page.text) + 1
    tot = 0
    # print("Pages are {}".format(page_number - 1))
    csvwriter.writerow(['text', 'class'])

    for i in range(0, page_number):

        if check_exists_by_xpath("//span[@class='location-review-review-list-parts-ExpandableReview__cta--2mR2g']"):
            # to expand the review
            driver.find_element_by_xpath("//span[@class='location-review-review-list-parts-ExpandableReview__cta"
                                         "--2mR2g']").click()
            time.sleep(2)

        container = driver.find_elements_by_xpath("//div[@class='location-review-review-list-parts"
                                                  "-SingleReview__mainCol--1hApa']")

        num_page_items = len(container)
        for j in range(num_page_items):
            if tot > max_rev:
                csvfile.close()
                return

            string = container[j].find_element_by_xpath(
                ".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class")
            data = string.split("_")

            rating = int(data[3]) / 10
            if rating >= 3:
                cl = 'pos'
            else:
                cl = 'neg'
            # print(data)

            review = container[j].find_element_by_xpath(".//q[@class='location-review-review-list-parts"
                                                        "-ExpandableReview__reviewText--gOmRC']/span") \
                                                        .text.replace("\n", "")
            # print("Review is : {}".format(review))

            # print("\n")
            csvwriter.writerow([review, cl])
            tot += 1

        if i == page_number - 2:
            csvfile.close()
            return

        driver.find_element_by_css_selector('a.ui_button.nav.next.primary').click()
        time.sleep(2)

    driver.back()


def main():
    # url of hotel to scrape
    url = 'https://www.tripadvisor.it/Hotel_Review-g187855-d570594-Reviews-Hotel_Nizza-Turin_Province_of_Turin_Piedmont.html'

    # number of reviews to get, leave float('inf') to get all
    max_rev = float('inf')
    # max_rev = 50

    try:
        hotel_scrape(url, max_rev)
    except Exception as e:
        print(e)

    driver.close()


if __name__ == '__main__':
    main()