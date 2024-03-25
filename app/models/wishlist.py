from flask import current_app as app


class WishlistItem:
    def __init__(self, id, uid, pid, time_added):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_added = time_added

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_added
FROM Wishes
WHERE id = :id
''',
                              id=id)
        return WishlistItem(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
SELECT id, uid, pid, time_added
FROM Wishes
WHERE uid = :uid
ORDER BY time_added DESC
''',
                              uid=uid)
        return [WishlistItem(*row) for row in rows]

# a method for entering a new object into the database
    @staticmethod
    def add_wishlist_item(uid, pid, time_added):
        try:
            rows = app.db.execute("""
INSERT INTO Wishes(uid, pid, time_added)
VALUES(:uid, :pid, :time_added)
RETURNING id
""",
                                  uid=uid,
                                  pid=pid,
                                  time_added=time_added)
            id = rows[0][0]
            return WishlistItem.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None
