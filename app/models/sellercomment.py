from flask import current_app as app

# For reference, the SQL for the Users table is as follows:
# 
# CREATE TABLE SellerComments (
#     id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
#     userid INT NOT NULL REFERENCES Users(id),
#     sellerid INT NOT NULL REFERENCES Users(id),
#     comment VARCHAR(255),
#     date_commented timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
#     rate INT
# );

class SellerComment:
    def __init__(self, id, userid, sellerid, comment, date_commented, rate):
        self.id = id
        self.userid = userid
        self.sellerid = sellerid
        self.comment = comment
        self.date_commented = date_commented
        self.rate = rate

    @staticmethod
    def get_seller_comments_by_user(userid):
        sqlstr = """
        SELECT id, comment, rate, date_commented, sellerid
        FROM SellerComments
        WHERE userid = :userid
        ORDER BY date_commented DESC
        LIMIT 5;
        """
        results = app.db.execute(sqlstr, userid=userid)
        comments = [{'comment': row[0], 'rate': row[1],
                     'date_commented': row[2],
                     'sellerid': row[3]
                     } for row in results]
        return comments