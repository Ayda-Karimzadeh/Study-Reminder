import database as db
from datetime import date, timedelta

db.create_table()

today = date.today()
review = today + timedelta(days=1)

db.add_topic("filter python", str(today), str(review))

print(db.get_review(str(review)))