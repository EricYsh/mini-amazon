from flask import current_app as app

# For reference, the SQL for the Users table is as follows:
# 
# CREATE TABLE Products (
#     id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
#     categoryid INT NOT NULL REFERENCES Categories(id),
#     name VARCHAR(255) UNIQUE NOT NULL,
#     description VARCHAR(511),
#     image VARCHAR(255),
# );

class Product:
    def __init__(self, id, categoryid, name, description, image, price = None, rating = None):
        self.id = id
        self.categoryid = categoryid
        self.name = name
        self.description = description
        self.image = image
        self.price = price
        self.rating = rating

    @staticmethod
    def get(id):
        rows = app.db.execute('''
            SELECT id, name, price, available
            FROM Products
            WHERE id = :id
            ''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all():
        rows = app.db.execute('''
            SELECT *
            FROM Products
            ''',)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_top_k_expensive_products(k):
        rows = app.db.execute('''
            SELECT p.id, p.categoryid, p.name, p.description, p.image, ph.price, COALESCE(ROUND(avg_rating.avg_rate, 2), 0)
            FROM Products p
            JOIN SellerInventories si ON p.id = si.productid
            JOIN PriceHistory ph ON si.id = ph.inventoryid
            JOIN (
                SELECT inventoryid, MAX(time_changed) AS latest_time
                FROM PriceHistory
                GROUP BY inventoryid
            ) ph_latest ON ph.inventoryid = ph_latest.inventoryid AND ph.time_changed = ph_latest.latest_time
            LEFT JOIN (
                SELECT productid, AVG(rate) AS avg_rate
                FROM ProductComments
                GROUP BY productid
            ) avg_rating ON p.id = avg_rating.productid
            ORDER BY ph.price DESC
            LIMIT :k
            ''',
                            k=k)
        return [Product(*row) for row in rows]
    


    @staticmethod
    def search_products_by_name(search, category_id=None):
        query_params = {'search': search}
        category_condition = ''

        if category_id:
            category_condition = 'AND p.categoryid = :category_id'
            query_params['category_id'] = category_id

        rows = app.db.execute(f'''
            SELECT p.id, p.categoryid, p.name, p.description, p.image, ph.price, COALESCE(ROUND(avg_rating.avg_rate, 2), 0) AS average_rating
            FROM Products p
            JOIN SellerInventories si ON p.id = si.productid
            JOIN PriceHistory ph ON si.id = ph.inventoryid
            JOIN (
                SELECT inventoryid, MAX(time_changed) AS latest_time
                FROM PriceHistory
                GROUP BY inventoryid
            ) ph_latest ON ph.inventoryid = ph_latest.inventoryid AND ph.time_changed = ph_latest.latest_time
            LEFT JOIN (
                SELECT productid, AVG(rate) AS avg_rate
                FROM ProductComments
                GROUP BY productid
            ) avg_rating ON p.id = avg_rating.productid
            WHERE p.name ILIKE '%' || :search || '%' {category_condition}
            ORDER BY ph.price DESC
            LIMIT 50
            ''', **query_params)
        return [Product(*row) for row in rows]

    
    @staticmethod
    def search_products_by_description(search, category_id=None):
        query_params = {'search': search}
        category_condition = ''

        # 如果提供了 category_id，则在查询中加入一个额外的条件
        if category_id:
            category_condition = 'AND p.categoryid = :category_id'
            query_params['category_id'] = category_id

        rows = app.db.execute(f'''
            SELECT p.id, p.categoryid, p.name, p.description, p.image, ph.price, COALESCE(ROUND(avg_rating.avg_rate, 2), 0) AS average_rating
            FROM Products p
            JOIN SellerInventories si ON p.id = si.productid
            JOIN PriceHistory ph ON si.id = ph.inventoryid
            JOIN (
                SELECT inventoryid, MAX(time_changed) AS latest_time
                FROM PriceHistory
                GROUP BY inventoryid
            ) ph_latest ON ph.inventoryid = ph_latest.inventoryid AND ph.time_changed = ph_latest.latest_time
            LEFT JOIN (
                SELECT productid, AVG(rate) AS avg_rate
                FROM ProductComments
                GROUP BY productid
            ) avg_rating ON p.id = avg_rating.productid
            WHERE p.description ILIKE '%' || :search || '%' {category_condition}
            ORDER BY ph.price DESC
            LIMIT 50
            ''', **query_params)
        return [Product(*row) for row in rows]



    @staticmethod
    def get_product_by_id(product_id):
        rows = app.db.execute('''
            SELECT p.id, p.categoryid, p.name, p.description, p.image, ph.price, COALESCE(ROUND(avg_rating.avg_rate, 2), 0) AS average_rating
            FROM Products p
            JOIN SellerInventories si ON p.id = si.productid
            JOIN PriceHistory ph ON si.id = ph.inventoryid
            JOIN (
                SELECT inventoryid, MAX(time_changed) AS latest_time
                FROM PriceHistory
                GROUP BY inventoryid
            ) ph_latest ON ph.inventoryid = ph_latest.inventoryid AND ph.time_changed = ph_latest.latest_time
            LEFT JOIN (
                SELECT productid, AVG(rate) AS avg_rate
                FROM ProductComments
                GROUP BY productid
            ) avg_rating ON p.id = avg_rating.productid
            WHERE p.id = :product_id
            ''',
                            product_id=product_id)
        if rows:
            row = rows[0]
            return Product(*row)
        else:
            return None


    @staticmethod
    def get_reviews(product_id):
        reviews = app.db.execute('''
            SELECT pc.id, pc.comment, pc.time_commented, pc.rate, u.firstname, u.lastname
            FROM ProductComments pc
            JOIN Users u ON pc.userid = u.id
            WHERE pc.productid = :product_id
            ORDER BY pc.time_commented DESC
            ''',
                                product_id=product_id)

        return reviews if reviews is not None else None


    @staticmethod
    def get_sellers(product_id):
        sellers = app.db.execute('''
            SELECT u.id, u.firstname, u.lastname, u.email, si.quantity
            FROM Users u
            JOIN SellerInventories si ON u.id = si.sellerid
            WHERE si.productid = :product_id
            ''',
            product_id=product_id)
        return sellers if sellers is not None else None
        
    @staticmethod
    def get_all_categories():
        rows = app.db.execute('''
            SELECT id, name
            FROM Categories
            ORDER BY name ASC
        ''')
        return rows  
