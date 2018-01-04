"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import abort, redirect, url_for,session,request,render_template
from .app import app
from ..oauth import monzotoken
from ..api import monzoapi
from ..model import monzoaccount
from ..model import monzobalance
from .. import settings
import uuid
from functools import wraps

#app = app.app

app.secret_key = "really stupid secret key"

def check_token():
    access_token = session.get("access_token",None)
    api = monzoapi.MonzoApi(access_token)
    if not api.is_authenticated():
        token = monzotoken.MonzoToken()
        api.access_token = token.access_token
        if not api.is_authenticated():
            token.refresh()
        session["access_token"] = token.access_token        
        return api.is_authenticated()
    else:
        return True

def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not check_token():
            state_token = uuid.uuid4()
            url = "https://auth.getmondo.co.uk/?client_id=%s&redirect_uri=%s&response_type=code&state=%s" % (settings.settings["client_id"],settings.settings["redirect_url"],state_token,)
            session["state"] = state_token
            return redirect(url, code=302)
        return f(*args, **kwargs)
    return wrapper

@app.route('/dashboard')
@app.route('/')
@authenticate
def dashboard():
    access_token = session.get("access_token",None)
    accounts = monzoaccount.MonzoAccount.listAccounts(monzoapi.MonzoApi(access_token))
    for account in accounts:
        account.readBalance()
    return render_template('dashboard.html',accounts=accounts)

@app.route('/account/<accountid>')
@authenticate
def show_account(accountid):
    access_token = session.get("access_token",None)
    account = monzoaccount.MonzoAccount.getAccount(monzoapi.MonzoApi(access_token),accountid)
    return render_template('account.html',account=account,transactions=account.listTransactionsThisMonth())

@app.route('/auth',methods=['POST', 'GET'])
def get_token():
    if request.method == 'POST': #Came from the form - get the code
        code = request.form['code']
        state = request.form['state']
    else:
        code = request.args.get('code', None)
        state = request.args.get('state', None)
        if code==None: #Show the form to take a code
            return render_template('getcode.html',state=state)
    
    #Now we have a code - check the status then do the exhange
    session_state = str(session.pop("state","None"))
    if state != session_state:
        return "State wrong!"

    #Don't attempt to load the token (we don't have one yet!)
    token = monzotoken.MonzoToken(load_token=False)
    token.exchange_code(code)
    if token.access_token==None:
        return token.resp_text
    else:
        session["access_token"] = token.access_token
        return redirect("/dashboard",code=302)



    
    
