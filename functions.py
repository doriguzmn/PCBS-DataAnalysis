#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 08:28:02 2021

@author: dori
"""

import pandas as pd
from scipy import stats
from statsmodels.formula.api import ols
import pingouin as pg
import matplotlib.pyplot as plt
import seaborn as sns



def getUsableVideos(learning,participantData):
    """This functions returns the usable videos by (1) merging participant and learning data (and deleting a repeated column: 'Study_Condition') 
    and (2) subsetting the subjects whose videos are usable (some videos did not have enough quality).

    inputs: 
        - learning: This dataframe has the information about the learning of the subjects in the experiment. It includes how many problems they 
        solved before talking to Jaden, the virtual tutor, how many they solved after, and a composite score measuring learning gains (after-before). 
        There are two different types of algebra question: those about conceptual learning, and those about procedural learning. The total learning 
        variables are merging those two types of question.
        - participantData: This dataframe has the participant information: participant gender, age, grade, school, previous algebra experience, 
        Jaden's perceived gender/ethnicity ... It also contains the self-reported rating of the rapport experienced in the interaction between Jaden and the student.

    outputs: 
        -mergeddf: this dataframe has the merged information of the two dataframes above (i.e. learning and participantData)
        - UsableVideos: mergeddf but subsetting for the participants whose videos are of high quality 
        and were thus used to obtain the "thin-sliced" ratings in Amazon Mechanical Turk (explained below).
    """
    #1. merge the participant and learning data 
    mergeddf = learning.merge(participantData, on='Participant')
    mergeddf = mergeddf.drop('Study_Condition', axis=1)

    #2. subset the subjects whose videos are usable 
    UsableVideos = mergeddf[mergeddf["Usable"]=="Y"]

    return mergeddf, UsableVideos


def getFullData(rapport, UsableVideos, mergeddf):
    """This function returns a database merging the merged usable data obtained above, with the rapport ratings that AMT workers gave for each slice of 
    a participant's video, plus a column with the average slice rating for said video.

    inputs: 
        - rapport: dataframe containing the "thin-sliced" rapport ratings provided by AMT workers. Workers rated the rapport between Jaden and the participant,
        for each 30-second slice of a video. 
        - UsableVideos: same as above 
        - mergeddf : same as above

    outputs:
        - full_usabledatabase: dataframe merging UsableVideos and rapport. Therefore, it has demographic information about the participant, 
        about the participants' learning gains and the rapport ratings by AMT workers, both the individual slices and the total average for each video. 
        Video and participant are, in this dataframe, equivalent, as we only have videos for participants in the UsableVideos dataframe.
    """
    #first, I create a dictionary for each video (keys) that has the ratings for all slices (values)
    rapportvideo = {}
    for _, row in rapport.iterrows():
        if row['Video'] in rapportvideo:
            rapportvideo[row['Video']].append(row['Rating'])
        else:
            rapportvideo[row['Video']] = list()
            rapportvideo[row['Video']].append(row['Rating'])

    #create a data set from this dictionary, with one participant (or video) in each row and all the individual slice ratings as the columns:
    rapport_dataset= pd.DataFrame.from_dict(rapportvideo, orient='index').reset_index(level=0)
    rapport_dataset= rapport_dataset.add_prefix('AMT_Slice_')
    rapport_dataset = rapport_dataset.rename(columns={'AMT_Slice_index':'Participant'})

    #get the average of all the slices, and put them in a new column (Note: I had to remove the participant column first to do this)
    select=rapport_dataset.drop('Participant', axis=1)
    rapport_dataset.insert(83, 'AMT_Rapport_Average', select.mean(axis=1))

    #To merge rapport_database with the previous data (i.e. usablevideos)
    full_usabledatabase = UsableVideos.merge(rapport_dataset, on='Participant')

    #to save the Excelsheets:
    rapport_dataset.to_excel("WoZ_2019_AMTRatings.xlsx", index=False)

    with pd.ExcelWriter('WoZ_2019_FullData.xlsx') as writer:   
        mergeddf.to_excel(writer, sheet_name='AllVideos', index=False)
        full_usabledatabase.to_excel(writer, sheet_name='UsableVideos', index=False)

    return full_usabledatabase


def dataAnalysis(interesting_columns, full_usabledatabase):
    """This function returns the outputs of the data analyses performed. In particular, it takes the columns of interest 
    and the full usable dataset, and returns the output of the ANOVA (each column by condition) and that of the linear regression 
    between each column and condition (with and without regressors). Moreover, it returns the output of a t-test between
    the participants' self-reported rapport rating and the AMT-obtained rapport ratings.


    inputs: 
        - interesting_columns: columns that we want to use in the analyses. In this case, those describing the total 
        learning gains, the conceptual learning gains, the procedural learning gains, the average of all slice ratings
        provided by AMT, and the self-reported rapport rating provided by the participant.
        - full_usabledatabase: 

    outputs:
        - outputs from the ANOVA, linear regression and t-test analyses. If running on the terminal, the graphs will
        be saved, and the outputs will be printed on the terminal. 
    """
    
    splitdata= full_usabledatabase.groupby('Condition')
    
    for column in interesting_columns:
        print(column, splitdata[column].describe())
        plt.figure()
        sns.boxplot(y=column, x='Condition', order=["Task-only",'Fixed','Adaptive'], 
                    data=full_usabledatabase, 
                    palette="colorblind")
        sns.stripplot(y=column, x='Condition', order=["Task-only",'Fixed','Adaptive'],
                    data=full_usabledatabase, 
                    jitter=True,
                    dodge=True, 
                    marker='o', 
                    alpha=0.5,
                    color='grey')
        plt.savefig(column+'.png')

        
        

    #to perform an ANOVA on all the interesting columns by condition:
    for column in interesting_columns:   
        aov = pg.anova(data=full_usabledatabase, dv=column, between='Condition', detailed=True)
        print(column, aov)

    #to do a regression, as that was significant in a previous analysis that I want to replicate using the usable data (I used this package osl because the models I based myself on were created in R )

    for column in interesting_columns:
        formula= column + str(' ~ ') + "Condition"
        model = ols(formula, data=full_usabledatabase)
        fitted_model = model.fit()
        print(column, fitted_model.summary())
        
    #to include more regressors in the regression:

    for column in interesting_columns:
        formularegressors = column + str(' ~ ') + "Condition + Student_Gender + Grade + Algebra_experience"
        model = ols(formularegressors, data=full_usabledatabase)
        fitted_model = model.fit()
        print(column, fitted_model.summary())

    #Lastly, to investigate whether the self-reported rapport and the AMT-obtained rapport are different, I get the descriptives, draw a boxplot and perform a t-test:
    print(full_usabledatabase['self_report_Rapport_Average'].describe())
    print(full_usabledatabase['AMT_Rapport_Average'].describe())

    f, (ax1, ax2) = plt.subplots(1,2)
    sns.boxplot(y=full_usabledatabase['self_report_Rapport_Average'], ax=ax1)
    sns.boxplot(y=full_usabledatabase['AMT_Rapport_Average'], ax=ax2)
    plt.setp(ax1, ylim=[2,6])
    plt.setp(ax2, ylim=[2,6])
    f.tight_layout(pad=2.0)
    plt.savefig('reportedvsAMTrapport.png')

    print(stats.ttest_ind(full_usabledatabase['self_report_Rapport_Average'], full_usabledatabase['AMT_Rapport_Average']))
    
    
    
    