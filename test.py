from dataaccess import _db_access as db
from dataaccess import data_access
from reminder import Reminder


r = db.query_where_equal('reminder', ['id', 'category_id', 'content', 'time'])
print(r)
