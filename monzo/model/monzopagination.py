import datetime

class MonzoPaging(object):

    def __init__(self):
        self.limit = None # integer
        self.before = None # iso date string
        self.since_date = None # iso date string
        self.since_trans = None #string

    def __str__(self):
        return self.get_param_string()
    
    def set_limit(self,limit):
        self.limit = int(limit)

    def set_before(self,before_dt):
        before_dt = before_dt.replace(microsecond=0)
        self.before = before_dt.isoformat("T") + "Z"

    def set_since_date(self,since_dt):
        since_dt = since_dt.replace(microsecond=0)
        self.since_date = since_dt.isoformat("T") + "Z"

    def set_since_trans(self,trans_id):
        self.since_trans = trans_id
        
    def get_param_string(self):
        params = []
        if self.limit!=None:
            params.append("limit=%s" % (self.limit,))
        if self.before!=None:
            params.append("before=%s" % (self.before,))
        if self.since_date!=None:
            params.append("since=%s" % (self.since_date,))
        elif self.since_trans!=None:
            params.append("since=%s" % (self.since_trans,))

        return "&".join(params)
    
