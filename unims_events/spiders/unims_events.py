import scrapy
# import geopy

# from geopy.geocoders import GoogleV3
# from geopy.exc import GeocoderTimedOut

from unims_events.items import EventItem, OrganizerItem, LocationItem, GeoItem, AddressItem

country_lookup = {
    'Germany': 'DE'
}

class UniMuensterEventsSpider(scrapy.Spider):
    name = 'unims-events'
    start_urls = ['http://www.uni-muenster.de/Rektorat/exec/termine.php?layout=standard-ergebnis&limit=1000']

    def parse(self, response):
        # geolocator = GoogleV3()
        for event in response.xpath('//div[contains(@class,"vevent")]'):
            event_item = EventItem()
            event_item["@context"] = "http://schema.org"
            event_item["@type"] = "Event"

            address_field = event.xpath('div/div/span[contains(@class, "p-location")]//text()')
            if address_field:
                address_string = address_field.extract_first().replace('\n',' ')
                # address = geolocator.geocode(address_string, timeout=10)
                address = None

            location_item = LocationItem()
            location_item['@type'] = 'Place'
            location_item['name'] = address_string

            # if address:
            #     geo_item = GeoItem()
            #     geo_item['@type'] = 'GeoCoordinates'
            #     geo_item['latitude'] = address.latitude
            #     geo_item['longitute'] = address.longitude
            #     event_item['geo'] = geo_item
            #
            #     address_item = AddressItem()
            #     address_item['@type'] = 'PostalAddress'
            #     for component in address.raw['address_components']:
            #         if component['types'][0] == 'postal_code':
            #             address_item['postalCode'] = component['long_name']
            #         if component['types'][0] == 'locality':
            #             address_item['addressLocality'] = component['long_name']
            #         if component['types'][0] == 'route':
            #             address_item['streetAddress'] = component['long_name']
            #         if (component['types'][0] == 'route') and (component['types'][0] == 'street_number'):
            #             address_item['streetAddress'] + ' ' + component['long_name']
            #         if component['types'][0] == 'country':
            #             address_item['addressCountry'] = country_lookup.get(component['long_name'])
            #
            #     location_item['address'] = address_item

            organizer_item = OrganizerItem()
            organizer_item['@type'] = 'Person'
            organizer_item['name'] = 'Olga Organisator'

            event_item['name'] = event.xpath('h3/a/span/text()').extract_first()
            event_item['organizer'] = organizer_item
            event_item['x-tags'] = 'tags'
            event_item['source'] = response.urljoin(event.xpath('h3/a/@href').extract_first())
            event_item['startDate'] = event.xpath('div/div/span[contains(@class, "dtstart")]/@title').extract_first()
            end_date = event.xpath('div/div/span[contains(@class, "dtend")]/@title').extract_first()
            if end_date:
                event_item['endDate'] = end_date
            event_item['location'] = location_item

            details_page = event_item['source']

            event_item = scrapy.Request(details_page, meta={'event_item': event_item}, callback=self.parse_event)

            yield event_item

    def parse_event(self, response):
        event_item = response.request.meta['event_item']
        event_item_description = response.xpath('//div[contains(@class, "vevent")]//*[self::p or self::em][not(a)]/text()').extract_first()
        if event_item_description:
            event_item['description'] = event_item_description
        else:
            event_item['description'] = 'FIXME Missing description'

        subheading = response.xpath('//*[@id="inhalt"]/article/div[2]/div/h2/span/text()').extract_first()
        if subheading:
            event_item['description'] = subheading + ':\n\n' + event_item['description']

        event_item['x-category'] = response.xpath('//span[contains(@class, "p-category")]/text()').extract_first()
        event_item_url = response.xpath('//a[contains(@class, "p-url")]/@href').extract_first()
        if event_item_url:
            event_item['url'] = event_item_url
        return event_item
