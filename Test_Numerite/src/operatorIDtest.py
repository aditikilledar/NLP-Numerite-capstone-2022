import OperatorPrediction as opred
import pandas as pd
import warnings
warnings.simplefilter('ignore')

f = open('operator_pred_accuracy.txt', 'w')

# SVAMP
print('---------Running on SVAMP---------------')
f.write('SVAMP:\n')

ops = ['add', 'sub', 'div', 'mul']
for op in ops:
    df = pd.read_json(f'../data/SVAMP_Cleaned/{op}.json')
    questions = df['full_question'].tolist()
    operators = df['Type'].tolist()

    correct_pred = 0

    for i, q in enumerate(questions):
        pred = opred.predict_operation(q)
        ans = operators[i]
        if ans == 'Common-Division':
            ans = 'division'
        if ans.lower() == pred.lower():
            correct_pred += 1
        print(f'-----------{i + 1}/{len(questions)} done--------------------')

    accuracy = (correct_pred * 100) / len(questions)
    f.write(f'Accuracy for {op}:\t{accuracy}%\n')

#Singleop
print('-------------Running on Singleop------------------')
f.write('\nSingleOP:\n')
ops = ['add', 'sub', 'div', 'mul']
for op in ops:
    df = pd.read_json(f'../data/SingleOP_Clean/singleop{op}.json')
    questions = df['sQuestion'].tolist()
    operators = df['Type'].tolist()

    correct_pred = 0

    for i, q in enumerate(questions):
        pred = opred.predict_operation(q)
        ans = operators[i]
        if ans == 'Common-Division':
            ans = 'division'
        if ans.lower() == pred.lower():
            correct_pred += 1
        print(f'-----------{i + 1}/{len(questions)} done--------------------')

    accuracy = (correct_pred * 100) / len(questions)
    f.write(f'Accuracy for {op}:\t{accuracy}%\n')

f.close()
