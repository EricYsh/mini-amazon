from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login

# For reference, the SQL for the Users table is as follows:
# 
# CREATE TABLE Users (
#     id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
#     email VARCHAR UNIQUE NOT NULL,
#     password VARCHAR(255) NOT NULL,
#     firstname VARCHAR(255) NOT NULL,
#     lastname VARCHAR(255) NOT NULL,
#     address VARCHAR(511),
#     isSeller BOOLEAN DEFAULT False,
#     balance DECIMAL(12,2) DEFAULT 0 CHECK (balance >= 0) NOT NULL
# );

class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, address, isSeller, balance):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.isSeller = isSeller
        self.balance = balance


    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, address, isSeller, balance
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname)
VALUES(:email, :password, :firstname, :lastname)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, address, isSeller, balance
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None


    @staticmethod
    def show_user_profile(id):
        row = app.db.execute("""
select email, firstname, lastname, address, isSeller, balance
from Users
where id = :id
""",
                              id = id)

        return {
        'email': row[0][0], 
        'firstname': row[0][1], 
        'lastname': row[0][2], 
        'address': row[0][3], 
        'isSeller': row[0][4], 
        'balance': row[0][5]}
       