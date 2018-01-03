import datetime
from .monzobalance import MonzoBalance
from .monzopagination import MonzoPaging
from .monzotransaction import MonzoTransaction

class MonzoAccount(object):

    def __init__(self,api,json_dict=None):
        self.api = api
        self.account_id = None
        self.created = None
        self.description = None
        self.account_type = None
        self.balance = None
        
        if json_dict:
            self.account_id = json_dict.get("id",None)
            self.description = json_dict.get("description",None)
            self.account_type = json_dict.get("type",None)
            self.created = json_dict.get("created",None)
            if self.created:
                self.created = datetime.datetime.strptime(self.created,"%Y-%m-%dT%H:%M:%S.%fZ")
        
    @classmethod
    def listAccounts(cls,api):
        accounts = []
        accounts_json = api.listAccounts()
        for account_json in accounts_json["accounts"]:
            account = cls(api,account_json)
            accounts.append(account)
        return accounts

    @classmethod
    def getAccount(cls,api,account_id):
        accounts_json = api.listAccounts()
        for account_json in accounts_json["accounts"]:
            account = cls(api,account_json)
            if account.account_id == account_id:
                account.readBalance()
                return account
        return None
        
    def readBalance(self):
        balance_json = self.api.readBalance(self.account_id)
        self.balance =  MonzoBalance(self.api,balance_json)
        return self.balance

    def listTransactionsThisMonth(self,expand=None):
        now = datetime.datetime.now()
        this_month = now.replace(day=1,hour=0,minute=0,second=0,microsecond=0)
        page = MonzoPaging()
        page.set_since_date(this_month)
        return self.listTransactions(page,expand)

    def listTransactionsToday(self,expland=None):
        now = datetime.datetime.now()
        today = now.replace(hour=0,minute=0,second=0,microsecond=0)
        page = MonzoPaging()
        page.set_since_date(today)
        return self.listTransactions(page,expand)

    def listTransactionSinceDate(self,from_dt,expand=None):
        page = MonzoPaging()
        page.set_since_date(from_dt)
        return self.listTransactions(page,expand)

    def listTransactionsSinceTransaction(self,trans_id,expand=None):
        page = MonzoPaging()
        page.set_since_trans(trans_id)
        return self.listTransactions(page,expand)

    def listTransactionsBetween(self,since_dt,to_dt,expand=None):
        page = MonzoPaging()
        page.set_since_date(since_dt)
        page.set_before(to_dt)
        return self.listTransactions(page,expand)
        
    def listTransactions(self,pagination=None,expand=None):
        transactions = []
        transactions_json = self.api.listTransactions(self.account_id,pagination,expand)
        for transaction_json in transactions_json["transactions"]:
            transaction = MonzoTransaction(self.api,transaction_json)
            transactions.append(transaction)
            
        return transactions
    
    
