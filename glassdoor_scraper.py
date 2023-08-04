import os
import sys
import pandas as pd
# import config
# import utils
from .config import glassdoor_login_url, username, password, path_to_driver
from .utils import login_into_glassdoor, review_count, get_review_page, Create_driver, glassdoor_scraper

class GlassdoorDataScraper():
    def __init__(self, path_to_driver):
        self.url = glassdoor_login_url
        self.path_to_driver = path_to_driver
        self.driver = Create_driver(self.url, self.path_to_driver).get_driver()     
        
        # GET LOGED IN DRIVER(BROWSER) INSTANCE
        self.chrome_driver = login_into_glassdoor(self.driver, username, password)

    def scrap_by_company_name(self, company_name):
        # GET REVIEW PAGE OF THE COMPANY
        # get_review_page(self.url, self.driver,self.path_to_driver, company_name) 
        get_review_page(self.chrome_driver, company_name) 
        # GET THE NUMBER OF REVIEW PAGES AVAILABLE TO SCRAP
        pages = review_count(self.driver)
        # GET REVIEWS
        # glassdoor_review = glassdoor_scraper(self.driver, pages)
        glassdoor_review = glassdoor_scraper(self.chrome_driver, pages)
        # SAVING DATA TO CSV
        print("||Saving the Scraped Data||")
        df_reviews = pd.DataFrame(glassdoor_review)
        df_reviews.to_csv(company_name + ".csv", index=False)
        # self.driver.quit()

        return glassdoor_review
    
if __name__ == "__main__":
    path_to_driver = "./chromedriver.exe"
    company_name = "Scanta"
    all_reviews = GlassdoorDataScraper(path_to_driver).scrap_by_company_name(company_name)
    
    # # SAVING DATA TO CSV
    # print("||Saving the Scraped Data||")
    # df_reviews = pd.DataFrame(all_reviews)
    # df_reviews.to_csv(company_name + ".csv", index=False)
    # df_reviews
