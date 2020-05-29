# Bbc_Scraping
 BBC News data Collect and Store

# Details
  * This Python Application crawls BBC online news website using the SCRAPY crawler framework .
  * This appliction cleans the news articles to obtain only information relevant to the news story, e.g. News URL, News Text, News Headline, Author.
  * News articles crawled are stored in [MongoDB Atlas](https://www.mongodb.com/cloud/atlas), 
  * An APIs are provided, to access the data stored at the mongo database.
    *   Using the search REST API, end user can fetch:
          * All the news articles in data base.
          * News Articles with a given keyword in News Text.
          * News Articles with a given keyword in News Headline.
# Directory Structure:
   * Directory bbcnews:
      -   Contains the Scrapy Spider for BBC News Website.
   * Directory Log:
      - This directory is created at runtime and contains log file of crawler.
   * Directory Output:
      - This directory is also created at runtime.
      - It contains the output json file including the data cawled from BBC News Website.
      - It contains a file 'visited_urls.txt', which is dynamically created. It's used to avoid scraping the same URL.
   * Directory API:
      - This directory contains script bbc_apisearsh.py provides implementation of search REST API, for News Crawler.
      - Three search APIs are implemented, which are:
          - For fetching all the news articles in MongoDb.
                         (Example API Call: <ROOT URL>/news )
          - For fetching news articles from MongoDb, with a given keyword in News article.
                         (Example API Call: <ROOT URL>/newstext/<string:keyword>
          - For fetching news articles from MongoDb, with a given keyword in News Title.
                         (Example API Call: <ROOT URL>/newstitl/<string:keyword> 
   * File bbcnewRules.json:
      - In this file rules are defined for crawling BBC News Website.
      - End-User can edit this file as per requirement.

# Execution:
1. To execute BBC News Website Crawler, execute command scrapy crawl bbcdata.
2. To use REST APIs:
   - Change to directory RestAPI and execute command python bbc_apisearsh.py
   - As long as this script is executing, end user can use Search REST API to get the desired data from hosted MongoDB Atlas
