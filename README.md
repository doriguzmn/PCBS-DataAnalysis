# PCBS-DataAnalysis
My project is part of the Rapport-Aware Peer Tutor, whose goal is to advance understanding of the nature of rapport development and its impact on learning processes and outcomes, in particular with virtual ECAs as tutors. The project is led by Justine Cassell. 

In order to do this, over 100 hours of data of students tutoring each other in algebra were collected and the verbal and nonverbal behaviors that contribute to the rapport between them were analyzed. Findings showed that tutoring pairs with greater rapport engage in more of the socially-supportive behaviors like help-offering, explanation-prompting, comprehension-monitoring, and self-explanations (from tutees) indicative of positive, supportive climates for learning. Students whose rapport with their partner deepens over time also solve more problems and learn more on a post-test. 

As a result of this work, the first computational model of rapport was developed, which allowed Justine's Cassell's team to design a virtual peer tutor, Jaden, that can develop rapport with a student to better support them in learning. 

My project will consist in evaluating the efficacy of rapport-building social components of a virtual peer tutoring system (i.e. Jaden) and its influence in the learning of the students. Importantly, three conditions based on different models of rapport were used: 

-Task-only (control): no social dialogue used at all. 

-Fixed model of rapport, where fixed rules were implemented for Jaden's use of social dialogue, informed by prior literature (e.g. Gradually increasing frequency and intimacy of self-disclosure).

-Adaptive model of rapport, where Jaden's use of social utterances is determined by social reasoning, based on the current rapport level (as determined by the rapport estimator).


I collected rapport ratings of 30-second slices from Jaden's tutoring sessions using Amazon Mechanical Turk (i.e. "thin-slice rapport), and I will use these data to evaluate the relationship between rapport and learning. First, I will analyze condition differences on student's rapport (both self-reported on the post-tutoring session surveys, and the observer-rated “thin-slice” rapport) and learning outcomes on a post-test. If time allows, I will conduct a more sophisticated analyses using Granger causality to understand how an agent’s social utterance in one thin-slice window may “Granger-cause” an increase in rapport in the subsequent slice. 






