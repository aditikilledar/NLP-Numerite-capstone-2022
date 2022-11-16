import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords

import torch
from transformers import BertTokenizer
from torch.utils.data import TensorDataset
from transformers import BertForSequenceClassification

from torch.utils.data import DataLoader, RandomSampler, SequentialSampler

def evaluate(dataloader_val):

        # model.eval()

        loss_val_total = 0
        predictions, true_vals = [], []

        for batch in dataloader_val:

                batch = tuple(b.to(device) for b in batch)

                inputs = {'input_ids':      batch[0],
                          'attention_mask': batch[1],
                          'labels':         batch[2],
                          }

                # disable gradient calculation
                with torch.no_grad():
                        outputs = model(**inputs)

                loss = outputs[0]
                logits = outputs[1]
                loss_val_total += loss.item()

                logits = logits.detach().cpu().numpy()
                label_ids = inputs['labels'].cpu().numpy()
                predictions.append(logits)
                true_vals.append(label_ids)

        #     loss_val_avg = loss_val_total/len(dataloader_val)

        predictions = np.concatenate(predictions, axis=0)
        true_vals = np.concatenate(true_vals, axis=0)

        return predictions, true_vals

def decode_prediction(pred):
        label_dict = {'multiplication': 0, 'subtraction': 1, 'addition': 2, 'division': 3}
        pred_flat = np.argmax(pred, axis=1).flatten()
        y_pred = [k for k, v in label_dict.items() if pred_flat[0] == v]
        return y_pred

def clean_text(text):
        """
        text: a string

        return: modified initial string
        """
        REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
        BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
        # STOPWORDS = set(stopwords.words('english'))
        text = text.lower() # lowercase text
        text = REPLACE_BY_SPACE_RE.sub('', text) # replace REPLACE_BY_SPACE_RE symbols by space in text. substitute the matched string in REPLACE_BY_SPACE_RE with space.
        text = BAD_SYMBOLS_RE.sub('', text) # remove symbols which are in BAD_SYMBOLS_RE from text. substitute the matched string in BAD_SYMBOLS_RE with nothing.
        text = ''.join([i for i in text if not i.isdigit()])
        text = " ".join(text.split())
        return text

def predict_operation(user_input):
        df = pd.read_csv('data/combined.csv')
        df.drop(df.index,inplace=True)

        # user_input = 'In the fridge, there are 4 stacks of chocolate puddings, 7 stacks of brownies and 5 stacks of pasta salad. How many stacks of dessert are there?'
        user_input = clean_text(user_input)
        userdf = {"Type": ['Unknown'],
                  "Clean": [user_input],
                  "label": [3]
                  }
        userdf = pd.DataFrame(userdf)

        df = pd.concat([df, userdf], ignore_index = True)
        df = df.tail(1)

        # init tokenizer
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased',
                                                  do_lower_case=True)

        encoded_data_pred = tokenizer.batch_encode_plus(
                df.Clean.values,
                add_special_tokens=True,
                return_attention_mask=True,
                pad_to_max_length=True,
                max_length=256,
                return_tensors='pt'
        )

        input_ids_pred = encoded_data_pred['input_ids']
        attention_masks_pred = encoded_data_pred['attention_mask']
        labels_pred = torch.tensor(df.label.values)

        dataset_pred = TensorDataset(input_ids_pred, attention_masks_pred, labels_pred)

        device = 'cpu'
        dataloader_prediction = DataLoader(dataset_pred)

        #  encode values in labels
        label_dict = {'multiplication': 0, 'subtraction': 1, 'addition': 2, 'division': 3}
        model = BertForSequenceClassification.from_pretrained("bert-base-uncased",
                                                              num_labels=len(label_dict),
                                                              output_attentions=False,
                                                              output_hidden_states=False)

        model.to(device)
        model.load_state_dict(torch.load('../models/ep2finetuned_BERT_epoch_2.model', map_location=torch.device('cpu')))
        model.eval()

        loss_val_total = 0
        predictions, true_vals = [], []

        for batch in dataloader_prediction:
                batch = tuple(b.to(device) for b in batch)

                inputs = {'input_ids': batch[0],
                          'attention_mask': batch[1],
                          'labels': batch[2],
                          }

                # disable gradient calculation
                with torch.no_grad():
                        outputs = model(**inputs)

                loss = outputs[0]
                logits = outputs[1]
                loss_val_total += loss.item()

                logits = logits.detach().cpu().numpy()
                label_ids = inputs['labels'].cpu().numpy()
                predictions.append(logits)
                true_vals.append(label_ids)

        #     loss_val_avg = loss_val_total/len(dataloader_val)

        predictions = np.concatenate(predictions, axis=0)
        # true_vals = np.concatenate(true_vals, axis=0)

        return decode_prediction(predictions)[0]
