# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapeEraItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# coursera spider item
class CourseraItem(scrapy.Item):
    job_title = scrapy.Field()
    company_name = scrapy.Field()
    location = scrapy.Field()
    about_company = scrapy.Field()
    job_overview = scrapy.Field()
    company_overview = scrapy.Field()
    responsibilities = scrapy.Field()
    basic_qualifications = scrapy.Field()
    preferred_qualifications = scrapy.Field()
    apply_link = scrapy.Field()