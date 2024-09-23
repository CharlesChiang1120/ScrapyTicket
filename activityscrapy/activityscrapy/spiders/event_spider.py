import scrapy
import json
import os

class EventSpider(scrapy.Spider):
    name = "event_spider"
    start_urls = ['https://kktix.com/']

    def parse(self, response):
        events_dict = {}
        event_elements = response.xpath('//ul/li/a')

        for event_element in event_elements:
            try:

                activity_info = event_element.xpath('.//figure/figcaption/div/div/div/div[1]/h2/text()').get()
                time = event_element.xpath('.//span[@class="date"]/text()').re_first(r'\d{4}/\d{1,2}/\d{1,2}')
                ticket_link = event_element.xpath('./@href').get()
                image_url = event_element.xpath('.//figure/img/@src').get()

                if activity_info and time:
                    events_dict[activity_info] = {'date': time, 'ticketLink': ticket_link, 'image': image_url}
            except Exception as e:
                self.logger.warning(f'Error extracting event details: {e}')

        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'events.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(events_dict, f, ensure_ascii=False, indent=4)

        for activity_info, info in events_dict.items():
            self.log(f'Activity Info: {activity_info}')
            self.log(f'Date: {info["date"]}')
            self.log(f'Ticket Link: {info["ticketLink"]}')
            self.log(f'Image: {info["image"]}')
            self.log('-' * 40)
