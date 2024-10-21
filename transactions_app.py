from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api 
#Import Account and Transaction models
from models import AccountModel, TransactionModel, db

app = Flask(__name__)

#Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bank.db"    #Path to the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    #Generally recomended to set this to false

db.init_app(app)
api = Api(app)


# Define REST API url's
def register_api():
    from transactions_api import TransactionAPI, AccountAPI   #Local import to avoid circular imports
    api.add_resource(TransactionAPI, '/transactions/<int:transaction_id>', '/transactions')
    api.add_resource(AccountAPI, '/accounts/<int:account_id>', '/accounts')


# Start the app
if __name__ == '__main__':
    
    # Create the database and tables (if they don't exist)
    with app.app_context():
        db.create_all() 
    
    register_api() 
    
    app.run(debug=True)

