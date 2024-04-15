from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random
from datetime import datetime

num_users = 100
num_categories = 10
num_price_histories = 6000
num_sellerinventories = 2000

Faker.seed(0)
fake = Faker()

def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

def gen_users(num_users):
    with open('Users.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
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

gen_users(num_users)
gen_categories(num_categories)
gen_price_histories(num_price_histories,num_sellerinventories)
