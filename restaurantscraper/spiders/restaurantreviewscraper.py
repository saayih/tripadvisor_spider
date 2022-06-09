# 9th June, 2022
# Ulugbek Khamdamov
# GIST, South Korea

import scrapy
import csv
import time
from scrapy.selector import Selector

MAX_RESTAURANTS = 2  # collect information from each
MAX_REVIEWS = 1000


class RestaurantreviewscraperSpider(scrapy.Spider):
    name = 'restaurantreviewscraper'

    def start_requests(self):
        allowed_domains = ['tripadvisor.com']

        urls = [
            "https://www.tripadvisor.com/Restaurants-g186338-London_England.html",
            # "https://www.tripadvisor.in/Restaurants-g186220-Bristol_England.html",
            # "https://www.tripadvisor.in/Restaurants-g187069-Manchester_Greater_Manchester_England.html",
            # "https://www.tripadvisor.in/Restaurants-g186337-Liverpool_Merseyside_England.html",
            # "https://www.tripadvisor.in/Restaurants-g294197-Seoul.html",
            # "https://www.tripadvisor.in/Restaurants-g297884-Busan.html",
            # "https://www.tripadvisor.in/Restaurants-g297889-Incheon.html",
            # "https://www.tripadvisor.in/Restaurants-g297887-Daejeon.html"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def __init__(self):
        self.restaurants_scraped = 0

    def parse(self, response):

        restaurants = response.xpath('//*[@class="bHGqj Cj b"]')
        for restaurant in restaurants:
            res_url = ('https://www.tripadvisor.com%s' % \
                       restaurant.xpath('@href').extract_first())
            fin_url = res_url.split('Reviews')
            for x in range(1,10):
                final_url = fin_url[0] + 'Reviews'+ f'-or{x}0'
                yield scrapy.Request(final_url, callback=self.parse_restaurant)

    def parse_restaurant(self, response):
        sel = Selector(response)
        rest_name = sel.xpath('//h1/text()').extract()[1]


        city = response.xpath('//*[@id="taplc_trip_planner_breadcrumbs_0"]/ul/li[5]/a/span/text()').extract_first()
        country = response.xpath('//*[@id="taplc_trip_planner_breadcrumbs_0"]/ul/li[3]/a/span/text()').extract_first()

        # extract cuisine info

        excellent_count = response.xpath('//*[@id="taplc_detail_filters_rr_resp_0"]/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[1]/span[2]/text()').extract_first()
        good_count = response.xpath('//*[@id="taplc_detail_filters_rr_resp_0"]/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/span[2]/text()').extract_first()
        average_count = response.xpath('//*[@id="taplc_detail_filters_rr_resp_0"]/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[3]/span[2]/text()').extract_first()
        poor_count = response.xpath('//*[@id="taplc_detail_filters_rr_resp_0"]/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[4]/span[2]/text()').extract_first()
        terrible_count = response.xpath('//*[@id="taplc_detail_filters_rr_resp_0"]/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[5]/span[2]/text()').extract_first()

        review_file = "review_data.csv"
        reviews = response.xpath('//*[@class="partial_entry"]')
        rev_text = ""
        count = 0
        with open(review_file, 'a', newline='') as f:
            review_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for review in reviews:
                count = count + 1
                rev_text = review.xpath(".//text()").extract_first()
                if review.xpath(".//span[@class='postSnippet']/text()").extract_first() != None:
                    rev_text = rev_text + review.xpath(".//span[@class='postSnippet']/text()").extract_first()
                rev_text.replace("...", " ")
                rev_text = rev_text + "\n"
                review_writer.writerow([rest_name, rev_text])



        filename = "restaurant_data.csv"


        with open(filename, 'a', newline='') as f:
            res_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            res_writer.writerow([rest_name,city,country,excellent_count, good_count, average_count,poor_count,terrible_count])



