import scrapy
from scrapy.item import Item, Field

# thanks to https://stackoverflow.com/a/40581523/274811
class EventItem(scrapy.Item):

    def __init__(self):
        super().__init__()
        self.fields["@context"] = scrapy.Field()
        self.fields["@type"] = scrapy.Field()
        self.fields["x-category"] = scrapy.Field()
        self.fields["x-tags"] = scrapy.Field()
        self.fields["name"] = scrapy.Field()
        self.fields["description"] = scrapy.Field()
        self.fields["organizer"] = scrapy.Field()
        self.fields["url"] = scrapy.Field()
        self.fields["source"] = scrapy.Field()
        self.fields["startDate"] = scrapy.Field()
        self.fields["endDate"] = scrapy.Field()
        self.fields["location"] = scrapy.Field()
        self.fields["geo"] = scrapy.Field()

class OrganizerItem(scrapy.Item):

    def __init__(self):
        super().__init__()
        self.fields["@type"] = scrapy.Field()
        self.fields["name"] = scrapy.Field()

class LocationItem(scrapy.Item):

    def __init__(self):
        super().__init__()
        self.fields["@type"] = scrapy.Field()
        self.fields["name"] = scrapy.Field()
        self.fields["address"] = scrapy.Field()

class GeoItem(scrapy.Item):

    def __init__(self):
        super().__init__()
        self.fields["@type"] = scrapy.Field()
        self.fields["latitude"] = scrapy.Field()
        self.fields["longitute"] = scrapy.Field()

class AddressItem(scrapy.Item):

    def __init__(self):
        super().__init__()
        self.fields["@type"] = scrapy.Field()
        self.fields["addressCountry"] = scrapy.Field()
        self.fields["addressLocality"] = scrapy.Field()
        self.fields["postalCode"] = scrapy.Field()
        self.fields["streetAddress"] = scrapy.Field()
