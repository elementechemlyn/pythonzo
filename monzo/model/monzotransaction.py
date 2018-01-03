import datetime
from .monzomerchant import MonzoMerchant

class MonzoTransaction(object):

    def __init__(self,api,json_dict=None):
        self.api = api
        self.account_balance = None
        self.amount = None
        self.created = None
        self.currency = None
        self.description = None
        self.trans_id = None
        self.merchant_id = None
        self.merchant = None
        self.metadata = None
        self.notes = None
        self.is_load = None
        self.settled = None
        if json_dict:
            self.load(json_dict)
            
    @classmethod
    def retrieveTransaction(cls,api,trans_id,expand=None):
        trans_json = api.retrieveTransaction(trans_id,expand)
        return cls(api,trans_json["transaction"])

    def expand(self,expand="merchant"):
        trans_json = self.api.retrieveTransaction(self.trans_id,expand=expand)
        self.load(trans_json["transaction"])
    
    def load(self,json_dict):
        self.account_balance = int(json_dict["account_balance"])
        self.amount = int(json_dict["amount"])
        self.created = datetime.datetime.strptime(json_dict["created"],"%Y-%m-%dT%H:%M:%S.%fZ")
        self.currency = json_dict["currency"]
        self.description = json_dict["description"]
        self.trans_id = json_dict["id"]
        self.metadata = json_dict["metadata"]
        self.notes = json_dict["notes"]
        self.is_load = json_dict["is_load"]
        try:
            self.settled = datetime.datetime.strptime(json_dict["settled"],"%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            self.settled = json_dict["settled"]

        self.load_merchant(json_dict["merchant"])
        
    def load_merchant(self,merchant):
        if type(merchant) is dict:
            self.merchant_id = merchant["id"]
            self.merchant = MonzoMerchant(self.api,merchant)
        else:
            self.merchant_id = merchant
            self.merchant = None
            
