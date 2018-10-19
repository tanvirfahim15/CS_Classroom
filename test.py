from Database.database import db

for i in db.users.find():
    print(i)