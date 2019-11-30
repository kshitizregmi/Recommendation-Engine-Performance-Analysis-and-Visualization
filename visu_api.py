from flask import Flask,render_template,request
from db import event_search,conn,time,rate_time,f_events,posts
import datetime
app = Flask(__name__, template_folder="templates")
import pandas as pd
from datetime import timedelta
from collections import Counter
db=conn()
event= db['posts']

#define function necessary
# calculate id occurance for trend
def calculate_id_occurence(df):
    obj=[]
    event = list(df.eventType.unique()) 
    s=[]
    for i in range(len(event)):
        s=[]
        eventType = df[df["eventType"] == event[i]]
        # print(eventType)
        sav = list(eventType.postId)
        c = Counter(sav)
        p = c.most_common(50)
        s= list(zip(*p))
        tmp = {"type":event[i],"postid":list(s[0]) ,"hits":list(s[1]) }
        obj.append(tmp)
        # return json of event type post id and no of hits on that post id
    return obj

#find id and title of given array of post ids
def search_title(array):
    x = event.find({"id":{"$in":array}},{"title":1,"id":1})
    return list(x)

# dataframe decomposition and make new dataframe with id its event type and no of hits 
def break_df(x,i):
    pid = x.iloc[i].pid
    et = x.iloc[i].eventType
    hit = x.iloc[i].hits
    js =  {
        "id":pid,
        "eventType":et,
        "hits":hit

    }
    df = pd.DataFrame.from_dict(js)
    return df

# joins two dataframe
def Joindf(x,y):
    notrel = pd.merge(x, y, how='inner',on='id')
    df = notrel.drop_duplicates(keep='first')
    return df

# return json of id its event type no of hits on that id and its title 
def data(df):
    notrelv = {
    "id":list(df.id),
    "eventType":list(set(df.eventType)),
    "hits":list(df.hits),
    "title":list(df.title)
    }
    return notrelv



@app.route('/', methods=['POST','GET'])
def index():
    print(request.method)
    if  request.method == 'GET':

        isodate = datetime.datetime.now()-timedelta(days = 25)
        isodate2 = datetime.datetime.now()
        
    else:
        f_day = request.form.get('fday')
        t_day = request.form.get('tday')

        if f_day == "" or t_day=="":
            isodate = datetime.datetime.now()-timedelta(months = 3)
            isodate2 = datetime.datetime.now()
        else:

            isodate = datetime.datetime.strptime(f_day,'%Y-%m-%d')
            isodate2 = datetime.datetime.strptime(t_day,'%Y-%m-%d')
    time_ev = time(isodate ,isodate2)


# finds events at given range of datetime for different approach of recommendatiion (collaborative , cosine , collab cosine , category )
# and post events 
    ###############################
    colab_save=event_search(isodate,isodate2,"collab.SAVE","SAVE")
    cosine_save = event_search(isodate,isodate2,"cosine.SAVE","SAVE")
    colab_cosine_save = event_search(isodate,isodate2,"colab_cosine_event.SAVE","SAVE") 
    categories_save =event_search(isodate,isodate2,"categories.SAVE","SAVE") 
    ########################################################
    colab_NOT_RELEVANT=event_search(isodate,isodate2,"collab.NOT_RELEVANT","NOT_RELEVANT")
    cosine_NOT_RELEVANT = event_search(isodate,isodate2,"cosine.NOT_RELEVANT","NOT_RELEVANT")
    colab_cosine_NOT_RELEVANT = event_search(isodate,isodate2,"colab_cosine_event.NOT_RELEVANT","NOT_RELEVANT") 
    categories_NOT_RELEVANT = event_search(isodate,isodate2,"categories.NOT_RELEVANT","NOT_RELEVANT") 
    ###########################################################
    colab_RELEVANT = event_search(isodate,isodate2,"collab.RELEVANT","RELEVANT")
    cosine_RELEVANT = event_search(isodate,isodate2,"cosine.RELEVANT","RELEVANT")
    colab_cosine_RELEVANT = event_search(isodate,isodate2,"colab_cosine_event.RELEVANT","RELEVANT") 
    categories_RELEVANT = event_search(isodate,isodate2,"categories.RELEVANT","RELEVANT") 
    #############################################################
    colab_VIEWED =event_search(isodate,isodate2,"collab.VIEWED","VIEWED")
    cosine_VIEWED = event_search(isodate,isodate2,"cosine.VIEWED","VIEWED")
    colab_cosine_VIEWED = event_search(isodate,isodate2,"colab_cosine_event.VIEWED","VIEWED") 
    categories_VIEWED = event_search(isodate,isodate2,"categories.VIEWED","VIEWED") 
    #################################################################
    colab_OFFICIAL_LINK = event_search(isodate,isodate2,"collab.OFFICIAL_LINK","OFFICIAL_LINK")
    cosine_OFFICIAL_LINK = event_search(isodate,isodate2,"cosine.OFFICIAL_LINK","OFFICIAL_LINK")
    colab_cosine_OFFICIAL_LINK = event_search(isodate,isodate2,"colab_cosine_event.OFFICIAL_LINK","OFFICIAL_LINK") 
    categories_OFFICIAL_LINK = event_search(isodate,isodate2,"categories.OFFICIAL_LINK","OFFICIAL_LINK")
    ################################################################
    colab_UNSAVE=event_search(isodate,isodate2,"collab.UNSAVE","UNSAVE")
    cosine_UNSAVE = event_search(isodate,isodate2,"cosine.UNSAVE","UNSAVE")
    colab_cosine_UNSAVE = event_search(isodate,isodate2,"colab_cosine_event.UNSAVE","UNSAVE") 
    categories_UNSAVE =event_search(isodate,isodate2,"categories.UNSAVE","UNSAVE") 

# put all values avobe to json with time 
    event_json = {
        "time_ev":time_ev,

        "c_save":colab_save,
        "cs_save":cosine_save,
        "cc_save":colab_cosine_save,
        "cat_save":categories_save,

        "c_notRelevent":colab_NOT_RELEVANT,
        "cs_notRelevent":cosine_NOT_RELEVANT,
        "cc_notRelevent":colab_cosine_NOT_RELEVANT,
        "cat_notRelevent":categories_NOT_RELEVANT,

        "c_relevent":colab_RELEVANT,
        "cs_relevent":cosine_RELEVANT,
        "cc_relevent":colab_cosine_RELEVANT,
        "cat_relevent ":categories_RELEVANT,

        "c_seen":colab_VIEWED,
        "cs_seen":cosine_VIEWED,
        "cc_seen":colab_cosine_VIEWED,
        "cat_seen ":categories_VIEWED,

        "c_offLink":colab_OFFICIAL_LINK,
        "cs_offLink":cosine_OFFICIAL_LINK,
        "cc_offLink":colab_cosine_OFFICIAL_LINK,
        "cat_offLink":categories_OFFICIAL_LINK,

        "c_unsave":colab_UNSAVE,
        "cs_unsave":cosine_UNSAVE,
        "cc_unsave":colab_cosine_UNSAVE,
        "cat_unsave":categories_UNSAVE
    }
    keys =list(event_json.keys()) # event_json variable keys 


    keys1={
        "keys":keys     # event_json variable keys in json format
    }
    
    rates = rate_time(isodate,isodate2) # find rating for given date range

    time_event = []
    collab_rate=[]
    cosine_rate=[]
    collab_cosine_rate =[]
    category_rate = []
    for i in range(len(rates)):
        time_event.append(rates[i]['time']) # find all the date in database of given range of date
        collab_rate.append(rates[i]['ratings_average_collab']) # find average rating of colloborative for given range of date from database
        cosine_rate.append(rates[i]['ratings_average_cosine'])  # find average rating of cosine for given range of date from database
        collab_cosine_rate.append(rates[i]['ratings_average_collabCosine']) # find average rating of colloborative + coine for given range of date from database
        category_rate.append(rates[i]['ratings_average_category']) # find average rating of category for given range of date from database
# make json of each value 
    rate_json = {
        "time":time_event,
        "collab":collab_rate,
        "cosine":cosine_rate,
        "collab_cosine":collab_cosine_rate,
        "category": category_rate
    }
# throw all values in vis.html template to render/ plot
    return render_template('visualizegraph.html',eve =  event_json ,rat = rate_json , keys=keys1 )



@app.route('/trend', methods=['GET'])
def trend():
    # delete duplicate event data and calculate their occurance 
    print(request.method)
    df= pd.DataFrame(f_events())
    df.pop('_id')
    df.pop('__v')
    df.head()
    df.sort_values( by=['time'] , ascending  = False ,inplace=True)
    df.pop('time')
    df.drop_duplicates(keep='first',inplace=True)
    df.sort_values(by=['eventType','postId'] , ascending  = True ,inplace=True)
    details = calculate_id_occurence(df)

    print(details)
    li =[]
    for i in range(len(details)):
        li.append(list(details[i].values()))

    x = pd.DataFrame(li,columns=['eventType','pid','hits'])

    # dataframe(x)  decomposition and make new dataframe with id its event type and no of hits 

    NOT_RELEVANT = break_df(x,0)
    OFFICIAL_LINK = break_df(x,1)
    RELEVANT = break_df(x,2)
    SAVE = break_df(x,3)
    UNSAVE = break_df(x,4)
    VIEWED = break_df(x,5)

    list_of_postid = list(x.pid)
    tem=[]
    #search title in db
    for i in range(len(list_of_postid )):
        x = search_title(list_of_postid[i])
        tem.append(x)

#   list of list to list
    print(tem)
    flatno = [y for x in tem for y in x]
    idtitle = pd.DataFrame(flatno)
    idtitle.pop('_id')
    idtitle.drop_duplicates(inplace=True)
    KEY_VAL =[]
    for i in range(len(list_of_postid)):
        idtit = idtitle[idtitle['id'].isin(li[i][1])]
        id_title_json =idtit.to_dict('records')
        KEY_VAL.append(id_title_json)

    new = [y for x in KEY_VAL for y in x]
    all_df = pd.DataFrame(new)

    # inner join two dataframe  and make one 
    notrel = Joindf(NOT_RELEVANT,all_df )
    off = Joindf(OFFICIAL_LINK,all_df )
    rel = Joindf(RELEVANT,all_df )
    save = Joindf(SAVE,all_df )
    unsave = Joindf(UNSAVE,all_df )
    view = Joindf(VIEWED,all_df )

    # return json of id its event type no of hits on that id and its title 
    n_rel = data(notrel)
    offlink = data(off)
    relevent = data(rel)
    saves = data(save)
    unsaves = data(unsave)
    viewes = data(view)
    return render_template('trend.html',n_rel =n_rel,offlink = offlink, relevent = relevent ,saves = saves, unsaves = unsaves,viewes = viewes )




if __name__ == '__main__':
    app.run(debug=True)