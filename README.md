# TripAdvisor scraper for Italian hotels #
Scrape TripAdvisor for reviews of Italian hotels with rating labels. Marks a review as positive if it has at least three stars, negative otherwise.
Updated on January 2020.
## Dependencies ##
- [Selenium](https://pypi.org/project/selenium/)
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) or [geckodriver](https://github.com/mozilla/geckodriver/releases/tag/v0.26.0)
## Usage ##
Open the file and specify the path to your webdriver.
To run:
```
python tripAdvisorScraper.py
```
To change hotel, open the file and change the url in main().
To limit the number of scraped reviews, edit max_rev.
Augment the sleep time if you have a slow internet connection.

The .csv file contains an output example.