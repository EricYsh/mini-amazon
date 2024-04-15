from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random

num_users = 100
num_products = 500
num_purchases = 2500
num_categories = 10
num_sellerinvertories = 2000
num_orderitems = 500
num_orders = 10


Faker.seed(0)
fake = Faker()

urls = [
    "https://m.media-amazon.com/images/I/614pn1oYPCL.jpg",
    "https://m.media-amazon.com/images/I/611DiOFTVfL.jpg",
    "https://m.media-amazon.com/images/I/61YNwmfTUOL._AC_UF894,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/51aX6Nv7rAL.jpg",
    "https://m.media-amazon.com/images/I/61Q79ulDs6L._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/61AcT0ZuO3L.jpg",
    "https://m.media-amazon.com/images/I/91eY5tY-pGS._AC_UF894,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/71gtKUViyOL._AC_UF1000,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/61x-ngKuW3L._AC_UF894,1000_QL80_.jpg",
    "https://m.media-amazon.com/images/I/51xT9lbPAmL._AC_UF1000,1000_QL80_.jpg"
]


def fake_decimal(max_digits=12, decimal_places=2):
    number = round(random.random() * (10**(max_digits - decimal_places)), decimal_places)
    formatted_number = f"{number:0.{decimal_places}f}"
    return formatted_number


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_products(num_products):
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Product...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 10 == 0:
                print(f'{pid}', end=' ', flush=True)
            category_id = fake.random_int(min=0, max=num_categories-1)
            name = fake.sentence(nb_words=3)[:-1]
            description = fake.sentence(nb_words=4)
            image = random.choice(urls)
            writer.writerow([pid, category_id, description, image, name])
        print(f'{num_products} generated')
    return




def gen_sellerinventories(num_sellerinvertories):
    with open('SellerInventories.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('SellerInventories...', end=' ', flush=True)
        for sid in range(num_sellerinvertories):
            if sid % 10 == 0:
                print(f'{sid}', end=' ', flush=True)
            sellerid = fake.random_int(min=50, max=99)
            pid = fake.random_int(min=0, max=num_products-1)
            quantity = fake.random_int(min=1, max=100)
            writer.writerow([sid, sellerid, pid, quantity])
        print(f'{num_sellerinvertories} generated')
    return

def gen_orderitems(num_orderitems):
    with open('OrderItems.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('OrderItems...', end=' ', flush=True)
        for oiid in range(num_orderitems):
            if oiid % 10 == 0:
                print(f'{oiid}', end=' ', flush=True)
            oid = oiid % 50
            pid = fake.random_int(min=0, max=num_products-1)
            sellerid = fake.random_int(min=50, max=99)
            quantity = fake.random_int(min=1, max=5)
            brought_price = fake_decimal(12, 2)
            fulfilled = fake.random_element(elements=('true', 'false'))
            writer.writerow([oiid, oid, pid, sellerid, quantity, brought_price, fulfilled])
        print(f'{num_orderitems} generated')
    return





gen_products(num_products)
gen_sellerinventories(num_sellerinvertories)
gen_orderitems(num_orderitems)