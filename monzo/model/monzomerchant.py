import datetime

class MonzoMerchantAddress(object):

    def __init__(self,address):
        self.address = address["address"]
        self.city = address["city"]
        self.country = address["country"]
        self.latitude = address["latitude"]
        self.longitude = address["longitude"]
        self.postcode = address["postcode"]
        self.region = address["region"]
        
class MonzoMerchant(object):

    def __init__(self,api,json_dict=None):
        self.api = api
        self.address = None
        self.created = None
        self.group_id = None
        self.merchant_id = None
        self.logo = None
        self.emoji = None
        self.name = None
        self.category = None
        if json_dict:
            self.load(json_dict)

    def load(self,json_dict):
        self.address = MonzoMerchantAddress(json_dict["address"])
        self.created = datetime.datetime.strptime(json_dict["created"],"%Y-%m-%dT%H:%M:%S.%fZ")
        self.group_id = json_dict["group_id"]
        self.merchant_id = json_dict["id"]
        self.logo = json_dict["logo"]
        self.emoji = json_dict["emoji"]
        self.name = json_dict["name"]
        self.category = json_dict["category"]
        
