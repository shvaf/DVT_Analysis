# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 11:20:09 2023

@author: vafeas
"""




import pandas as pd
import numpy as np
import csv
import string
import warnings
warnings.filterwarnings("ignore")
import re
import time
import random
from datetime import datetime

file_text = pd.read_table(r"data\ChatGPT_generated_fake_DVT_data.txt")
N = len(file_text)
#size = 

list_of_column_names = file_text.columns.values
column_names = list_of_column_names[0].split(',')
data_reg = pd.DataFrame(columns = column_names, index = range(0,N)) 
for index, row in file_text.iterrows():
    a = file_text.iloc[index].str.split(',').tolist() 
    data_reg['PAT_ID'][index] = a[0][0]
    data_reg['PAT_MRN_ID'][index] =  a[0][1] 
    data_reg['ORDER_PROC_ID'][index] = a[0][2]
    data_reg['ORDER_TIME'][index] = a[0][3]
    data_reg['RESULT_TIME'][index] = a[0][4]
    data_reg['DESCRIPTION'][index] = a[0][5]
    data_reg['RESULT'][index] = ' '.join(map(str,a[0][6:]))


data_reg['DVT'] = ''
data_reg['DVT - Positive'] = ''
data_reg['DVT - Negative'] = ''
data_reg['DVT - Unclear'] = ''
data_reg['Found Key Word'] = ''
data_reg['Venous Reflux'] = 0
data_reg['DVT - Conclusions'] = ''
data_reg['DVT - Impressions'] = ''
data_reg['DVT - Conclusions or Impression'] = ''
data_reg['Venous Reflux'] = ''
data_reg['Regex - Vein Mapping'] = ''



#Pseudocode

# Find conclusions or impressions and cut the string there
# Look for key words such as DVT, Thromobosis, etc 
# Look ahead and behind of the key words and look for phrases that indicate presence or absence of thrombosis 
# Focus on "thrombus is present" to test and build algorithm

conc_impress_words = ["IMPRESSION", 
                      "conslusions",
                      "conclusions",
                      "impressions",
                      "impression",
                      "IMPRESSION",
                      "INDICATION",
                      "FINDINGS",
                      "Findings"
                      ]
# key words for dvt
key_words = [#"thrombus",
             #"thrombosis",
             #"deep and superficial venous thrombosis", Doesn't catch superficial if I include this in key words 
             "sonographic evidence of acute deep venous thrombosis",
             "thrombus along",
             "stable thrombosis",
             "acute thrombosis",
             "acute thrombus",
             "deep venous thrombosis",
             "DVT",
             "occlusive thrombus",
             "deep vein thrombosis",
             "appears thrombosed",
             "nonocclusive venous thrombosis",
             "nonocclusive venous thrombus",
             "deep venous thrombosis",
             "venous thrombosis", #algorithm struggles when it's superficial venous thrombosis
             "venous thrombus",
             "vein thrombosis",
             "right lower extremity deep venous thrombosis",
             "of venous thrombosis",
             "nonocclusive thrombus",
             "nonocclusive thrombosis",
             "deep vein thromboses",
             "left distal femoral, popliteal, and tibial deep vein thrombosis",
             "isolated right calf peroneal deep vein thrombus",
             "deep vein thrombus",
             #"deep or superficial vein thrombosis",
             "left femoral, popliteal, and tibial deep vein thrombosis",
             "right femoral, popliteal, and calf vein deep venous thrombosis",
             "femoral, popliteal and tibial vein deep venous thrombosis",
             "residual chronic thrombus",
             "nonocclusive hypoechoic thrombus",
             "very extensive right femoral, popliteal, tibial and external iliac deep vein thrombosis",
             "occlusive and nonocclusive right distal femoral, popliteal, tibial, and gastrocnemius muscular deep vein thrombosis",
             "left subclavian, axillary, and brachial vein venous thrombosis",
             "right femoral, popliteal, and peroneal deep venous thrombosis",
             "left femoral and popliteal deep venous thrombosis",
             "right distal external iliac, common femoral, deep femoral, popliteal, and tibial deep vein thrombosis"
             "acute-appearing, mostly occlusive thrombus",
             "bilateral femoral, right popliteal, and right common femoral deep vein thrombosis",
             "chronic appearing non-occlusive bilateral common femoral, deep femoral, femoral, and popliteal deep vein thrombosis",
             "bilateral calf deep venous thrombosis",
             "femoral, popliteal, and tibial venous thrombosis",
             "deep nor superficial vein thrombosis", #come back to this
             #"deep or superficial thrombosis",
             #"deep or superficial vein thrombosis",
             "a left common femoral, deep femoral, femoral, and popliteal deep vein thrombosis",
             "left jugular vein thrombosis",
             "extensive left common femoral, femoral, popliteal, and tibial deep vein thrombosis",
             "extensive right internal jugular, subclavian, axillary, and brachial deep vein thrombosis",
             "chronic thrombus",
             "right axillary, subclavian, and brachial deep vein thrombus",
             "right femoral, popliteal, and tibial deep vein thrombosis",
             "right subclavian, axillary, and brachial vein deep venous thrombosis",
             "left femoral, popliteal and tibial deep vein thrombosis",
             "acute appearing thrombus",
             "persistent thrombosis",
             "chronic-appearing nonocclusive right popliteal deep vein thrombus",
             "chronic-appearing bilateral tibial and right popliteal deep vein thrombosis",
             "bilateral common femoral, deep femoral, popliteal, and tibial deep vein thrombosis",
             "nonocclusive chronic-appearing left internal jugular deep vein thrombosis",
             "nonocclusive right popliteal vein thrombus",
             "right distal external iliac, common femoral, deep femoral, popliteal, and tibial deep vein thrombosis",
             "mostly occlusive thrombus",
             "right internal jugular vein, subclavian, and axillary vein deep venous thrombosis",
             "acute-appearing, mostly occlusive thrombus",
             "chronic thrombus",
             "nonocclusive area of thrombus",
             "completely thrombosed",
             "a chronic-appearing right distal femoral and popliteal as well as left peroneal deep vein thrombosis",
             "femoral vein thrombus",
             "right upper arm basilic vein thrombus",
             "thrombus in the left axillary",
             "nonocclusive deep venous thrombosis",
             "occlusive deep venous thrombosis",
             "echogenic deep venous thrombosis",
             "right leg calf vein deep vein thrombosis",
             "chronic appearing left femoral and popliteal deep vein thrombosis",
             "left leg deep vein thrombosis",
             "right popliteal vein deep vein thrombosis",
             "a nonocclusive left deep femoral deep vein thrombosis",
             'vein thrombus',
             "venous thrombosis (dvt)",
             "left lower extremity deep vein thrombosis",
             #"deep and superficial venous thrombosis"
             ]
key_words_regex = '|'.join(key_words)


pos_words = ["is present",
             "is noted",
             "there is",
             "2\. there is",
             "there was",
             "detected",
             "detect",
             "detectable",
             "demonstrating",
             "demonstrate",
             "normally",
             "with evidence", 
             "with evidence of"
             "present",
             "acute",
             "was detected",
             #"no other",
             "consistent with",
             "extensive",
             "within",
             "around",
             "positive",
             "along",
             "continuing",
             "residual",
             "chronic",
             "involving",
             "stable",
             "partially occlusive",
             "consistent with",
             "non-occlusive",
             "is in",
             "involving",
             "extensive acute left leg",
             "is seen",
             "of two axial calf veins",
             "chronic-appearing very focal left popliteal",
             "revealing",
             "in the",
             "as above",
             "as described",
             "vein mapping with",
             "subacute appearing",
             "of the right",
             "abnormal examination with evaluation of",
             "with bilateral peroneal",
             "1 persistent, likely",
             "remain",
             "as described",
             "showing"
             ]
pos_words_regex = '|'.join(pos_words)

pre_neg_words = [" no ",
             "without",
             "without evidence for",
             "without evidence of",
             #"no sonographically apparent",
             "negative for",
             #"do not see definite findings",
             "does not appear",
             "there is no ",
             "no evidence of",
             " no other site for",
             'there is no evidence of',
             'definitive exclusion of',
             'clinical suspicion of',
             'presence of possible',
             "possibleright"
             ]

post_neg_words = ["normal",
             "no sonographically apparent",
             "negative for",
             "do not see definite findings",
             "does not appear",
             #"there is no",
             #"in either",
             "but ",
             "was not ",
             "is not ",
             "cannot be ruled out"]



pre_neg_words_regex = '|'.join(pre_neg_words)
post_neg_words_regex = '|'.join(post_neg_words)

normal_scan = [" normal bilateral lower extremity venous duplex scan",
               " normal venous examination",
               " normal examination",
               "a normal venous examination",
               " normal left lower extremity venous",
               " normal bilateral lower extremity venous duplex scan",
               " normal bilateral upper extremity venous duplex scan",
               " normal lower extremity venous duplex",
               " normal left upper extremity venous duplex",
               " normal left leg venous duplex exam",
               " normal bilateral lower extremity venous",
               " normal right lower extremity venous duplex",
               " a normal chronic venous evaluation",
               " normal bilateral lower extremity venous examination",
               " normal right leg venous duplex exam",
               " normal right lower extremity venous examination",
               " a normal limited venous examination",
               " normal right upper extremity venous duplex exam",
               " normal upper extremity venous duplex exam",
               " a normal limited, as described above, chronic venous examination",
               " normal left lower extremity venous duplex exam",
               " normal upper extremity venous duplex evaluation",
               " normal but limited lower extremity venous duplex evaluation",
               " normal study right lower extremity color doppler phlebogram",
               " normal venous duplex ultrasound of the left upper extremity",
               "	normal left lower extremity venous duplex exam",
               "	a normal pre-cannulation study"
               ]
normal_words = '|'.join(normal_scan)

superficial_words = ["superficial vein thrombosis", 
                     "superficial venous thrombosis",
                     "superficial vein thrombus",
                     "right echogenic superficial vein thrombosis"]
superficial_words_regex = '|'.join(superficial_words)

pos_superficial = ["there is",
                   "also",
                   "abnormal examination"]
pos_superficial_regex = '|'.join(pos_superficial)

thrombus_start = [
    ' there is deep vein thrombosis',
    ' evidence of dvt in',
    ' bilateral lower extremity deep venous thrombosis,',
    ' 1 nonocclusive deep venous thrombosis',
    ' 1 evidence of dvt in', 
    ' 1 partially occlusive thrombus', 
    ' 1 stable thrombus',
    ' thrombus along',
    ' 1 stable thrombus',
    '	 right popliteal venous thrombosis',
    ' dvt of the basilic',
    ' 1 stable thrombus',
    ' 1 greater saphenous vein thrombosis'
    ]

thrombus_start_regex = '|'.join(thrombus_start)

negative_start = [
    '	no detectable thrombus',
    'negative',
    'no evidence of',
    '	no deep or superficial',
    'no deep or',
    ' or ',
    ' no ',
    ' no other site for'
    ]
negative_start_regex = '|'.join(negative_start)

thrombus_override = [
    'on the left  there is deep venous thrombosis',
    'on the right  there is deep venous thrombosis']
thrombus_override_regex = ' | '.join(thrombus_override)

data_reg['count'] = 0
# Cut string based on conclusisons or impressions
for index, row in data_reg.iterrows():
    for j in range(len(conc_impress_words)):
        if bool(re.search(conc_impress_words[j], data_reg['RESULT'][index].lower())):
            data_reg['DVT - Conclusions or Impression'][index] = data_reg['RESULT'][index].lower().split(conc_impress_words[j], 1)[-1] 



# Step 0 - remove \n from texts
for index, row in data_reg.iterrows():
    data_reg['DVT - Conclusions or Impression'][index] =  data_reg['DVT - Conclusions or Impression'][index].replace("\\n"," ")
    data_reg['DVT - Conclusions or Impression'][index] =  data_reg['DVT - Conclusions or Impression'][index].replace(":"," ")
    data_reg['DVT - Conclusions or Impression'][index] =  data_reg['DVT - Conclusions or Impression'][index].replace("."," ")
    

# Step 1 - Find the key word
for index, row in data_reg.iterrows():
    for j in range(len(key_words)):
        if (re.search("refused", data_reg['DVT - Conclusions or Impression'][index].lower()) and re.search("pain", data_reg['DVT - Conclusions or Impression'][index].lower()) or re.search("could not tolerate", data_reg['DVT - Conclusions or Impression'][index].lower()) or re.search("incomplete venous examination", data_reg['DVT - Conclusions or Impression'][index].lower())):
            data_reg['Found Key Word'][index] = 'Incomplete Exam'
            break;
        elif key_words[j].lower() in data_reg['DVT - Conclusions or Impression'][index].lower():
            data_reg['Found Key Word'][index] = 'Yes'
            break;
        if re.search("reflux", data_reg['DVT - Conclusions or Impression'][index].lower()):
            data_reg['Venous Reflux'][index] = 'Yes'
            break;



# Data sets of other words            
valvular = data_reg[data_reg['Found Key Word'] == 'Valvular']
valvular.to_html("data/HTML_files/valvular.html")
incomplete_exam = data_reg[data_reg['Found Key Word'] == 'Incomplete Exam']
venous_reflux = data_reg[data_reg['Found Key Word'] == 'Venous Reflux']
venous_reflux.to_html("data/HTML_files/reflux.html")
vein_measurements = data_reg[data_reg['Found Key Word'] == 'Vein Measurements']            




pos_search = '('+pos_words_regex+')'+'( \w*){0,5}'+'('+key_words_regex+')'+'|'+'('+key_words_regex+')'+'( \w*){0,5}'+'('+pos_words_regex+')'
pos_search_svt = '('+pos_superficial_regex+')'+'( \w*){0,10}'+'('+superficial_words_regex+')'

neg_search = '('+pre_neg_words_regex+')'+'( \w*){0,5}'+'('+key_words_regex+')'+'|'+'('+key_words_regex+')'+'( \w*){0,5}'+'('+post_neg_words_regex+')'
#neg_search = '('+pre_neg_words_regex+')'+'( \w*){0,5}'+'('+pos_words_regex+')'+'|'+'('+pos_words_regex+')'+'( \w*){0,5}'+'('+post_neg_words_regex+')'+'|'+'('+pre_neg_words_regex+')'+'( \w*){0,5}'+'('+key_words_regex+')'+'|'+'('+key_words_regex+')'+'( \w*){0,5}'+'('+post_neg_words_regex+')'
#neg_search = '('+neg_words_regex+')'+'( \w*){0,10}'+'('+pos_words_regex+')'+'|'+'('+pos_words_regex+')'+'( \w*){0,10}'+'('+neg_words_regex+')'+'|'+'('+neg_words_regex+')'+'( \w*){0,5}'+'('+key_words_regex+')'+'|'+'('+key_words_regex+')'+'( \w*){0,5}'+'('+neg_words_regex+')'
#neg_search_svt = '('+pre_neg_words_regex+')'+'( \w*){0,5}'+'(superficial)'+'|'+'(superficial)'+'( \w*){0,5}'+'('+post_neg_words_regex+')'
neg_search_svt = '('+pre_neg_words_regex+')'+'( \w*){0,5}'+'('+superficial_words_regex+')' + '|'+ '('+negative_start_regex+')'+'( \w*){0,5}'+'('+superficial_words_regex+')' 

data_reg['Regex - Found Key Word'] = ''
data_reg['Regex - Found Positive Key Word'] = ''
data_reg['Regex - Found Negative Key Word'] = ''
data_reg['DVT'] = ''
data_reg['DVT - Yes'] = ''
data_reg['DVT - No'] = ''
data_reg['DVT - Unclear'] = ''
data_reg['SVT'] = ''
data_reg['clots'] = ''
data_reg['possible'] = ''
data_reg['abnormal/normal'] = ''
data_reg['Exam_type'] = ''
data_reg['DVT_true_false'] = ''# data_reg['DVT_true_false'].astype(object)
data_reg['SVT_true_false'] = ''# data_reg['SVT_true_false'].astype(object)
blank_conclusions = []

# 1 - look for normal or abnormal within the first 20 spots
for index, row in data_reg.iterrows():
    if(re.search('lower extremity', data_reg['DESCRIPTION'][index].lower()) != None):
        data_reg['Exam_type'][index] = 'Lower body'
    if(re.search('right lower extremity', data_reg['DESCRIPTION'][index].lower()) != None):
        data_reg['Exam_type'][index] = 'Right Lower body'
    if(re.search('left lower extremity', data_reg['DESCRIPTION'][index].lower()) != None):
        data_reg['Exam_type'][index] = 'Left Lower body'
    if(re.search('upper extremity', data_reg['DESCRIPTION'][index].lower()) != None):
        data_reg['Exam_type'][index] = 'Upper body'  
    if(re.search('right upper extremity', data_reg['DESCRIPTION'][index].lower()) != None):
        data_reg['Exam_type'][index] = 'Right Upper body' 
    if(re.search('left upper extremity', data_reg['DESCRIPTION'][index].lower()) != None):
        data_reg['Exam_type'][index] = 'Left Upper body' 
    if data_reg['DVT - Conclusions or Impression'][index] == '':
        blank_conclusions.append([index])
    if re.findall(normal_words, data_reg['DVT - Conclusions or Impression'][index][:80]) != []: 
        data_reg['DVT'][index] = False 
        data_reg['DVT - No'][index] = 'FALSE' 
        data_reg['SVT'][index] = False
        data_reg['abnormal/normal'][index] = 'normal'
        continue #if there is a normal exam, no DVT or SVT and further evaluations are unnecessary
    if (re.findall(key_words_regex.lower(), data_reg['DVT - Conclusions or Impression'][index].lower()) != None):
        print(re.findall(key_words_regex.lower(), data_reg['DVT - Conclusions or Impression'][index].lower()))
        counter = 0
        keyword_match = re.finditer(key_words_regex.lower(), data_reg['DVT - Conclusions or Impression'][index].lower())
        DVT_true_false = []
        SVT_true_false = []
        for match_obj in keyword_match:
            print(match_obj)
            b = match_obj.span()[0]# search for negative before 
            print(b)
            if b >= 25: #length of negative options plus 2 spaces
                c = b-25
            if b < 25:
                c = 0
            d = match_obj.span()[1]# search for negative after
            e = d+22 #length of negative options plus 2 spaces
            g = b-13 #length of superficial plus 2 spaces
            if b >= 82: #length of string plus deep vein thrombosis, 2 spaces
                h = b-82
            if b < 82:
                h = 0 
            if (re.search('this examination be repeated', data_reg['DVT - Conclusions or Impression'][index][0:b].lower()) != None): #ignore match objects that are prefaced by exam repeat instructions
                print('00', data_reg['DVT - Conclusions or Impression'][index][h:b].lower())
                DVT_true_false.append(False)
            elif (re.search('examination does not conclusively exclude the presence of', data_reg['DVT - Conclusions or Impression'][index][h:b].lower()) != None):
                print('0', data_reg['DVT - Conclusions or Impression'][index][h:b].lower())
                DVT_true_false.append(False)
            elif (re.search(pre_neg_words_regex.lower(), data_reg['DVT - Conclusions or Impression'][index][c:b].lower()) != None):
                print('1',re.search(pre_neg_words_regex.lower(), data_reg['DVT - Conclusions or Impression'][index][c:b].lower()))
                DVT_true_false.append(False)
            elif (re.search(post_neg_words_regex.lower(), data_reg['DVT - Conclusions or Impression'][index][d:e].lower()) != None):
                print('2', re.search(post_neg_words_regex.lower(), data_reg['DVT - Conclusions or Impression'][index][d:e].lower()))
                DVT_true_false.append(False)
            elif (re.search('superficial', data_reg['DVT - Conclusions or Impression'][index][g:b].lower()) != None): #check if it's SVT
                if (re.search('deep and superficial', data_reg['DVT - Conclusions or Impression'][index][(b-23):b].lower()) != None):  # check if it says deep and superificial
                    print('30', re.search('deep and superficial', data_reg['DVT - Conclusions or Impression'][index][(b-23):b].lower()))
                    DVT_true_false.append(True)
                else:
                    print('3', re.search('superficial', data_reg['DVT - Conclusions or Impression'][index][g:b].lower()))
                    DVT_true_false.append(False)
            else:
                print('4')
                DVT_true_false.append(True)
            if b >= 24: #length of superficial plus 2 spaces #Not sure how to deal with this now, worried about deep or superficial
                f = b-24
            if b < 24:
                f = 0
            if re.search('superficial', data_reg['DVT - Conclusions or Impression'][index][f:b].lower()) != None: 
                print('5', re.search('superficial', data_reg['DVT - Conclusions or Impression'][index][f:b].lower()))
                if (re.search('deep and superficial', data_reg['DVT - Conclusions or Impression'][index][(b-23):b].lower()) != None):  # check if it says deep and superificial
                    print('30', re.search('deep and superficial', data_reg['DVT - Conclusions or Impression'][index][(b-23):b].lower()))
                    DVT_true_false.append(True)
                    SVT_true_false.append(True)
                if re.search(negative_start_regex, data_reg['DVT - Conclusions or Impression'][index][f:b].lower()) != None: 
                    print('6', re.search(negative_start_regex, data_reg['DVT - Conclusions or Impression'][index][f:b].lower()))
                    SVT_true_false.append(False)
                else:
                    print('7', re.search(negative_start_regex, data_reg['DVT - Conclusions or Impression'][index][f:b].lower()))
                    SVT_true_false.append(True)
            counter = 1 + counter
        if any(DVT_true_false):
            data_reg['DVT'][index] = True
        else:
            data_reg['DVT'][index] = False
        if any(SVT_true_false):
            data_reg['SVT'][index] = True
        else:
            data_reg['SVT'][index] = False
        data_reg['DVT_true_false'][index] = ','.join([str(x) for x in DVT_true_false])
        data_reg['SVT_true_false'][index] = ','.join([str(x) for x in SVT_true_false])
        
# Manual Entry 
# These are entries where the results were not cut into DVT - Conclusions or Impressions and I manually entered them
dvt_manual_index = [253, 3150, 2707, 431]
nodvt_manual_index = [84, 2555, 295, 3121, 731, 1005, 1203, 1361, 1516, 1734, 2171, 2253, 2712, 2974]
#svt_manual_index = []
for j in range(len(dvt_manual_index)):
    data_reg['DVT'][dvt_manual_index[j]] = True
for j in range(len(nodvt_manual_index)):
    data_reg['DVT'][nodvt_manual_index[j]] = False
    
no_diag_list = [295, 468, 530, 585, 659, 678, 720, 860, 1679, 1790, 2095, 2269, 2299, 2406, 2684, 2705, 2865, 2898, 2971, 2996, 3005, 3280, 2122]
for j in range(len(no_diag_list)):
    data_reg['Found Key Word'][no_diag_list[j]] = 'No Diagnosis'
    data_reg['DVT - Conclusions or Impression'][no_diag_list[j]] = 'No Diagnosis'
    data_reg['DVT'][no_diag_list[j]] = False


unclear_list = ['Unclear DVT', '', 'Abnormal - Unclear DVT']
data_unclear = data_reg[data_reg['DVT'].isin(unclear_list)]            
data_unclear.to_html("data/HTML_files/data unclear.html")   
data_reg[data_reg['SVT'] != ''].to_html("data/HTML_files/svt.html")
data_reg[data_reg['clots'] == 'clot'].to_html("data/HTML_files/clot.html") 
data_reg[data_reg['possible'] == 'possible'].to_html("data/HTML_files/possible.html") 


print(data_reg['Regex - Found Key Word'].value_counts())
print(data_reg['Regex - Found Positive Key Word'].value_counts())  
print(data_reg['Regex - Found Negative Key Word'].value_counts())   
print(data_reg['DVT'].value_counts())
print(data_reg['SVT'].value_counts())     
timestr = time.strftime("%Y%m%d-%H%M%S")  




random.seed(10)
filename = timestr+'qc_regex_samplefile.html'


# Updating formats to reach final dataset
data_reg['RowID'] = data_reg.index + 1
   
#data_reg.sample(n=10).to_html('test files\\' + filename)  
data_reg.sample(n = 20).to_html('test files\\' + filename)   
#data_reg['ORDER_TIME'] = data_reg['ORDER_TIME'].strftime("%Y-%m-%d")

# making an html output for ease of review
data_reg.to_html(r'data/HTML_files/data_html.html')


# Determine a dataset of the earliest DVT diagnosis for each patient
final_dataset = data_reg[(data_reg['DVT'] == True) | (data_reg['SVT'] == True)] # fix so that you're pulling DVT and SVT
final_dataset['Thrombus'] = True
final_dataset = (final_dataset.groupby('PAT_ID')
       .apply(lambda g: g[g['ORDER_TIME'].isin([g['ORDER_TIME'].min()])])
       .reset_index(drop=True))#.drop_duplicates('ORDER_TIME') # maybe don't drop duplicates and keep both
duplicates = final_dataset['PAT_ID'].duplicated()
# indexs (not RowID) of duplicates: 
# [80, 198, 211, 250, 270, 322, 386, 452, 460, 477, 498, 590, 619, 655, 757, 787, 884, 984, 992, 1012, 1042, 1078]

# for index in range(len(duplicates)):
#     if duplicates[index] == True:
#         final_dataset['Exam_type'][index] = 'Upper and Lower Body'
final_dataset = (final_dataset.groupby('PAT_ID')
       .apply(lambda g: g[g['PAT_ID'].isin([g['PAT_ID'].min()])])
       .reset_index(drop=True)) #drop duplicates   
final_dataset = final_dataset[["RowID", "PAT_ID", "PAT_MRN_ID", "DVT", "SVT", "ORDER_TIME", "RESULT_TIME", "Exam_type", "Thrombus"]]
final_dataset.to_html(r'data/HTML_files/final_dataset_html.html')
final_dataset.to_excel(r'data/Excel_files/DVT.xlsx', index = False)
#add a manual step that collapses patients with upper and lower into both
