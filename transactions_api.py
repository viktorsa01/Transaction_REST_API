from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import db, AccountModel, TransactionModel
from datetime import datetime

#Define the fields for accounts
accountFields = {
    "id": fields.Integer,
    "name": fields.String,
    "availableCash": fields.Float
}

#Define the fields for transactions
transactionFields = {
    "id": fields.Integer,
    "sourceAccountId": fields.Integer,
    "destinationAccountId": fields.Integer,
    "registeredTime": fields.DateTime,
    "executedTime": fields.DateTime,
    "success": fields.Boolean,
    "cashAmount": fields.Float
}

#Define the request parser for transactions
transaction_parser = reqparse.RequestParser()
transaction_parser.add_argument('source_account_id', type=int, required=True, help='Source account ID is required')
transaction_parser.add_argument('destination_account_id', type=int, required=True, help='Destination account ID is required')
transaction_parser.add_argument('amount', type=float, required=True, help='Transaction amount is required')

#Define the request parser for accounts
account_parser = reqparse.RequestParser()
account_parser.add_argument('name', type=str, required=True, help='Account name is required')
account_parser.add_argument('availableCash', type=float, default=0 , help='Account balance is required') 

class TransactionAPI(Resource):
    @marshal_with(transactionFields)    #Automatically formats the output to the fields defined above
    def get(self, transaction_id=None):
        if transaction_id:
            transaction = TransactionModel.query.filter_by(id=transaction_id).first()    #Get the transaction with the given id
            if not transaction:
                abort(404, message="Transaction not found")
        else:
            transaction = TransactionModel.query.all()    #If no id is given, return all transactions
        return transaction

    @marshal_with(transactionFields)    #Automatically formats the output to the fields defined above
    def post(self):
        args = transaction_parser.parse_args()
        if args["amount"] < 0:      #Check that the transaction amount is not negative
            abort(400, message="Negative transaction amount is not allowed") 
            
        registeredTime = datetime.now()
        source_Account = AccountModel.query.filter_by(id=args["source_account_id"]).first()      #Get the source account
        destination_Account = AccountModel.query.filter_by(id=args["destination_account_id"]).first()    #Get the destination account
        
        if not source_Account:
            abort(404, message="Source account not found")
        if not destination_Account:
            abort(404, message="Destination account not found")
            
        if source_Account.availableCash < args["amount"]:   #Check that the source account has enough funds, before executing transaction
            abort(400, message="Insufficient funds")    
        
        #Update the account balances
        source_Account.availableCash -= args["amount"]
        destination_Account.availableCash += args["amount"]
        executedTime = datetime.now()
        
        #Store transaction in the database
        Transaction = TransactionModel(
            sourceAccountId = args["source_account_id"],
            destinationAccountId = args["destination_account_id"],
            registeredTime = registeredTime,
            executedTime = executedTime,
            success = True,
            cashAmount = args["amount"]
        )
        db.session.add(Transaction)
        db.session.commit()
        
        return Transaction, 200

class AccountAPI(Resource):
    @marshal_with(accountFields)    #Automatically formats the output to the fields defined above
    def get(self, account_id = None):
        if account_id:
            account = AccountModel.query.filter_by(id = account_id).first()   #Get the account with the given id
            if not account:
                abort(404, message="Account not found")
        else:
            account = AccountModel.query.all()  #If no id is given, return all accounts
            
        return account
        
    @marshal_with(accountFields)    #Automatically formats the output to the fields defined above
    def post(self):
        args = account_parser.parse_args()
        if args["availableCash"] < 0:   #Check that the initial account balance is not negative
            abort(400, message="Negative ballance is not allowed")
        account = AccountModel(name=args["name"], availableCash=args["availableCash"])   
        db.session.add(account)
        db.session.commit()
        return account, 201
     
#Notes and potential additions:
#delete account, patch account (only name not balance), get all transactions for an account
#maybe store transactions with insufficient funds with success = False, downside: system may be flodded with failed transactions 
#require more options for transaction history managment. 
#authentication and/or authorization, each account has a password, each transaction must be signed by source account password, probably more sophisticated solutions as well
#race conditions, two transactions at the same time might lead to negative balance, maybe use locking mechanism

