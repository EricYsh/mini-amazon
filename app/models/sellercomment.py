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
        SELECT comment, rate, date_commented, sellerid, id
        FROM SellerComments
        WHERE userid = :userid
        ORDER BY date_commented DESC
        LIMIT 5;
        """
        results = app.db.execute(sqlstr, userid=userid)
        comments = [{'comment': row[0], 'rate': row[1],
                     'date_commented': row[2],
                     'sellerid': row[3],
                        'id': row[4]
                     } for row in results]
        return comments
    
    @staticmethod
    def get_comment_by_id(comment_id):
        sqlstr = """
        SELECT id, sellerid, userid, comment, date_commented, rate
        FROM SellerComments
        WHERE id = :comment_id;
        """
        result = app.db.execute(sqlstr, comment_id=comment_id)
        if result:
            return SellerComment(*result[0])
        return None

    def update(self):
        sqlstr = """
        UPDATE SellerComments
        SET comment = :comment, rate = :rate, date_commented = current_timestamp
        WHERE id = :id;
        """
        app.db.execute(sqlstr, id=self.id, comment=self.comment, rate=self.rate)

    @staticmethod
    def delete_comment(comment_id):
        sqlstr = "DELETE FROM SellerComments WHERE id = :comment_id;"
        app.db.execute(sqlstr, comment_id=comment_id)