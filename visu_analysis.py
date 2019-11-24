
from db import conn ,user_events,user_rating,insert_event,rate_insert,recommendation
import datetime
import pandas as pd
import json
#list of list to one list 
def list_only(li):
    return [y for x in li for y in x]

#find average of dataframe if column rating exists in dataframe
def average(df):
    if 'rating' in df.columns:
        return df.rating.mean()
    else:
        return 0


#filter events by time/date in descending order and calculate aggerate number of events  
def filter(df):
    if df.empty:
        return  
    else:
        df.pop('_id')
        df.pop('__v')
        df.sort_values( by=['time'] , ascending  = False,inplace=True)
        df.pop('time')
        df.drop_duplicates(keep='first',inplace=True)
        #print(df)
        dups_evn = df.pivot_table(index=['eventType'], aggfunc='size')
        df = pd.DataFrame(dups_evn , columns=['repi'])
        df.reset_index(level=0, inplace=True)
        return df

def events_agg(df):
    if df.empty:
        df['eventType'] = ["SAVE","OFFICIAL_LINK","VIEWED","UNSAVE","RELEVANT",'NOT_RELEVANT']
        df["repi"] = [0,0,0,0,0,0]
    resp = {}
    a =  ["SAVE","OFFICIAL_LINK","VIEWED","UNSAVE","RELEVANT",'NOT_RELEVANT']
    b = list(df['eventType'])
    A = set(a)
    B = set(b)
    C = list(A-B)
    value = [0 for i in range(len(C))]
    dis = dict(zip(C,value))
    df_json = df.to_dict('records')
    for row in df_json:
        attr = row.get('eventType')
        val = row.get('repi')
        resp.update({attr:val})
    resp.update(dis)
    return resp 


today =datetime.datetime.today()
ke = recommendation()
uids=[]
collab=[]
cosine = []
alls = []
cat=[]
dates = []
for i in range(len(ke)):
    uid = ke[i].get('user')
    uids.append(uid)  #user ids in db
    collabs = ke[i].get('collab')
    collab.append(collabs) #collaboratie ids
    cosines = ke[i].get('cosine')
    cosine.append(cosines) #cosine ids
    all_d = ke[i].get('all')
    alls.append(all_d) # collab+ cosine
    cats = ke[i].get('cat')
    cat.append(cats)   #categories data from api 
    dates_1 = ke[i].get('date')  #date of data
    dates.append(dates_1)


cl = []
cs=[] #cosine 
cca =[] #collab + cosines all
apis =[] #api ids data
date_db =[]

for i in range(len(uids)):
    user_events_colloab = user_events(collab[i],uids[i])  
    cl.append(list(user_events_colloab)) #list of user event collob filtering
    user_events_cosine = user_events(cosine[i],uids[i])
    cs.append(list(user_events_cosine)) #user event list of cosine similarity
    user_events_colab_cosine = user_events(alls[i],uids[i])
    cca.append(list(user_events_colab_cosine)) #user event of collab and cosine
    user_events_categories = user_events(cat[i],uids[i])
    apis.append(list(user_events_colab_cosine)) #user events of categories

#############################
flattened_list_collab = list_only(cl) #collab
df1 = pd.DataFrame(flattened_list_collab)
collab_event = filter(df1)   #dataframe of collaborative filtering events 
#############################
flattened_list_cosine = list_only(cs) #cosine
df = pd.DataFrame(flattened_list_cosine)
cosine_event = filter(df)    #dataframe of cosinesimilarity events 
################################
flattened_list_colab_cosine = list_only(cca) #collab cosine
df2 = pd.DataFrame(flattened_list_colab_cosine)
colab_cosine_event = filter(df2) # dataframe of colaborative and cosine events
###################################
flattened_list_api = list_only(apis) #catagories 
df3 = pd.DataFrame(flattened_list_api)
api_event = filter(df3) # dataframe of categories recomended events 
################################

col_r  = events_agg(collab_event)
cos_r =events_agg(cosine_event)
cc_r = events_agg(colab_cosine_event)
c_r =events_agg(api_event)

events=[{
    "time":today,
    "collab": col_r,
    "cosine":cos_r,
    "colab_cosine_event":cc_r,
    "categories":c_r,
}]
print(events)
# insert_event(events)


# #################Find Mean of dataset 
clr = []
csr=[] #cosine 
ccar =[] #collab + cosines all
apisr =[] #api ids data
date_dbr =[]

for i in range(len(uids)):
    user_rating_colloab = user_rating(collab[i],uids[i])
    clr.append(list(user_rating_colloab)) #list of user event collob filtering
    user_rating_cosine = user_rating(cosine[i],uids[i])
    csr.append(list(user_rating_cosine)) #user event list of cosine similarity
    user_rating_colab_cosine = user_rating(alls[i],uids[i])
    cca.append(list(user_rating_colab_cosine)) #user event of collab and cosine
    user_rating_categories = user_rating(cat[i],uids[i])
    apis.append(list(user_rating_categories)) #user events of categories

########################
flattened_list_collabr = list_only(clr) #collab
collab_rate = pd.DataFrame(flattened_list_collabr)
flattened_list_cosiner = list_only(csr) 
cosine_rate = pd.DataFrame(flattened_list_cosiner)
flattened_list_collabr = list_only(ccar) 
collab_cosine_rate = pd.DataFrame(flattened_list_collabr)
flattened_list_collabr = list_only(apisr)
api_rate = pd.DataFrame(flattened_list_collabr)

#find average of all dataframe 
ratings_average_collab =average(collab_rate)
ratings_average_cosine = average(cosine_rate)
ratings_average_collabCosine = average(collab_cosine_rate)
ratings_average_catrate = average(api_rate)

############# Insert yesterday recomended events to database collection named analysis


dataset = [{
        'time':today,
        'ratings_average_collab': ratings_average_collab,
        'ratings_average_cosine':ratings_average_cosine,
        'ratings_average_collabCosine':ratings_average_collabCosine,
        'ratings_average_category':ratings_average_catrate
        }]

# rate_insert(dataset)



