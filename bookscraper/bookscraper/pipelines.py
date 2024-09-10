# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()
            else:
                value = adapter.get(field_name)
                adapter[field_name] = value[0].replace(' ...more', '')

        # Category and Product Type to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        # Price without pound symbol and cast to float format
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)

        # Availability showing only number of books in stock if any
        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')

        if (len(split_string_array) < 2):
            adapter['availability'] = 0
        else:
            availability_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availability_array[0])

        # Number of reviews as integer
        num_review_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_review_string)

        # Review stars as number
        stars_string = adapter.get('stars')
        split_stars_array = stars_string.split(' ')

        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == 'zero':
            adapter['stars'] = 0
        elif stars_text_value == 'one':
            adapter['stars'] = 1
        elif stars_text_value == 'two':
            adapter['stars'] = 2
        elif stars_text_value == 'three':
            adapter['stars'] = 3
        elif stars_text_value == 'four':
            adapter['stars'] = 4
        elif stars_text_value == 'five':
            adapter['stars'] = 5

        return item

import mysql.connector

class SaveToMySQLPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host        = 'localhost',
            user        = 'root',
            password    = '',
            database    = 'books'
        )

        self.cur = self.conn.cursor()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS books(
                id              INT NOT NULL auto_increment,
                url             VARCHAR(255),
                title           TEXT,
                upc             VARCHAR(255),
                product_type    VARCHAR(255),
                stars           INTEGER,
                category        VARCHAR(255),
                description     TEXT,
                price           DECIMAL,
                tax             DECIMAL,
                price_incl_tax  DECIMAL,
                price_excl_tax  DECIMAL,
                availability    INTEGER,
                num_reviews     INTEGER,
                PRIMARY KEY (id)
            )
        """)

    def process_item(self, item, spider):
        self.cur.execute("""
            INSERT INTO books (
                url,
                title,
                upc,
                product_type,
                stars,
                category,
                description,
                price,
                tax,
                price_incl_tax,
                price_excl_tax,
                availability,
                num_reviews
            )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
        """, (
            item['url'],
            item['title'],
            item['upc'],
            item['product_type'],
            item['stars'],
            item['category'],
            str(item['description']),
            item['price'],
            item['tax'],
            item['price_incl_tax'],
            item['price_excl_tax'],
            item['availability'],
            item['num_reviews']
        ))
        
        self.conn.commit()
        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()