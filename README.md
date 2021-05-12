# Rapport-Aware Peer Tutor Data Analysis
My project is part of the Rapport-Aware Peer Tutor, whose goal is to advance understanding of the nature of the development of rapport and its impact on learning processes, in particular with virtual ECAs as tutors. The project is led by Justine Cassell. 

In order to study rapport in a human-human tutoring environment, over 100 hours of data of students tutoring each other in algebra were collected and the verbal and nonverbal behaviors that contribute to the development rapport between them were analyzed. Findings showed that tutoring pairs with greater rapport engage in more of the socially-supportive behaviors like help-offering, explanation-prompting, comprehension-monitoring, and self-explanations, all indicative of positive, supportive climates for learning (Madaio, Peng, Ogan, & Cassell, 2018; Sinha & Cassell, 2015). Students whose rapport with their partner deepens over time also solve more problems and learn more on a post-test. 

As a result of this work, the first computational model of rapport was developed, which allowed Cassell's team to design a virtual peer tutor, Jaden, that can develop rapport with a student to better support them in learning. 

My project will consist in evaluating the efficacy of rapport-building social components of a virtual peer tutoring system (i.e. Jaden) and its influence in the learning of the students. Importantly, three conditions based on different models of rapport were used by Jaden in its interactions with student tutees: 

-Task-only (control): no social dialogue used at all. 

-Fixed model of rapport, where fixed rules were implemented for Jaden's use of social dialogue, informed by prior literature (e.g. gradually increasing frequency and intimacy of self-disclosure).

-Adaptive model of rapport, where Jaden's use of social utterances is determined by social reasoning, based on the current rapport level (as determined by a rapport estimator built by Cassell's team).

#### Table of Contents

* [Code General Description](#code)
* [Reading the Data](#data)
* [Data analysis](#analyses)
* [To Do](#future)
* [Bibliography](#bibliography)
* [What I learned from this course](#learned)

## <a name="data"></a>Reading the Data

## <a name="data"></a>Reading the Data

First, we install the packages required.

```python
import pandas as pd
from scipy import stats
from statsmodels.formula.api import ols
import pingouin as pg
import matplotlib.pyplot as plt
import seaborn as sns
```

### getUsableVideos

First, we define a function called getUsableVideos, which requires the 

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

## <a name="data"></a>Reading the Data

## <a name="analyses"></a>Data analysis

First, I will analyze condition differences on student's rapport (both self-reported on the post-tutoring session surveys, and the observer-rated “thin-slice” rapport) and learning outcomes on a post-test. 

## <a name="future"></a>To Do

If time allows, I will conduct a more sophisticated analyses using Granger causality to understand how an agent’s social utterance in one thin-slice window may “Granger-cause” an increase in rapport in the subsequent slice. 

## <a name="bibliography"></a>Bibliography

Madaio, M., Peng, K., Ogan, A., & Cassell, J. (2018). A climate of support: a process-oriented analysis of the impact of rapport on peer tutoring. International Society of the Learning Sciences, Inc.[ISLS].

Sinha, T., & Cassell, J. (2015, November). We click, we align, we learn: Impact of influence and convergence processes on student learning and rapport building. In Proceedings of the 1st Workshop on Modeling INTERPERsonal SynchrONy And infLuence (pp. 13-20).

## <a name="learned"></a>What I learned from this course


