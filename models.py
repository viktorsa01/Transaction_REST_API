from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class AccountModel(db.Model):
    __tablename__ = 'accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    availableCash = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f"Account = (name = {self.name}, Account balance = {self.availableCash})"

class TransactionModel(db.Model):
    __tabename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    sourceAccountId = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)     #sourceAccountId points to the id of the source account
    destinationAccountId = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)  #destinationAccountId points to the id of the destination account
    registeredTime = db.Column(db.DateTime, nullable=False)  
    executedTime = db.Column(db.DateTime, nullable=False) 
    success = db.Column(db.Boolean, nullable=False)
    cashAmount = db.Column(db.Float, nullable=False)
    
    sourceAccount = db.relationship('AccountModel', foreign_keys=[sourceAccountId], backref= "outgoing_transactions")   #Sets up bidirectional relationship between AccountModel and TransactionModel
    destinationAccount = db.relationship('AccountModel', foreign_keys=[destinationAccountId], backref= "incoming_transactions")     #Sets up bidirectional relationship between AccountModel and TransactionModel  
    
    def __repr__(self):
        return f"Transaction = (sourceAccountId = {self.sourceAccountId}, destinationAccountId = {self.destinationAccountId}, cash amount = {self.cashAmount})"
