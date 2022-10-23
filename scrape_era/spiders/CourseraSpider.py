import scrapy

from ..items import CourseraItem

class CourseraSpider(scrapy.Spider):
    name = 'coursera'
    start_urls = [
        'https://boards.greenhouse.io/embed/job_board?for=coursera'
    ]

    def parse_details(self, response, apply_link):
        item = CourseraItem()
        item['job_title'] = response.xpath("//div[@id='header']/h1/text()").get()
        item['company_name'] = (response.xpath("//span[@class='company-name']/text()").get()).split('at')[1].strip()
        item['location'] = (response.xpath("//div[@class='location']/text()").get()).strip()
        item['about_company'] = response.xpath("//div[@class='content-intro']/p/text()").get()

        item['job_overview'] = response.xpath("//strong[text()[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'job overview')]]/../following-sibling::p[1]/span/text()").get()   # select based on text (case insensitive)

        item['company_overview'] = response.xpath("//strong[text()[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'company overview')]]/../following-sibling::p[1]/span/text()").get()   # select based on text (case insensitive)

        i = 0
        # Iterate over the list of Responsibilities, Basic and Preferred Qualifications
        for ul in response.xpath("//div[@id='content']/ul"):
            keyPointList = []
            for li in ul.xpath(".//li"):
                keyPoint = ''
                for span in li.xpath(".//span"):
                    keyPoint += span.xpath(".//text()").get()
                keyPointList.append(keyPoint)

            if i == 0:
                item['responsibilities'] = keyPointList
            elif i == 1:
                item['basic_qualifications'] = keyPointList
            elif i == 2:
                item['preferred_qualifications'] = keyPointList
                break   # Got all important job details, No need to iterate further

            keyPointList = []
            i += 1

        item['apply_link'] = apply_link
        yield item

    def parse(self, response):
        for job in response.xpath("//div[@class='opening']/a/@href"):
            apply_link = job.get()
            gh_jid = apply_link.split('=')[1]   # Get the job id from the apply link
            detail_page = f'https://boards.greenhouse.io/embed/job_app?for=coursera&token={gh_jid}'
            yield response.follow(detail_page, callback=self.parse_details, cb_kwargs={'apply_link': apply_link})   # Go to the job details page