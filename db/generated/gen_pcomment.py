import csv
from random import randint, seed
from faker import Faker

# Initialize the Faker generator
fake = Faker()

# Seed the random number generator for reproducibility
seed(1)

def generate_data():
    data = []
    for id in range(1500):
        productid = id % 500
        userid = randint(0, 99)
        comment = fake.text(max_nb_chars=200)  # Generate random text for the comment
        time_commented = fake.date_time_this_decade()  # Generate random datetime in this decade
        rate = randint(1, 5)  # Random rate between 1 and 5
        data.append([id, productid, userid, comment, time_commented, rate])
    return data

def write_to_csv(filename, data):
    # Open the file in append mode, so existing data is not overwritten
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

# Generate the data
data = generate_data()

# Write the generated data to the CSV file
write_to_csv('/home/ubuntu/shared/mini-amazon/db/generated/ProductComments.csv', data)
