import monzo.oauth.monzotoken as monzotoken
import monzo.api.monzoapi as monzoapi
import monzo.model.monzotransaction as monzotransaction
import monzo.model.monzoaccount as monzoaccount
import monzo.model.monzobalance as monzobalance

api = monzoapi.MonzoApi()

if not api.is_authenticated():
    raise Exception("API Not authenticated!")

accounts = monzoaccount.MonzoAccount.listAccounts(api)
for a in accounts:
    if a.account_type=="uk_retail":
        account = a
        break

print(a.readBalance())
transactions = a.listTransactions()
balance = monzobalance.MonzoBalance(a.account_id)
print(balance)

t = transactions[1]
print(t.trans_id)

t = monzotransaction.MonzoTransaction.retrieveTransaction(api,t.trans_id)
print(t.merchant)
t.expand()
print(t.merchant)
