from werkzeug.security import generate_password_hash
import csv
from faker import Faker
from random import randint, seed
import random
from datetime import datetime

num_users = 100
num_categories = 10
num_price_histories = 6000
num_sellerinventories = 2000
num_products = 500
num_orderitems = 500
num_carts = 200
num_orders = 50

# Global variables
NUM_SELLER_COMMENTS = 100
NUM_PRODUCT_COMMENTS = 1500
PRODUCT_ID_MOD = num_products
SELLER_ID_MIN = num_users / 2
SELLER_ID_MAX = num_users - 1
USER_ID_MIN = 0
USER_ID_MAX = num_users - 1
RATE_MIN = 1
RATE_MAX = 5


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

def get_csv_writer(f):
    # return csv.writer(f, dialect='unix')
    return csv.writer(f, dialect='unix', quoting=csv.QUOTE_MINIMAL)



## gen1
def gen_users(num_users):
    used_email = set()
    with open('Users.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            while email in used_email:
                profile = fake.profile()
                email = profile['mail']
            used_email.add(email)
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name = fake.name().split()
            firstname = name[0]
            lastname = name[-1] if len(name) > 1 else ''
            address = fake.address().replace('\n', ', ')
            is_seller = uid >= (num_users/2)
            balance = round(random.uniform(0, 1000), 2)
            writer.writerow([uid, email, password, firstname, lastname, address, is_seller, balance])
        print(f'{num_users} generated')

def gen_categories(num_categories):
    with open('Categories.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        print('Categories...', end=' ', flush=True)
        categories = ['Electronics', 'Books', 'Clothing', 'Home & Garden', 'Toys', 'Sports', 'Beauty', 'Automotive', 'Art', 'Music']
        for cid in range(num_categories):
            if cid < len(categories):
                name = categories[cid]
            else:
                name = fake.word().capitalize()
            writer.writerow([cid, name])
        print(f'{num_categories} generated')

def gen_price_histories(num_price_histories,num_sellerinventories):
    with open('PriceHistory.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        print('PriceHistory...', end=' ', flush=True)
        for hid in range(num_price_histories):
            if hid % 100 == 0:
                print(f'{hid}', end=' ', flush=True)
            inventoryid = random.randint(0, num_sellerinventories-1)
            price = round(random.uniform(0.01, 500.00), 2)
            time_changed = fake.date_time_between(start_date='-2y', end_date='now').strftime("%Y-%m-%d %H:%M")
            writer.writerow([hid, inventoryid, price, time_changed])
        print(f'{num_price_histories} generated')


## gen2.py
def fake_decimal(max_digits=12, decimal_places=2):
    number = round(random.random() * (10**(max_digits - decimal_places)), decimal_places)
    formatted_number = f"{number:0.{decimal_places}f}"
    return formatted_number


def gen_products(num_products):
    used_name = set()
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Product...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 10 == 0:
                print(f'{pid}', end=' ', flush=True)
            category_id = fake.random_int(min=0, max=num_categories-1)
            
            name = fake.sentence(nb_words=3)[:-1]
            while name in used_name:
                name = fake.sentence(nb_words=3)[:-1]
            used_name.add(name)
            description = fake.sentence(nb_words=30)
            image = random.choice(urls)
            writer.writerow([pid, category_id, name, description, image])
        print(f'{num_products} generated')
    return




def gen_sellerinventories(num_sellerinventories):
    with open('SellerInventories.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('SellerInventories...', end=' ', flush=True)
        for sid in range(num_sellerinventories):
            if sid % 10 == 0:
                print(f'{sid}', end=' ', flush=True)
            sellerid = fake.random_int(min=50, max=99)
            pid = fake.random_int(min=0, max=num_products-1)
            quantity = fake.random_int(min=0, max=100)
            writer.writerow([sid, sellerid, pid, quantity])
        print(f'{num_sellerinventories} generated')
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



# // id [0 - 200]
# // userid = [random 0 - 99]
# // quantity [1-100] 付款功能需要 check数量够不够
# // sellerinventoryid [0 - 1999]
# // saved for later [ random true of false]
# CREATE TABLE Carts ( 【shanghui】
#     id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
#     userid INT NOT NULL REFERENCES Users(id),
#     quantity INT NOT NULL,
#     sellerinventoryid INT NOT NULL REFERENCES SellerInventories(id),
#     saved_for_later BOOLEAN DEFAULT FALSE
def gen_carts(num_carts):
    with open('Carts.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Carts...', end=' ', flush=True)
        for id in range(num_carts):
            if id % 10 == 0:
                print(f'{id}', end=' ', flush=True)
            userid = fake.random_int(min=0, max=num_users-1)
            quantity = fake.random_int(min=1, max=100)
            sellerinventoryid = fake.random_int(min=0, max=num_sellerinventories-1)
            saved_for_later = fake.random_element(elements=('true', 'false'))
            writer.writerow([id, userid, quantity, sellerinventoryid, saved_for_later])
        print(f'{num_carts} generated')
    return


# // id [0 - 49]
# // userid [random 0 - 99]
# // time [random Date]
# // order_status [random status list[in progress, fulfilled]]
# CREATE TABLE Orders ( 【shanghui】
#     id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
#     userid INT NOT NULL REFERENCES Users(id),
#     time_brought timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
#     order_status VARCHAR(255) NOT NULL
def gen_orders(num_orders):
    order_statuses = ['in progress', 'fulfilled']
    with open('Orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush=True)
        for id in range(num_orders):
            if id % 10 == 0:
                print(f'{id}', end=' ', flush=True)
            userid = fake.random_int(min=0, max=num_users-1)
            time = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=None)
            formatted_time = time.strftime('%Y-%m-%d %H:%M')  # Custom format
            order_status = fake.random_element(elements=order_statuses)
            writer.writerow([id, userid, formatted_time, order_status])
        print(f'{num_orders} generated')
    return



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
write_to_csv('SellerComments.csv', seller_comments_data)

# Generate and write the data for ProductComments
product_comments_data = generate_product_comments()
write_to_csv('ProductComments.csv', product_comments_data)



gen_carts(num_carts)
gen_orders(num_orders)


gen_products(num_products)
gen_sellerinventories(num_sellerinventories)
gen_orderitems(num_orderitems)

gen_users(num_users)
gen_categories(num_categories)
gen_price_histories(num_price_histories,num_sellerinventories)
