import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

#read the rapport data
rapport = pd.read_excel ('AllSlicesData_NiceFormat_edited.xlsx')

#read the participant and learning data
learning = pd.read_excel('Dori-RAPT_WoZ_2019_learning-gain_condition.xlsx')

participantdata=pd.read_excel('Dori-RAPT_WoZ_participant_data.xlsx')

#to merge the participant and learning data
mergeddf = learning.merge(participantdata, on='Participant')

#Now, I'll subset the subject with usable videos (some videos did not have enough quality

usablevideos = mergeddf[mergeddf["Usable"]=="Y"]

with pd.ExcelWriter('MergedData.xlsx') as writer:  
	mergeddf.to_excel(writer, sheet_name='AllVideos', index=False)
	usablevideos.to_excel(writer, sheet_name='UsableVideos', index=False)


#to perform the ANOVA on learning gains by condition, I need to get the data for each condition individually:
task_only=[]
for i, row in usablevideos.iterrows():
	if row["Condition"] == "Task-only":
		task_only.append(row['Learning_gain_total'])

fixed=[]

for i, row in usablevideos.iterrows():
	if row["Condition"] == "Fixed":
		fixed.append(row['Learning_gain_total'])

adaptive=[]

for i, row in usablevideos.iterrows():
	if row["Condition"] == "Adaptive":
		adaptive.append(row['Learning_gain_total'])


#to get the f and p value:
fvalue, pvalue=stats.f_oneway(task_only,fixed,adaptive)
print(fvalue, pvalue)

#to perform the ANOVA on learning gains by condition, I need to get the data for each condition individually:
task_only=[]
for i, row in usablevideos.iterrows():
	if row["Condition"] == "Task-only":
		task_only.append(row['Average_Rapport (average of survey items 1-8)'])

fixed=[]

for i, row in usablevideos.iterrows():
	if row["Condition"] == "Fixed":
		fixed.append(row['Average_Rapport (average of survey items 1-8)'])

adaptive=[]

for i, row in usablevideos.iterrows():
	if row["Condition"] == "Adaptive":
		adaptive.append(row['Average_Rapport (average of survey items 1-8)'])

#to get the f and p value:
fvalue, pvalue=stats.f_oneway(task_only,fixed,adaptive)
print(fvalue, pvalue)

