# import necessary modules
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# import GlassdoorScraper.config
from .config import search_company_url

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 


# CREATING CHROME DRIVER
class Create_driver():

    def __init__(self, glassdoor_login_url, path_to_driver):
        self.url = glassdoor_login_url
        self.chrome_driver_path = path_to_driver

    def add_chrome_options(self):
        # Create chrome options instance
        chrome_options = webdriver.ChromeOptions()

        # Update Chrome options
        chrome_options.add_argument("--window-size=1920,1080")
        # chrome_options.add_argument('--ignore-certificate-errors')
        # chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--start-maximized")
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')
        return chrome_options
    
    def get_driver(self):
        # set up webdriver and navigate to Glassdoor website
        # CREATE URL STRING
        login_url = self.url

        # CREATE CHROME OPTIONS
        chrome_options = self.add_chrome_options()
        path_to_chromedriver = self.chrome_driver_path

        # CREATE BROWSER INSTANCE
        print("CREATING BROWSER INSTANCE.........")
        chrome_driver = webdriver.Chrome(path_to_chromedriver, options=chrome_options)
        chrome_driver.wait = WebDriverWait(chrome_driver, 10)
        chrome_driver.get(login_url)
        print("\nBROWSE FOR URL : {} READY".format(login_url))

        return chrome_driver


# SEARCHING FOR LOGIN FIELD
def login_into_glassdoor(chrome_driver, username, password):
# def login_into_glassdoor(login_url, chrome_driver, path_to_driver, username, password):
    print("\nLogin Using Gmail")
    i = 0
    try:
        print("\nAttempting to login into GlassDoor...")
        i += 1
        user_field = chrome_driver.find_element(By.ID,"inlineUserEmail")
        time.sleep(1)
        user_field.send_keys(username)
        user_field.send_keys(Keys.TAB)
        user_field.send_keys(Keys.ENTER)
        time.sleep(1)
        pw_field = chrome_driver.find_element(By.ID,"inlineUserPassword")
        pw_field.send_keys(password)
        pw_field.send_keys(Keys.TAB)
        pw_field.send_keys(Keys.TAB)
        pw_field.send_keys(Keys.ENTER)
                       
        print("Login successfully") 
    
    except TimeoutException:
        print("TimeoutException! Email/password field or login button not found on glassdoor.com")

    return chrome_driver

# GET REVIEW PAGE
def get_review_page(chrome_driver, company_name):
# def get_review_page(login_url, path_to_driver,chrome_driver, company_name):
    i=0
    chrome_driver.get(search_company_url+company_name)
    print("searching for ",company_name," company")
    time.sleep(2)
    i+=1
    try:       
        # CLICK THE COMPANY WHICH APPEARS FIRST
        continue_company_search = chrome_driver.find_element(By.XPATH, ".//*[@data-test='company-tile']").click()     # gives the company which appears first
        # continue_company_search = chrome_driver.find_element(By.CSS_SELECTOR,".css-1wh1oc8")
        # continue_company_search = chrome_driver.find_element_by_xpath(".//*[@id='Discover']/div/div/div[1]/div[1]/div[1]/a[1]").click()
        print("Company found !!")

        # SERCHING FOR REVIEW PAGE OF THE COMPANY
        print("searching for review page") 
        time.sleep(2)
        company_review = chrome_driver.find_element(By.XPATH, ".//*[@id='EIProductHeaders']/div/a[1]").click()   # company review BUTTON
        print("Wellcome to the review page!!!")

        # company_review = chrome_driver.find_element(By.CSS_SELECTOR, "a.eiCell.cell.reviews")
        # company_review.click()   # company review BUTTON
        # company_review = chrome_driver.find_element(By.CSS_SELECTOR, ".align-items-center") 
        # company_review.click()
        # print("Wellcome to the review page!!!")

    except Exception as e:
        print("---" * 40)
        print("FAILED TO GETTING REVIEW PAGE, TRYING AGAIN")
        print(e)
        chrome_driver.quit()
        i += 1
        print("ATTEMPT COUNT : ", i)
        # chrome_driver = Create_driver(login_url, path_to_driver).get_driver()
        chrome_driver = get_review_page(chrome_driver, company_name)
        print("---" * 40)

    # return chrome_driver
    # except:
    #     print("FAILED TO LINK ON COMAPNY PAGE")    
    

# SEARCHING FOR NUMBER OF PAGES AVAILABLE
def review_count(chrome_driver):
    try: 
        page_source = chrome_driver.page_source
        soup = BeautifulSoup(page_source)
        string_count = soup.find_all('div', {'class' : 'count'})[1].text
        # search for review string
        review_string = string_count.replace('k', '000').replace('K', '000')
        print(review_string)
        total_reviews = int(review_string)   # total reviews available at company review page
        pages = round(total_reviews/10)   # total pages
        print("\nTotal pages are: ", pages)
        print("\n")
        return(pages)  
        # i += 1
        # SEARCH FOR NUMBER OF REVIEWS STRING
        # string = chrome_driver.find_element(By.CSS_SELECTOR, "div.paginationFooter")
        # string = chrome_driver.find_element(By.CSS_SELECTOR, ".paginationFooter")    
         
        # r_string = string.text
        # print (string)  
        # review_string = (r_string.split(' '))
        # total_reviews = int(review_string[5].replace(',',''))   # total reviews available at company review page
        # pages = round(total_reviews/10)   # total pages
        # print("Total pages are: ", pages)
        
        # return pages

    except:
        print('Error! string which contain the counts of review | NOT found.')


# SCRAPER CODE
def glassdoor_scraper(chrome_driver, pages):
    all_review_data = []
    page_source = chrome_driver.page_source
    soup = BeautifulSoup(page_source)
    # review_link = soup.find('a', {'data-test':'EiNavCondensed'})['href']
    review_link = soup.find('a', {'data-test' : 'ei-nav-reviews-link'})['href']
    review_link = "https://www.glassdoor.com" + review_link
    print("LINK : ", review_link)
    print("Total Pages : ", pages)
    for i in range(1,pages+1):
        
        print("Page : ", i)
        page_link = "_P"+str(i)+".htm"        
        page_review_link = review_link.replace('.htm','') + page_link
        print("SCRAPPING FOR .....REVIEW PAGE LINK : ", page_review_link)
        chrome_driver.get(page_review_link)    
        
        page_review_source = chrome_driver.page_source
        pr_soup = BeautifulSoup(page_review_source)
        
        # SEARCHING FOR REVIEW_FEED
        print("---"*30)
        empReviews_Feeds = pr_soup.find_all('li', {'class' : 'noBorder empReview cf pb-0 mb-0'})
        print("REVIEW FOUND ON PAGE :", len(empReviews_Feeds))
        try:
            for empReviews in empReviews_Feeds:
                try:
                    #print("-------------\n")
                    emp_id = empReviews['id']
                    #print("REVIEWER ID :", emp_id)
                    review_title = empReviews.find('h2').text
                    review_link_ = empReviews.find('a')['href']
                    #print("REVIEW LINK : ", review_link_)
                    review_details = empReviews.find('span', {'class' : 'common__EiReviewDetailsStyle__newUiJobLine'}).text
                    review_time = review_details.split('-')[0]
                    reviewer_info = review_details.split('-')[1].replace('\xa0', '')
                    rating_ = empReviews.find('span',{'class':'ratingNumber mr-xsm'}).text
                    #print("REVIEW RATING :", rating_)
                    #print("REVIEW TIME :", review_time.strip())
                    #print("REVIEW TITLE :", review_title.strip())
                    #print("REVIEWER INFO :", reviewer_info.strip())
                    pros_ = empReviews.find('span', {'data-test' : 'pros'}).text
                    pros_ = pros_.replace('\xa0', '')
                    #print("PROS :", pros_)
                    cons_ = empReviews.find('span', {'data-test' : 'cons'}).text
                    cons_ = cons_
                    #print("CONS :", cons_)

                    data = {
                        'comment_id': emp_id,
                        'review_link' : review_link_,
                        'review_title' : review_title,
                        'review_rating' : rating_,
                        'emp_info' : reviewer_info ,
                        'time': review_time.strip(),
                        'pros': pros_,
                        'cons': cons_,
                        'text': pros_ + cons_
                    }
                    all_review_data.append(data)
                    
                except Exception as e:
                    print(e)
                    continue
                    
            time.sleep(2)
            #print("---"*30)
        except:
            pass  
    return all_review_data

                   