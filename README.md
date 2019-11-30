# Project

Recommendation system/Engine Performance analysis and Visualization.

## 
## Description about Recommendation System

Recommendation system used is a hybrid system that works with algorithm called Single Value Decomposition (SVD), and Cosine Similarity (= Bag of words). 

User using the app selects the category of opportunity, and we track all activity that the user does, (activity like view the opportunity, save the opportunity, click relevant on that opportunity, click irrelevant on that opportunity, and visit official link of that opportunity) in that app.

We do data cleaning and use recommendation system to predict best possible opportunity for given user id using SVD and Cosine Similarity. 

If recommendation engine do not generate any recommendation (In worst case) we recommend only those opportunity of selected category with latest deadlines. If recommendation engine generates the recommendation we append those opportunity of selected category with latest deadlines, with recommended opportunity.

## Technology Used
1.	Python
2.	Pandas 
3.	HTML 
4.	CSS
5.	Javascript
6.	Chart.Js

## Database Used

•	MongoDB

## Files
1.	visu_analysis.py

2.	visu_api.py

3.	db.py

4.	templates

    -	visualizegraph.html

    -	trend.html
  

# visu_analysis.py

> Functions:


1.	Finds average of ratings calculated for recommendation system for all user. Types of ratings average:
  -	Ratings average of Collaborative filtering algorithm recommended posts.
  -	Ratings average of Cosine Similarity algorithm recommended posts.
  -	Ratings average of Cosine Similarity algorithm + Collaborative filtering algorithm recommended posts.
  -	Ratings average of selected category post with latest deadline.

For example,
```
[

{

'time': datetime.datetime(2019, 11, 30, 12, 40, 9, 846748),

 'ratings_average_collab': 5.783333333333333,
 
 'ratings_average_cosine': 2.6666666666666665, 
 
'ratings_average_collabCosine': 4.65645, 

'ratings_average_category': 0

}

]

```


2.	Finds the total number of posts events that occured in yesterday's recommendation.
 -  Post events: "SAVE","OFFICIAL_LINK","VIEWED","UNSAVE","RELEVENT","NOT_RELEVENT"
 

  For example,
```
[

{

'time': datetime.datetime(2019, 11, 30, 12, 22, 35, 611532),

 'collab': {
 
'OFFICIAL_LINK': 17, 

'RELEVANT': 31, 

'SAVE': 23, 

'UNSAVE': 6, 

'VIEWED': 94, '

NOT_RELEVANT': 2

}
, 

'cosine': {

'OFFICIAL_LINK': 1, 

'RELEVANT': 4,

 'SAVE': 6, 
 
'UNSAVE': 4, 

'VIEWED': 18, '

NOT_RELEVANT': 6

},

'colab_cosine_event': {

'NOT_RELEVANT': 9,

 'OFFICIAL_LINK': 37,
 
 'RELEVANT': 22, 
 
'SAVE': 64, 

'UNSAVE': 10, 

'VIEWED': 94

},

 'categories': {
 
'NOT_RELEVANT': 5,

 'OFFICIAL_LINK': 8, 
 
'RELEVANT':2 ,

 'SAVE': 1,
 
 'UNSAVE': 10, 
 
'VIEWED': 30

}
}
]
```

**All this information are stored in database for plotting.**


## visu_api.py
***
It uses visualizegraph.html to render html template and plot graph using chart.js

  1.	Plots bar chart and line chart for average ratings progress for given time range (default = 7 days).

  2.	Plots line chart for number of events occurring for given time range (default = 7 days).

    -	Line Chart of number of Events in Collaborative filtering
  
    -	Line Chart of number of Events in Cosine Similarity
  
    -	Line Chart of number of Events in Collaborative and Cosine Similarity
  
    -	Line Chart of number of Events in catagories
  
  3.	Finds trending Post  with events: "SAVE","OFFICIAL_LINK","VIEWED","UNSAVE","RELEVENT","NOT_RELEVENT"

    -	It uses trend.html to render html template and view trend in events.
    -	http://127.0.0.1:5000/trend

***

## db.py

This file contains all the database query for this project. I have used MongoDB database.

## Output

The output of this project is on file:

- Engine Working Analysis.pdf

- trend.pdf

