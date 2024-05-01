from flask import current_app as app
from datetime import datetime


# For reference, the SQL for the Users table is as follows:
# 
# CREATE TABLE Orders (
#     id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
#     userid INT NOT NULL REFERENCES Users(id),
#     time_brought timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
#     order_status VARCHAR(255) NOT NULL
# );

class Order:
    def __init__(self, id, userid, time_brought, order_status):
        self.id = id
        self.userid = userid
        self.time_brought = time_brought
        self.order_status = order_status


    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, userid, time_brought, order_status
FROM Orders
WHERE userid = :uid
AND time_brought >= :since
ORDER BY time_brought DESC
''',
                              uid=uid,
                              since=since)
        return [Order(*row) for row in rows]


    @staticmethod
    def set_fulfillment(oid):
        rows = app.db.execute('''
UPDATE orders
SET order_status = 'fulfilled'
WHERE id = :oid
''',
                              oid=oid)


    @staticmethod
    def create_order(uid):
        # Get the current UTC time
        current_utc_time = datetime.utcnow()

        # Format the datetime to remove microseconds
        formatted_time = current_utc_time.strftime('%Y-%m-%d %H:%M:%S')

        rows = app.db.execute('''
    INSERT INTO Orders (userid, time_brought, order_status)
    VALUES (:uid, :current_utc_time, 'in progress')
    RETURNING id
    ''',
                                uid=uid,
                                current_utc_time=formatted_time)
        return rows[0][0]
    
    @staticmethod
    def get_order_by_user_id(user_id):
        rows = app.db.execute('''
SELECT id, userid, time_brought, order_status
FROM Orders
WHERE userid = :user_id
ORDER BY time_brought DESC
''',
                              user_id=user_id)
        return [Order(*row) for row in rows]
    

    @staticmethod
    def get_order_by_id(order_id):
        rows = app.db.execute('''
SELECT id, userid, time_brought, order_status
FROM Orders
WHERE id = :order_id
''',
                              order_id=order_id)
        return Order(*rows[0]) if rows else None