from datetime import datetime, date
from email.mime import image
from WebApplication import db,app
from werkzeug.security import check_password_hash, generate_password_hash

import jdatetime

###

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(100), nullable = True)
    password = db.Column(db.String, nullable = True)
    role = db.Column(db.String(50), nullable = True)
    credit = db.Column(db.String(100), nullable = True)
    assets = db.Column(db.String(100), nullable = True)
    first_and_last_name = db.Column(db.String(100), nullable = True)
    international_bank_account_number = db.Column(db.String(100), nullable = True)
    bank_card_number = db.Column(db.String(100), nullable = True)
    verification_status = db.Column(db.String(10), nullable = True)
    registration = db.Column(db.String(50), nullable = False, default = str(jdatetime.datetime.now())) # Registration date

    def check_password(self,value): 
        return check_password_hash(self.password,value)

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_phone = db.Column(db.String(100), nullable = True)
    user_name = db.Column(db.String(100), nullable = True)
    transactions_type = db.Column(db.String(50), nullable = True)
    amount = db.Column(db.String(50), nullable = True)
    weight = db.Column(db.String(50), nullable = True) # Grams
    gold_rate = db.Column(db.String(50), nullable = True)
    description = db.Column(db.String(100), nullable = True)
    content = db.Column(db.String(100), nullable = True)
    status = db.Column(db.String(50), nullable = True)
    registration = db.Column(db.String(50), nullable = True, default = str(jdatetime.datetime.now())) # Registration date

class BuyPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String(100), nullable=True)
    registration = db.Column(db.String(50), nullable=False, default=str(jdatetime.datetime.now()))

class SellPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String(100), nullable=True)
    registration = db.Column(db.String(50), nullable=False, default=str(jdatetime.datetime.now()))

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(100), nullable=True)
    message = db.Column(db.Text, nullable=True)
    date = db.Column(db.String(50), nullable=False, default=str(jdatetime.datetime.now()))



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

###

# create the database and the db table
app.app_context().push()
db.create_all()

# commit the changes
db.session.commit()

# user = User(phone = "09309203258", password = generate_password_hash("PASS"), role = "administrator", credit = 0, assets = 0, first_and_last_name="", international_bank_account_number="", bank_card_number="", verification_status = "تأیید شده")
# db.session.add(user)
# db.session.commit()
