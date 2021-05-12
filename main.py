#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 08:28:02 2021

@author: dori
"""

from functions import getUsableVideos,getFullData,dataAnalysis
import pandas as pd

#DATA READING

#read the Excel sheet with the rapport ratings obtained using AMT 
rapport = pd.read_excel ('AllSlicesData_NiceFormat_edited.xlsx')

print(rapport.head())
#read the Excel with participant data and learning data
learning = pd.read_excel('Dori-RAPT_WoZ_2019_learning-gain_condition.xlsx')
participantData=pd.read_excel('Dori-RAPT_WoZ_participant_data.xlsx')

#DATA PROCESSING
    
MergedDf = getUsableVideos(learning,participantData)[0]
UsableVideos = getUsableVideos(learning,participantData)[1]

full_usabledatabase = getFullData(rapport, UsableVideos, MergedDf)
print(full_usabledatabase.head())

#DATA ANALYSIS

interesting_columns= ['Learning_gain_total','Learning_gain_conc','Learning_gain_proc','AMT_Rapport_Average', 'self_report_Rapport_Average']
dataAnalysis(interesting_columns, full_usabledatabase)




