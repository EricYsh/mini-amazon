import csv
from random import randint, seed
from faker import Faker

# Initialize the Faker generator
fake = Faker()

# Seed the random number generator for reproducibility
seed(1)

def generate_data():
    data = []
    for id in range(100):  # IDs from 0 to 99
        userid = randint(0, 99)  # UserID random between 0 and 99
        sellerid = randint(50, 99)  # SellerID random between 50 and 99
        comment = fake.sentence(nb_words=10)  # Generate a shorter, more precise comment
        date_commented = fake.date_this_decade()  # Generate a random date in this decade, formatted as 'YYYY-MM-DD'
        rate = randint(1, 5)  # Random rate between 1 and 5
        data.append([id, userid, sellerid, comment, date_commented, rate])
    return data

def write_to_csv(filename, data):
    # Open the file in append mode, so existing data is not overwritten
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            writer.writerow(row)

# Generate the data
data = generate_data()

# Write the generated data to the CSV file
write_to_csv('/home/ubuntu/shared/mini-amazon/db/generated/SellerComments.csv', data)
