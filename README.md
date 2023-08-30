# Numerite
Our capstone paper, titled "Numerite: An Automatic Math Word Problem Solver" was accepted at the conference RANLP 2023 (Recent Advances in Natural Language Processing), held in Bulgaria.

After a thorough literary review, we found that while research had moved on to solving more complex math word problems, models still struggled with solving basic simple word problems (2) (3) when given challenging wording and sentence structure (like in the SVAMP dataset)— we wanted to explore ways to fill this research gap and get better at solving math word problems automatically with more accuracy.

This paper explores techniques to automatically solve math word problems like: "Aditi has 5 apples. She buys 2 more apples. How many does she have now?" and other basic arithmetic word problems (simple addition, division, multiplication and subtraction) at the primary school level. (This was before ChatGPT!)

We used a hybrid NLP method to achieve this, combining intermediates from both rule-based and deep-learning techniques to extract information(1).

Our model, Numerite, performs better than the SOTA approaches by 6% on SVAMP (an extra challenging word problems dataset).


### Summary of key versions:
Python==3.7.10
spacy==2.3.5
neuralcoref==4.0
Hope this helped! :)

#### References
1) Mandal, Sourav, Sekh, Arif Ahmed, and Naskar, Sudip Kumar. ‘Solving Arithmetic Word Problems: A Deep Learning Based Approach’. 1 Jan. 2020 : 2521 – 2531.
2)Sowmya S Sundaram, Sairam Gurajada, Marco Fisichella, Deepak P,
Savitha Sam Abraham, “Why are NLP Models Fumbling at Elementary
Math? A Survey of Deep Learning based Word Problem Solvers, ’2022’
doi: 10.48550/arXiv.2205.1568
3)Arkil Patel, Satwik Bhattamishra, Navin Goyal, “Are NLP Models really
able to Solve Simple Math Word Problems?, ’2021’ Annual Conference
of the North American Chapter of the Association for Computational
Linguistics
