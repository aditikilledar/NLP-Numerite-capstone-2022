# capstone-2022
Tasks for ESA:
- [ ] replace nltk.pos_tagger w/ benepar POS tagger in IIRU
- [ ] find accuracies and evaluate
- [ ] make a list of known problems and constraints
- [ ] write the paper
- [ ] finalise report

Review 3: November 18 2022
-> Need FULL Implementation by then

here seems to be some compatibility issue between spacy v3 and neuralcoref. Here are the steps I did to make it work:

Setup a python3.7 on conda env and conda install -c anaconda git

As per stated in README.md,

git clone https://github.com/huggingface/neuralcoref.git

cd neuralcoref

pip install -r requirements.txt

pip install -e .

At this stage, your spacy version should be 2.3.x (verify using pip show spacy), because the requirements.txt did explicitly stated that spacy version has to be <3.0.0. Hence, DO NOT execute pip install -U spacy, which would upgrade your spacy version to beyond 3.0.0.

Execute python -m spacy download en to obtain your English Model.

Summary of key item versions:

Python==3.7.10
spacy==2.3.5
neuralcoref==4.0
Hope this helped! :)

![Gantt Chart](https://github.com/aditikilledar/capstone-2022/blob/a7f2c973cb202794c00baf0c40b2f60b1bdcde1e/UE19CS390B_REVIEW_1.pptx.jpg)
