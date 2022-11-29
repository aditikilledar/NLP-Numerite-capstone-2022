from AMWPS import AMWPS
import pandas as pd

ops = ['add', 'div', 'mul', 'sub']
f = open('svamp_operatorwise_accuracy.txt', 'w')

for op in ops:
    df = pd.read_json(f'../data/SVAMP_Cleaned/{op}.json')
    questions = df['full_question'].tolist()
    answers = df['Answer'].tolist()
    
    correct_pred = 0
    skipped_questions = []

    for i, q in enumerate(questions):
        try:
            solver = AMWPS(q)
            solver.solve()
            if int(solver.solution) == int(answers[i]):
                correct_pred += 1
        except:
            skipped_questions.append(q)

        print(f'------------------- {i}/{len(questions)} questions done --------------------------')

    accuracy = (correct_pred * 100) / len(questions)
    accuracy_higher = (correct_pred * 100) / (len(questions) - len(skipped_questions))

    f.write(f'Accuracy for {op} (including skipped questions):\t{accuracy}%\n')
    f.write(f'Accuracy for {op} (not including skipped questions:\t{accuracy_higher}%\n')
    f.write(f'Number of questions:\t{len(questions)}\n')
    f.write(f'Number of skipped questions:\t{len(skipped_questions)}\n\n\n')
        
f.close()