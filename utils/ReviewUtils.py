import requests
from time import sleep
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
class ReviewUtils:
    # Initializing the review utils class
    def __init__(self, username, n_pages):
        self.username = username
        self.endpoint = None
        self.n_pages = n_pages
        self.user_reviews_df = None
        self.scrape_success = None
    def getReviewEndPoint(self):
        # Getting the review endpoint required
        url = "https://www.trustpilot.com/search?query={}".format(self.username)
        response = get(url)
        preferred_url = "{}.com".format(self.username.lower())
        html_soup = BeautifulSoup(response.text, 'html.parser')
        review_containers = html_soup.find_all('a', class_ = 'search-result-heading')
        for i in range(len(review_containers)):
            if preferred_url in review_containers[i]['href']:
                self.endpoint = review_containers[i]['href']
        try:
            self.endpoint = review_containers[0]['href']
        except:
            self.endpoint = None

    def scrape_reviews(self, sleep_time = 0.3): 
        # Scraping the reviews with the endpoint acquired
        #print("This is the endpoint{}".format(self.endpoint))
        self.PATH = 'https://www.trustpilot.com{}?page='.format(self.endpoint)

        #print("This is the path{}".format(self.PATH))
        names = []
        ratings = []
        headers = []
        reviews = []
        locations = []
        try:
            # Trying to save the reviews
            for p in range(self.n_pages):
                sleep(sleep_time)
                final_path = "{}{}".format(self.PATH,p)

                #print(final_path)
                
                http = requests.get(final_path)
                bsoup = BeautifulSoup(http.text, 'html.parser')

                review_containers = bsoup.find_all('div', class_ = 'review-content__body')
                user_containers = bsoup.find_all('div', class_ = 'consumer-information__name')
                rating_container = bsoup.find_all('div',class_ = "star-rating star-rating--medium")
                location_container = bsoup.find_all('div',class_ = "consumer-information__location")


                for x in range(len(review_containers)):

                    review_c = review_containers[x]
                    try:
                        reviews.append(review_c.p.text)
                        headers.append(review_c.h2.a.text)
                    except:
                        reviews.append("No review")
                        headers.append("No review")
                    try:
                        reviewer = user_containers[x]
                        names.append(reviewer.text)
                    except:
                        names.append("Name not found")
                    try:
                        rating = rating_container[x].img['alt']
                        ratings.append(rating)
                    except:
                        ratings.append("Ratings not found")
                    try:
                        location = location_container[x]
                        user_loc = location.span.text
                        locations.append(user_loc)
                    except:
                        locations.append("Not Found")

                rev_df = pd.DataFrame(list(zip(headers, reviews, ratings, names,locations )),
                            columns = ['Header','Review','Rating', 'Name','Location'])
                #print(rev_df)
                rev_df['Header'] = rev_df['Header'].apply(ReviewUtils.clean_string)
                rev_df['Review'] = rev_df['Review'].apply(ReviewUtils.clean_string)
                rev_df['Name'] = rev_df['Name'].apply(ReviewUtils.clean_string)
                rev_df['Location'] = rev_df['Location'].apply(ReviewUtils.clean_string)
                scrape_success = 1
        except Exception as e:
            # If the endpoint was incorrect it should lead to an error
            print(e)
            scrape_success = 0
            rev_df = "Error"
            self.user_reviews_df = rev_df
            self.scrape_success = scrape_success
            
        # Setting the datafame with the reviews collected
        self.user_reviews_df = rev_df
        
        # Setting the scrape_success 0 = unsuccessful scraping, 1 = successfully scraped
        self.scrape_success = scrape_success
        
    @staticmethod
    def clean_string(text):
        # Static preprocessing function to clean the reviews
        text = text.replace("\n", "", 2)
        text = text.replace(' ', '')
        return text
