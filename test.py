from dataaccess import _db_access as db
from dataaccess import data_access
from reminder import Reminder

rem = Reminder()
rem.content = 'testing reminder 2'
data_access.add_reminder(rem)

