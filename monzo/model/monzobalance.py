class MonzoBalance(object):

    def __init__(self,api,json_dict=None):

        self.api = api
        self.local_currency = None
        self.local_exchange_rate = None
        self.total_balance = None
        self.local_spend = []
        self.balance = None
        self.currency = None
        self.spend_today = None
        if json_dict:
            self.load(json_dict)
            
    @classmethod
    def readBalance(cls,api,account_id):
        balance_json = api.readBalance(account_id)
        return cls(api,balance_json)
    
    def load(self,json_dict):
        self.local_currency = json_dict["local_currency"]
        self.local_exchange_rate = json_dict["local_exchange_rate"]
        self.total_balance = int(json_dict["total_balance"])
        self.local_spend = json_dict["local_spend"]
        self.balance = int(json_dict["balance"])
        self.currency = json_dict["currency"]
        self.spend_today = int(json_dict["spend_today"])
        
