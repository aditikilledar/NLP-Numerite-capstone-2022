from AMWPS import AMWPS
import pandas as pd
from timeit import default_timer as timer

ops = ['add', 'div', 'mul', 'sub']
f = open('singleop_operatorwise_accuracy.txt', 'w')

for op in ops:
    df = pd.read_json(f'../data/SingleOP_clean/singleop{op}.json')
    questions = df['sQuestion'].tolist()
    answers = df['lSolutions'].tolist()
    skipped_questions = []
    correct_pred = 0
    times = []
    for i, q in enumerate(questions):
        try:
            solver = AMWPS(q)
            solver.solve()
            ans = solver.solution
            if int(ans) == int(answers[i][0]):
                correct_pred += 1
        except:
            skipped_questions.append(q)
    
        print(f'------------------- {i}/{len(questions)} questions done --------------------------')

    accuracy = (correct_pred / len(questions)) * 100
    accuracy_higher = (correct_pred * 100)/(len(questions) - len(skipped_questions))

    f.write(f'Accuracy for {op} (including skipped questions):\t{accuracy}%\n')
    f.write(f'Accuracy for {op} (not including skipped questions:\t{accuracy_higher}%\n')
    f.write(f'Number of questions:\t{len(questions)}\n')
    f.write(f'Number of skipped questions:\t{len(skipped_questions)}\n\n\n')
    #print(data)
f.close()