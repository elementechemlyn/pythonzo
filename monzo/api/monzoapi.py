from .. import settings
from ..oauth import monzotoken

import requests

class MonzoApiException(Exception):

    def __init__(self,http_code,code,message):
        self.code = code
        self.message = message
        
class MonzoApi(object):

    def __init__(self,monzo_token=None):
        if monzo_token==None:
            monzo_token = monzotoken.MonzoToken()
        self.token = monzo_token
        self.access_token = self.token.access_token
        self.end_point = settings.settings["api_url"]

    def is_authenticated(self):
        resp = self.whoami()
        return resp.get('authenticated',False)
        
    def makeApiCall(self,path,body=None):
        headers = {"Authorization":"Bearer %s" % self.access_token}
        if body==None:
            resp = requests.get(self.end_point + path,headers=headers)
        else:
            resp = requests.post(self.end_point + path,data=body,headers=headers)
        resp_json = resp.json()
        if resp.status_code==200:
            return resp_json
        else:
            raise MonzoApiException(resp.status_code,resp_json["code"],resp_json["message"])
    
    def whoami(self):
        resp = self.makeApiCall("/ping/whoami")
        return resp

    def listAccounts(self):
        resp = self.makeApiCall("/accounts")
        return resp
    
    def listPots(self):
        resp = self.makeApiCall("/pots/listV1")
        return resp

    def readBalance(self,account_id):
        resp = self.makeApiCall("/balance?account_id=%s" % account_id)
        return resp

    def listTransactions(self,account_id,pagination=None,expand=None):
        path = "/transactions?account_id=%s" % account_id
        if expand:
            path = path + "&expand[]=" + expand
        if pagination:
            path = path + "&" + str(pagination)
        resp = self.makeApiCall(path)
        return resp

    def retrieveTransaction(self,transaction_id,expand=None):
        path = "/transactions/%s" % (transaction_id,)
        if expand:
            path = path + "?expand[]=" + expand
        resp = self.makeApiCall(path)
        return resp

    def annotateTransation(self,transaction_id,metadata):
        pass

    def createFeedItem(self,account_id,item_type,params,url=None):
        pass

    def uploadAttachment(self,file_name,file_type):
        pass

    def registerAttachment(self,external_id,file_url,file_type):
        pass

    def deregisterAttachment(self,attachment_id):
        pass
    
    
