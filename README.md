# Rapport-Aware Peer Tutor Data Analysis
My project is part of the Rapport-Aware Peer Tutor, whose goal is to advance understanding of the nature of the development of rapport and its impact on learning processes, in particular with virtual ECAs as tutors. The project is led by Justine Cassell. 

In order to study rapport in a human-human tutoring environment, over 100 hours of data of students tutoring each other in algebra were collected and the verbal and nonverbal behaviors that contribute to the development rapport between them were analyzed. Findings showed that tutoring pairs with greater rapport engage in more of the socially-supportive behaviors like help-offering, explanation-prompting, comprehension-monitoring, and self-explanations, all indicative of positive, supportive climates for learning (Madaio, Peng, Ogan, & Cassell, 2018; Sinha & Cassell, 2015). Students whose rapport with their partner deepens over time also solve more problems and learn more on a post-test. 

As a result of this work, the first computational model of rapport was developed, which allowed Cassell's team to design a virtual peer tutor, Jaden, that can develop rapport with a student to better support them in learning. 

My project will consist in evaluating the efficacy of rapport-building social components of a virtual peer tutoring system (i.e. Jaden) and its influence in the learning of the students. Importantly, three conditions based on different models of rapport were used by Jaden in its interactions with student tutees: 

-Task-only (control): no social dialogue used at all. 

-Fixed model of rapport, where fixed rules were implemented for Jaden's use of social dialogue, informed by prior literature (e.g. gradually increasing frequency and intimacy of self-disclosure).

-Adaptive model of rapport, where Jaden's use of social utterances is determined by social reasoning, based on the current rapport level (as determined by a rapport estimator built by Cassell's team).

#### Table of Contents

* [Defining the Functions](#functions)
* [Reading the Data](#data)
* [Data analysis](#analyses)
* [To Do](#future)
* [Bibliography](#bibliography)
* [What I learned from this course](#learned)

## <a name="functions"></a>Defining the Functions in functions.py

In functions.py, there are 3 functions defined, which will help us when we run the main.py code. First, we install the packages required.

```python
import pandas as pd
from scipy import stats
from statsmodels.formula.api import ols
import pingouin as pg
import matplotlib.pyplot as plt
import seaborn as sns
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


