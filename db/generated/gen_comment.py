import csv
from random import randint, seed
from faker import Faker

# Global variables
NUM_SELLER_COMMENTS = 100
NUM_PRODUCT_COMMENTS = 1500
PRODUCT_ID_MOD = 500
SELLER_ID_MIN = 50
SELLER_ID_MAX = 99
USER_ID_MIN = 0
USER_ID_MAX = 99
RATE_MIN = 1
RATE_MAX = 5

# Initialize the Faker generator
fake = Faker()

# Seed the random number generator for reproducibility
seed(1)

def generate_seller_comments():
    data = []
    for id in range(NUM_SELLER_COMMENTS):
        userid = randint(USER_ID_MIN, USER_ID_MAX)
        sellerid = randint(SELLER_ID_MIN, SELLER_ID_MAX)
        comment = fake.sentence(nb_words=10)
        time_commented = fake.date_time_this_decade().strftime('%Y-%m-%d %H:%M')
        rate = randint(RATE_MIN, RATE_MAX)
        data.append([id, userid, sellerid, comment, time_commented, rate])
    return data

def generate_product_comments():
    data = []
    for id in range(NUM_PRODUCT_COMMENTS):
        productid = id % PRODUCT_ID_MOD
        userid = randint(USER_ID_MIN, USER_ID_MAX)
        comment = fake.text(max_nb_chars=200)
        time_commented = fake.date_time_this_decade().strftime('%Y-%m-%d %H:%M')
        rate = randint(RATE_MIN, RATE_MAX)
        data.append([id, productid, userid, comment, time_commented, rate])
    return data

def write_to_csv(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            writer.writerow(row)

# Generate and write the data for SellerComments
seller_comments_data = generate_seller_comments()
write_to_csv('/home/ubuntu/shared/mini-amazon/db/generated/SellerComments.csv', seller_comments_data)

# Generate and write the data for ProductComments
product_comments_data = generate_product_comments()
write_to_csv('/home/ubuntu/shared/mini-amazon/db/generated/ProductComments.csv', product_comments_data)
