# Rapport-Aware Peer Tutor Data Analysis
My project is part of the Rapport-Aware Peer Tutor, whose goal is to advance understanding of the nature of the development of rapport and its impact on learning processes, in particular with virtual ECAs as tutors. The project is led by Justine Cassell.

Rapport defines the alignment of the participants in a conversation. This alignment can manifest in multiple ways, such as the smoothness of the conversation and the mutual understanding or closeness of the participants in the conversation. Here, a low level of rapport corresponds to a small alignment between the participants of a conversation, and contrary, a high level of rapport corresponds to a great alignment. 

In order to study rapport in a human-human tutoring environment, over 100 hours of data of students tutoring each other in algebra were collected and the verbal and nonverbal behaviors that contribute to the development rapport between them were analyzed. Findings showed that tutoring pairs with greater rapport engage in more of the socially-supportive behaviors like help-offering, explanation-prompting, comprehension-monitoring, and self-explanations, all indicative of positive, supportive climates for learning (Madaio, Peng, Ogan, & Cassell, 2018; Sinha & Cassell, 2015). Students whose rapport with their partner deepens over time also solve more problems and learn more on a post-test. 

As a result of this work, the first computational model of rapport was developed, which allowed Cassell's team to design a virtual peer tutor, Jaden, that can develop rapport with a student to better support them in learning. 

My project will consist in evaluating the efficacy of rapport-building social components of a virtual peer tutoring system (i.e. Jaden) and its influence in the learning of the students. Importantly, three conditions based on different models of rapport were used by Jaden in its interactions with student tutees: 

-Task-only (control): no social dialogue used at all. 

-Fixed model of rapport, where fixed rules were implemented for Jaden's use of social dialogue, informed by prior literature (e.g. gradually increasing frequency and intimacy of self-disclosure).

-Adaptive model of rapport, where Jaden's use of social utterances is determined by social reasoning, based on the current rapport level (as determined by a rapport estimator built by Cassell's team).

#### Table of Contents

* [General description of the code](#code)
* [Reading the data](#data)
* [Data processing](#processing)
* [Data analysis](#analyses)
* [Discussion and Future directions](#discussion)
* [Bibliography](#bibliography)
* [What I learned from this course](#learned)

## <a name="code"></a>General description of the code and packages

There are two python programs: functions.py (with the functions that we will require throughout the code) and main.py (with the actual data we are using)

Throughout this README, I will explain the main.py first, and then add the relevant functions from the functions.py program. Although the packages required are included in functions.py, I will add them here for clarity:

```python
import pandas as pd
from scipy import stats
from statsmodels.formula.api import ols
import pingouin as pg
import matplotlib.pyplot as plt
import seaborn as sns
```

## <a name="data"></a>Reading the data

We read the 3 Excel sheets that are needed for this data analysis:

```python
#read the Excel sheet with the rapport ratings obtained using AMT 
rapport = pd.read_excel ('AllSlicesData_NiceFormat_edited.xlsx')

#read the Excel with participant data and learning data
learning = pd.read_excel('Dori-RAPT_WoZ_2019_learning-gain_condition.xlsx')
participantData=pd.read_excel('Dori-RAPT_WoZ_participant_data.xlsx')
```

To help understand the rest of the code, here are the first few rows of each Excel sheet, which are explained below:

### AMT rapport ratings 
 <img src="https://user-images.githubusercontent.com/65661142/118037242-de75c780-b36d-11eb-9c3f-cb2d19b444b1.png" width="90%"></img> 

### Learning data
<img src="https://user-images.githubusercontent.com/65661142/118037239-dddd3100-b36d-11eb-84d9-e6b85d9ae10e.png" width="90%"></img>

### Participant demographics
<img src="https://user-images.githubusercontent.com/65661142/118037238-dd449a80-b36d-11eb-9150-b2b135d85e31.png" width="90%"></img>
 

## <a name="processing"></a>Data processing

Once we read the Excel sheets, we need to do some processing. Our goal is to get a database that includes:
-Participants' demographic data: participant gender, age, grade, school, previous algebra experience, Jaden's perceived gender/ethnicity, etc)
-Participant's learning information: how many problems participants solved before talking to Jaden, the virtual tutor, how many they solved after, a composite score measuring learning gains (after-before), etc)
-AMT 'thin-slice' rating of rapport: the rating of rapport for each 30-second slice of the tutoring videos with Jaden and a participant, in addition to a final rapport rating which is the average of all ratings from the individual slices for a certain participant.

Importantly, the AMT ratings of rapport are only available for participants whose video is of high quality. Therefore, the final database will include these three sets of information only for a subset of participants, and this subset is what we will use for the data analysis. 

```python
MergedDf = getUsableVideos(learning,participantData)[0]
UsableVideos = getUsableVideos(learning,participantData)[1]

full_usabledatabase = getFullData(rapport, UsableVideos, MergedDf)
```
### Function: getUsableVideos

First, we define a function called getUsableVideos, which has two goals:
- It merges the participant demographic data with the learning information for all participants, outputing a merged dataframe that accomplishes the first two THINGS mentioned above (in the outputs below: mergeddf)
- From said merged dataframe, it subsets the participants whose video has a high quality, and thus has the AMT rapport ratings (in the outputs below: UsableVideos)

```python
def getUsableVideos(learning,participantData):
    ""This functions returns the usable videos by (1) merging participant and learning data (and deleting a repeated column: 'Study_Condition') 
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
```

### Function: getFullData
Now, we will merge the AMT rapport ratings with the database containing the demographic and learning information for participants whose video is of high quality. In order to do this, we call getFullData. As the format of the AMT ratings sheet is not the same as the format of the merged dataframe including demographic and learning information, first we created a dataframe with the AMT ratings in the same format as the latter. 

```python
def getFullData(rapport, UsableVideos, mergeddf):
    """This function returns a database merging the merged usable data UsableVideos, with the rapport ratings that AMT workers gave for each slice of 
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

```

Here is how the final database looks like:

<img src="https://user-images.githubusercontent.com/65661142/118037237-dc136d80-b36d-11eb-987a-5a5b342d161a.png" width="90%"></img>

## <a name="analyses"></a>Data analysis

For the data analysis of these data, I will analyze condition differences on student's rapport (both self-reported on the post-tutoring session surveys, and the AMT-rated “thin-slice” rapport) and learning improvements from an algebra test done before the tutoring session with Jaden and a test done after. 

```python
interesting_columns= ['Learning_gain_total','Learning_gain_conc','Learning_gain_proc','AMT_Rapport_Average', 'self_report_Rapport_Average']
dataAnalysis(interesting_columns, full_usabledatabase)
```

### Function: dataAnalysis

This function consists of all the different data analyses that we will perform with these data. In particular, it is composed of ANOVAs with condition as the independent variable and the different learning gains and rapport measures as the dependent variables; linear regressions with the same variables and some regressors such as gender and previous algebra experience; and a t-test between the two rapport measures: AMT ratings of rapport, and self-reported ratings of rapport. 

```python
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
```    

Here are the outputs of said function:

### Descriptives of the five variables of interest: total learning gains (conc + proc), conceptual learning gains, procedural learning gains, AMT rapport ratings and self-report rapport ratings.


<img src="https://user-images.githubusercontent.com/65661142/118035271-4b3b9280-b36b-11eb-8535-df1499066a9d.png" width="90%"></img> 
### Boxplots by Condition of the five variables of interest: total learning gains (conc + proc), conceptual learning gains, procedural learning gains, AMT rapport ratings and self-report rapport ratings.

#### Total learning gains
<img src="https://user-images.githubusercontent.com/65661142/118031174-84bdcf00-b366-11eb-8261-8375c2faf8a2.png" width="90%"></img>
#### Conceptual learning gains
<img src="https://user-images.githubusercontent.com/65661142/118031353-b9ca2180-b366-11eb-9df7-268d3ac8ec5d.png" width="90%"></img> 
#### Procedural learning gains
<img src="https://user-images.githubusercontent.com/65661142/118031357-ba62b800-b366-11eb-9f8f-a9f4841d3526.png" width="90%"></img> 
#### AMT rapport ratings
<img src="https://user-images.githubusercontent.com/65661142/118040560-f8190e00-b371-11eb-8820-e3da34d608b3.png" width="90%"></img>
#### Self-report rapport ratings
<img src="https://user-images.githubusercontent.com/65661142/118031403-c6e71080-b366-11eb-9f07-f7c6fbfd34f6.png" width="90%"></img>  

### ANOVAs by Condition of the five variables of interest: total learning gains (conc + proc), conceptual learning gains, procedural learning gains, AMT rapport ratings and self-report rapport ratings.
<img src="https://user-images.githubusercontent.com/65661142/118035565-a79eb200-b36b-11eb-9e31-f101a6dc336f.png" width="90%"></img> 


### Linear Regressions: Condition ~ the five variables of interest: total learning gains (conc + proc), conceptual learning gains, procedural learning gains, AMT rapport ratings and self-report rapport ratings.

These regressions were performed because they had already been done previously by another researcher, and we wanted to rerun the analyses with the correct data, the participants whose video was good quality, and add the regression with the newly-acquired AMT rapport ratings.
#### Total learning gains
<img src="https://user-images.githubusercontent.com/65661142/118033714-6dccac00-b369-11eb-93ac-c4c4e502b1d8.png" width="90%"></img>
#### Conceptual learning gains
<img src="https://user-images.githubusercontent.com/65661142/118033718-6e654280-b369-11eb-85bc-52fca8dc7197.png" width="90%"></img> 
#### Procedural learning gains
<img src="https://user-images.githubusercontent.com/65661142/118033720-6efdd900-b369-11eb-8ede-5649e5254b0e.png" width="90%"></img> 
#### AMT rapport ratings
<img src="https://user-images.githubusercontent.com/65661142/118033721-6efdd900-b369-11eb-95db-699572c7838e.png" width="90%"></img>
#### Self-report rapport ratings
<img src="https://user-images.githubusercontent.com/65661142/118033723-6f966f80-b369-11eb-8562-199af1219ef0.png" width="90%"></img>

### Linear Regressions with regressors: Condition ~ the five variables of interest: total learning gains (conc + proc), conceptual learning gains, procedural learning gains, AMT rapport ratings and self-report rapport ratings. Regressors were Student_Gender + Grade + Algebra_experience.

#### Total learning gains
<img src="https://user-images.githubusercontent.com/65661142/118033724-6f966f80-b369-11eb-9062-f7152a491d1e.png" width="90%"></img>
#### Conceptual learning gains
<img src="https://user-images.githubusercontent.com/65661142/118033725-6f966f80-b369-11eb-9266-a21c06cea996.png" width="90%"></img>
#### Procedural learning gains
<img src="https://user-images.githubusercontent.com/65661142/118033726-702f0600-b369-11eb-99b4-c8af2f231913.png" width="90%"></img> 
#### AMT rapport ratings
<img src="https://user-images.githubusercontent.com/65661142/118033727-702f0600-b369-11eb-82cc-462c3c69ccf4.png" width="90%"></img>
#### Self-report rapport ratings
<img src="https://user-images.githubusercontent.com/65661142/118033728-702f0600-b369-11eb-9aa3-be4dbda92462.png" width="90%"></img> 

### t-test between different rapport ratings:

We also computed a t-test to investigate differences between AMT rapport ratings and self-report rapport ratings. 

#### Descriptives
<img src="https://user-images.githubusercontent.com/65661142/118033192-d23b3b80-b368-11eb-8c34-ebbcac34842b.png" width="45%"></img>
<img src="https://user-images.githubusercontent.com/65661142/118033195-d2d3d200-b368-11eb-8da6-5950e382c354.png" width="45%"></img> 

#### Boxplot
<img src="https://user-images.githubusercontent.com/65661142/118031401-c64e7a00-b366-11eb-914d-20131a22af39.png" width="90%"></img> 

### Statistics
<img src="https://user-images.githubusercontent.com/65661142/118032560-1b3ec000-b368-11eb-8154-b0c7393efb6a.png" width="90%"></img> 


## <a name="discussion"></a>Discussion and Future directions

There are no significant effects throughout this data analysis. This might be because the new dataset, which included only participants with videos of high quality, reduced the data points considerably. Moreover, it has been claimed that merely calculating the average of rapport for a full video is not the most useful way to investigate the development of rapport, as rapport is constantly changing (Madaio, Peng, Ogan, & Cassell, 2018; Sinha & Cassell, 2015). Therefore, in the future, we will study not the average rating of rapport, but the change in rapport throughout the whole interaction. A more sophisticated analysis that will be conducted will use Granger causality to understand how an agent’s social utterance in one thin-slice window may “Granger-cause” an increase in rapport in the subsequent slice. We can then use this measure to see whether the amount of increase in rapport vary between conditions, and whether that influences learning gains.  

## <a name="bibliography"></a>Bibliography

Madaio, M., Peng, K., Ogan, A., & Cassell, J. (2018). A climate of support: a process-oriented analysis of the impact of rapport on peer tutoring. International Society of the Learning Sciences, Inc.[ISLS].

Sinha, T., & Cassell, J. (2015, November). We click, we align, we learn: Impact of influence and convergence processes on student learning and rapport building. In Proceedings of the 1st Workshop on Modeling INTERPERsonal SynchrONy And infLuence (pp. 13-20).

## <a name="learned"></a>What I learned from this course

Before this semester, I didn't know what GitHub was, I never succeeded at changing directory in the terminal and I definitely could not have written this script! I had taken some DataCamp classes on data analysis last semester, so I vagely knew what panda and matplotlib were, but that was the extent of my coding experience. This semester, learning how to code was really my goal, and I can say that I'm happy with my level now. Of course, there are a lot of programs that I can't personally write, but I do understand the general thinking behind a code, and how to spell out the requirements of a program so that other people can write it. Moreover, doing this project I understood the value of feedback: I decided to do functions after I got feedback saying that it is much clearer to have a functions.py file which explains everything, and not that much code on the main.py program. 

All in all, I learned immensely about the way of thinking that is required to code, and I'm very glad that I took this class. Thank you!

