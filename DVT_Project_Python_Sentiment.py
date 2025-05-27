# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 10:42:54 2023

@author: vafeas
"""

import torch
import pandas as pd
import numpy as np
import csv
import string
import nltk
import nt
from nltk.sentiment import SentimentIntensityAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
from transformers import pipeline



import warnings
warnings.filterwarnings("ignore")


#data = pd.read_csv(r"data for Sentiment Analysis\ChatGPT_generated_fake_DVT_data.csv")      
file_text = pd.read_table(r"data\ChatGPT_generated_fake_DVT_data.txt")
N = len(file_text)
#size = 

list_of_column_names = file_text.columns.values
column_names = list_of_column_names[0].split(',')
data = pd.DataFrame(columns = column_names, index = range(0,N)) 
for index, row in file_text.iterrows():
    a = file_text.iloc[index].str.split(',').tolist() 
    data['PAT_ID'][index] = a[0][0]
    data['PAT_MRN_ID'][index] =  a[0][1] 
    data['ORDER_PROC_ID'][index] = a[0][2]
    data['ORDER_TIME'][index] = a[0][3]
    data['RESULT_TIME'][index] = a[0][4]
    data['DESCRIPTION'][index] = a[0][5]
    data['RESULT'][index] = ' '.join(map(str,a[0][6:]))

# setup of modules
sentiment = SentimentIntensityAnalyzer()
sentiment_pipeline = pipeline(model = "finiteautomata/bertweet-base-sentiment-analysis")


# make new DVT column
data['DVT_s'] = ''
data['sentiment'] = ''
data['DVT_sp'] = ''
data['sentiment_pipeline'] = '' 



# Pseudocode 
# pass in the text to the algorithm
# if there are phrases found in throm_pre
#   indicate in a column that there is thrombosis
# else if there are phrase found in throm_abs
#   indicate in a column that there isn't thrombosis
for index, row in data.iterrows():
    data['sentiment'][index] = sentiment.polarity_scores(data['RESULT'][index])
    # data['sentiment_pipeline'][index] = sentiment_pipeline(data['RESULT'][index]) # this is the problem line
    if data['sentiment'][index]['pos'] > 0:
        data['DVT_s'][index] = data['DVT_s'][index].replace('', 'Yes')
    else:
        data['DVT_s'][index] = data['DVT_s'][index].replace('', 'No')
    # if data['sentiment'][index]['POSITIVE'] > 0.01:
    #     data['DVT_sp'][index] = data['DVT_sp'][index].replace('', 'Yes')
    # else:
    #     data['DVT_sp'][index] = data['DVT_sp'][index].replace('', 'No')

print(data['DVT_s'].value_counts())
# print(data['DVT_sp'].value_counts())

# outputting a file to test for the effectiveness of the algorithm
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = timestr+'qc_samplefile.csv'
data.sample(n = 10).to_csv('test files for Sentiment Analysis\\' + filename)

