from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 100
num_carts = 200
num_orders = 50
num_sellerinvertories=2000

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')



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



gen_carts(num_carts)
gen_orders(num_orders)
