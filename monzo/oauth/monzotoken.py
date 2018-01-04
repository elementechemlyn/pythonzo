import requests
from .. import settings
import datetime

"""
TODO - This won't work for multiple users
Tokens need to be loaded for a specific user - not from settings.json
"""
class MonzoToken(object):

    def __init__(self,user_name=None,load_token=True):
        self.client_id = None
        self.client_secret = None
        self.redirect_url = None
        self.monzo_url = settings.settings["token_url"]

        self.access_token = None
        self.expires_in = None
        self.user_id = None
        self.refresh_token = None
        self.load_settings()
        if load_token:
            self.load_tokens(user_name)
            
    def load_settings(self):
        
        self.client_id = settings.settings["client_id"]
        self.client_secret = settings.settings["client_secret"]
        self.redirect_url = settings.settings["redirect_url"]
        
    def load_tokens(self,user_name):
        self.access_token = settings.settings.get("access_token",None)
        if self.access_token:
            expire_date = datetime.datetime.strptime(settings.settings["expires"],"%a %b %d %H:%M:%S %Y") 
            expires_in = expire_date - datetime.datetime.now()
            self.expires_in = expires_in.seconds
            self.refresh_token = settings.settings.get("refresh_token",None)
            if self.expires_in<1:
                self.access_token = None
                if self.refresh_token:
                    self.refresh_token()
        else:
            if load_token:
                raise Exception("No Access Token")
        
    def refresh(self):
        body = {
            "grant_type":"refresh_token",
            "client_id":settings.settings["client_id"],
            "client_secret":settings.settings["client_secret"],
            "refresh_token":self.refresh_token
        }
        resp = requests.post(self.monzo_url, data = body)
        if resp.status_code==200:
            resp_json = resp.json()
            self.access_token = resp_json["access_token"]
            settings.settings["access_token"] = self.access_token
            self.expires_in = resp_json["expires_in"]
            expire_datetime = datetime.datetime.now() + datetime.timedelta(seconds=int(self.expires_in))
            settings.settings["expires"] = expire_datetime.ctime()
            self.user_id = resp_json["user_id"]
            self.refresh_token = resp_json.get("refresh_token",None)
            if not self.refresh_token==None:
                settings.settings["refresh_token"] = self.refresh_token
            settings.save_settings()
            return int(self.expires_in)
        else:
            self.resp_text = resp.text()
            return 0

    def exchange_code(self,code):
        body = {
            "grant_type":"authorization_code",
            "client_id":settings.settings["client_id"],
            "client_secret":settings.settings["client_secret"],
            "redirect_uri":settings.settings["redirect_url"],
            "code":code
        }
        resp = requests.post(self.monzo_url, data = body)
        if resp.status_code==200:
            resp_json = resp.json()
            self.access_token = resp_json["access_token"]
            settings.settings["access_token"] = self.access_token
            self.expires_in = resp_json["expires_in"]
            expire_datetime = datetime.datetime.now() + datetime.timedelta(seconds=int(self.expires_in))
            settings.settings["expires"] = expire_datetime.ctime()
            self.user_id = resp_json["user_id"]
            self.refresh_token = resp_json.get("refresh_token",None)
            if not self.refresh_token==None:
                settings.settings["refresh_token"] = self.refresh_token
            settings.save_settings()
        else:
            self.resp_text = resp.text
