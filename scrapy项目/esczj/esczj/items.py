# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EsczjItem(scrapy.Item):
    car_series = scrapy.Field()
    car_id = scrapy.Field()
    models = scrapy.Field()
    price = scrapy.Field()
    travel_mileage = scrapy.Field()
    last_time = scrapy.Field()
    displacement = scrapy.Field()
    city = scrapy.Field()
    standard = scrapy.Field()
    car_location = scrapy.Field()
    contacts = scrapy.Field()
    inspection_expires = scrapy.Field()
    insurance_expires = scrapy.Field()
    warranty_expires = scrapy.Field()
    emission_standard = scrapy.Field()
    number_of_transfers = scrapy.Field()
    cer_user = scrapy.Field()
    maintenance = scrapy.Field()
    merchant_name = scrapy.Field()
    cer_engine = scrapy.Field()
    transmission = scrapy.Field()
    vehicle_class = scrapy.Field()
    color = scrapy.Field()
    fuel_label = scrapy.Field()
    drive_type = scrapy.Field()
    mouth = scrapy.Field()