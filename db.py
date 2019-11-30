import pymongo
import datetime
import pandas as pd
# connect to mongo db database
def conn():
    mongo = pymongo.MongoClient("mongodb://localhost:27017/oyaop")
    db = mongo["oyaop"]  # database name
    return db


# search events of given date range for the given 
def event_search(isodate,isodate2,search_attribute , attr):
    db = conn()
    analysis_event = db["event_analysis"] 
    e = analysis_event.find({"time":{ "$gte": isodate, "$lte": isodate2}}, {search_attribute:1} ).sort('date',1)
    li = list(e)
    df = pd.DataFrame(li)
    l = list(df.iloc[:,1])
    value = [d[attr] for d in l]
    return value

# finds event of given time range and sorts them in ascending order
def time(isodate ,isodate2):
    db =conn()
    analysis_event = db["event_analysis"] 

    time = analysis_event.find({"time":{ "$gte": isodate, "$lte": isodate2}},{"time":1}).sort('date',1)

    tdf = list(time)
    time_ev = [d['time'] for d in tdf]
    return time_ev

# finds 
def rate_time(isodate,isodate2):
    db=conn()
    analysis = db["rate_analysis"]
    rate = analysis.find({"time":{ "$gte": isodate, "$lte": isodate2} })
    return list(rate)

def user_events(u1test,uid): # user events in 24 hrs 
    db=conn()
    events_db = db["events"] 
    x = events_db.find({'$and':[{'userId':uid} , { "postId": { "$in": u1test } }]  }  )
    return list(x)


def user_rating(recid,uids ):  #ratings search grom ra = ratings_new
    db=conn()
    ra = db['ratings_new']
    lo = ra.find({'$and':[{'user_id': uids }, { "post_id": { "$in": recid } }]  }  ) 
    return list(lo)

# Inserts No of events  calculated for visualization

def insert_event(events):
    db = conn()
    analysis_event = db["event_analysis"] 
    analysis_event.insert_many(events)

# Inserts average ratings calculated for visualization
def rate_insert(dataset):
    db = conn()
    analysis = db["rate_analysis"]
    analysis.insert_many(dataset)
 
# finds all  yesterday recommended posts from databse
def recommendation():
    db=conn()
    recommendation = db['recommended']
    x = recommendation.find({})
    ke = list(x)
    return ke


# finds all events heppened yesterday for the recommended posts
def f_events():
    db = conn()
    event= db['events']
    x = event.find({})
    return list(x)


# def f_events(isodate, isodate2):
#     db = conn()
#     event= db['events']
#     event.find({"time":{ "$gte": isodate, "$lte": isodate2} })
#     return list(event)


# finds all post title and id  for given list of array(post ids)
def posts(array):
    db=conn()
    event= db['posts']
    x = event.find({"id":{"$in":array}},{"title":1,"id":1})
    return list(x)