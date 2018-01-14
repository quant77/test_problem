import json
from wsgiref import simple_server
import falcon
import requests
from pprint import pprint as pp
import numpy as np

class StorageEngine(object):
    def __init__(self):
        self.store = {} 

    def add_thing(self, thing):
        if len(self.store.keys()) == 0: current =0
        else: current = max(self.store.keys()) 
        self.store[current+1] = thing


def reputes_type(db, rtype, nr):
    '''
    for a given name_of_reputee(nr), return reputes of particular type(rtype) = reach or clarity
    ''' 
    return [i for i in db.store.values() if i['reputee'] == nr and i["repute"]['feature'] ==rtype]

def values_for_rid(reputes):
    '''
    return values for reputes and amount of unique values(rid's)
    it is assumed that reputes already belong to particular type(reach/clarity)
    '''
    rids=[];values=[]
    for i in reputes:
        if i['repute']['rid'] not in rids:
            rids.append(i['repute']['rid']); values.append(i['repute']['value'])    
    return values , len(rids)        

def S(a,b,x):
    '''
    S function as described in the notes
    perhaps, bounds have to be verified
    ''' 
    if a>=x: return 0
    if x>=a and ((a+b)/2.0) >= x : return 2*((x-a)/float(b-a))**2
    if x >= ((a+b)/2.0) and b>=x : return  1 - 2*((x-a)/float(b-a))**2
    if x >= b : return 1 

class ThingsResource(object):

    def __init__(self, db):
        self.db = db
        
    def on_get(self, req, resp):
    
        try:
            doc = json.loads(req.stream.read())

        except KeyError:
            raise falcon.HTTPBadRequest('Missing thing','A thing must be submitted in the request body.')
         
        name_of_reputee = doc["reputee"] # get reputee name
        reputes_r= reputes_type(self.db, 'reach', name_of_reputee)
        reputes_c= reputes_type(self.db,'clarity', name_of_reputee)
        values_r , x_r = values_for_rid(reputes_r); values_c, x_c = values_for_rid( reputes_c)
        
        
        reach_score = np.mean(values_r); reach_conf = S(a = 2, b = 6, x = x_r) 
        clarity_score = np.mean(values_c) ;  clarity_conf = S(a = 4, b = 8, x = x_c)
        clout_score = 0.1*(reach_score*reach_conf + clarity_score*clarity_conf)/float(reach_conf + clarity_conf)
        clout_conf = min(reach_conf,clarity_conf)
        pp(reputes_r);pp(reputes_c);pp(values_r); pp(values_c)
                
        
        result = {"reputee":  name_of_reputee,
                  "clout": {       
                    "score": clout_score, 
                    "confidence": clout_conf  },
                  "reach": {       
                    "score": reach_score,
                    "confidence": reach_conf    },
                  "clarity":      {       
                    "score": clarity_score,
                    "confidence": clarity_conf    }}
        resp.media = result #resp.context['result'] = result
        resp.status = falcon.HTTP_200
    

    def on_post(self, req, resp): 
        try:
            doc = json.loads(req.stream.read())#json.loads(req.stream.read().decode('utf-8'));

        except KeyError:
            raise falcon.HTTPBadRequest('Missing thing','A thing must be submitted in the request body.')

        proper_thing = self.db.add_thing(doc)
        resp.status = falcon.HTTP_201


app = falcon.API()
db = StorageEngine()
things = ThingsResource(db)
app.add_route('/things', things)
#app.add_error_handler(StorageError, StorageError.handle)
#app.add_sink(sink, r'/search/(?P<engine>ddg|y)\Z')

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()