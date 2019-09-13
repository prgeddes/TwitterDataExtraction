#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 10:37:20 2019

@author: paul
"""
# import relevant packages
from TwitterAPI import TwitterAPI
import pandas as pd
import json
i = 0       # counter
requestlist = []    # list for storing each call from the api (500 tweets at a time)

# search Criteria
SEARCH_TERM = ''
PRODUCT = 'fullarchive'
LABEL = 'Research'


#API keys to authorise and access the API
consumerKey=""
consumerSecret=""
accessToken=""
accessSecret=""

#Code to initiate API
api = TwitterAPI(consumerKey, consumerSecret, 
                  accessToken, accessSecret)
# loop which makes successive api calls based on amount of results 
while True:
    if i == 0 :
        requestlist.append(api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL), 
                {'query':SEARCH_TERM,
                 'fromDate': '201408220000',
                 'toDate': '201408310000',
                 'maxResults': 500}))
    
    else: 
        if requestlist[i-1].json().get('next') == None :
            break
        else: 
            requestlist.append(api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL), 
                    {'query':SEARCH_TERM,
                     'fromDate': '201408220000',
                     'toDate': '201408310000',
                     'maxResults': 500, 
                     'next':requestlist[i-1].json()['next']}))
        
    i +=1 
#save each payload to csv
for payload in requestlist:
    df = pd.read_json(json.dumps(payload.json()['results']))
    df.to_csv("acsvfile.csv", mode = 'a')
