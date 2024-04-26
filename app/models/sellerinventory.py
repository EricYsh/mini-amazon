from flask import current_app as app
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
import datetime

# For reference, the SQL for the Users table is as follows:
# 
# CREATE TABLE SellerInventories (
#     id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
#     sellerid INT NOT NULL REFERENCES Users(id),
#     productid INT NOT NULL REFERENCES Products(id),
#     quantity INT NOT NULL CHECK (quantity >= 0)
# );
DB_NAME = os.getenv('DB_NAME', 'amazon')
DB_USER = os.getenv('DB_USER', 'ubuntu')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'ZhkFrwbn5uKzkdoECS2ID7wxKYgHyr')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class SellerInventory:
    def __init__(self, id, sellerid, productid, quantity):
        self.id = id
        self.sellerid = sellerid
        self.productid = productid
        self.quantity = quantity

    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
SELECT p.name, p.image, pri.price, s.quantity, s.id
FROM SellerInventories AS s
JOIN Products AS p ON s.productid = p.id
JOIN (
    SELECT inventoryid, price, ROW_NUMBER() 
    OVER (PARTITION BY inventoryid ORDER BY time_changed DESC) AS row_num
    FROM PriceHistory
) AS pri ON pri.inventoryid = s.id AND pri.row_num = 1
WHERE s.sellerid = :uid;
''',
                        uid=uid
        )
        inventory_rows = [{'name': row[0], 'image': row[1], 'price': row[2], 'quantity': row[3], 'id': row[4]} for row in rows]
        return inventory_rows


    @staticmethod
    def insert_new_product(uid, name, description, image, price, quantity, category):
        session = Session()
        try:
            existing_product = session.execute(
                text('SELECT id FROM Products WHERE name = :name'),
                {'name': name}
            ).fetchone()
            # print("existing_product:", existing_product)
            if not existing_product:
                result = session.execute(
                    text('''
                    INSERT INTO Products (name, description, image, categoryid)
                    VALUES (:name, :description, :image, :category)
                    RETURNING id
                    '''),
                    {'name': name, 'description': description, 'image': image, 'category': category}
                )
                product_id = result.fetchone()[0]
            else:
                product_id = existing_product[0]
                print("product_id:", product_id)
            existing_inventory = session.execute(
                text('''
                SELECT id FROM SellerInventories 
                WHERE sellerid = :sellerid AND productid = :productid
                '''),
                {'sellerid': uid, 'productid': product_id}
            ).fetchone()
            print("existing_inventory:", existing_inventory)
            if not existing_inventory:
                result = session.execute(
                    text('''
                    INSERT INTO SellerInventories (sellerid, productid, quantity)
                    VALUES (:sellerid, :productid, :quantity)
                    RETURNING id
                    '''),
                    {'sellerid': uid, 'productid': product_id, 'quantity': quantity}
                )
                inventory_id = result.fetchone()[0]
            else:
                inventory_id = existing_inventory[0]
                session.execute(
                    text('''
                    UPDATE SellerInventories 
                    SET quantity = quantity + :quantity
                    WHERE id = :id
                    '''),
                    {'quantity': quantity, 'id': inventory_id}
                )
            print("elseinventory_id:", inventory_id)
            latest_price = session.execute(
                text('''
                SELECT price FROM PriceHistory
                WHERE inventoryid = :inventoryid
                ORDER BY time_changed DESC
                LIMIT 1
                '''),
                {'inventoryid': inventory_id}
            ).fetchone()
            if not latest_price or (latest_price and latest_price[0] != price):
                session.execute(
                    text('''
                    INSERT INTO PriceHistory (inventoryid, price, time_changed)
                    VALUES (:inventoryid, :price, :time_changed)
                    '''),
                    {'inventoryid': inventory_id, 'price': price, 'time_changed': datetime.datetime.utcnow()}
                )
            else:
                print("No new price history record needed; latest price matches new price.")
            session.execute(
                text('''
                INSERT INTO PriceHistory (inventoryid, price)
                VALUES (:inventoryid, :price)
                '''),
                {'inventoryid': inventory_id, 'price': price}
            )

            session.commit()
            return '1'
        except Exception as e:
            session.rollback()
            print("Error:", e)
            return 0
        finally:
            session.close()







    @staticmethod
    def edit_product(product_id, price, quantity):
        session = Session()
        try:
            session.execute(
                text("""
                    UPDATE SellerInventories
                    SET quantity = :quantity
                    WHERE id = :product_id
                """),
                {'product_id': product_id, 'quantity': quantity}
            )
            session.execute(
                text("""
                    INSERT INTO PriceHistory (inventoryid, price, time_changed)
                    VALUES (:inventoryid, :price, :time_changed)
                """),
                {'inventoryid': product_id, 'price': price, 'time_changed': datetime.datetime.utcnow()}
            )

            session.commit()
        except Exception as e:
            session.rollback()
            print(str(e))
        finally:
            session.close()
