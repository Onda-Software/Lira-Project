import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import tensorflow as tf
import numpy as np
from json import load

tokenizer = tf.keras.preprocessing.text.Tokenizer()

datas = load(open('./database/data//data.json'))

input_sequences = []
total_words = 0x00
total_sequences = 0x00

for data in datas:
    text = data['text']
    tokenizer.fit_on_texts([text])
    total_words = len(tokenizer.word_index)

    for index in range(1, len(text.split())):
     
        x_anagram_sequences = text.split()[:index]
        y_anagram_sequences = text.split()[index:]
        z_anagram_sequences = text.split()[index-1:index+1]

        if(x_anagram_sequences!=[] and y_anagram_sequences!=[] and z_anagram_sequences!= []):   

            input_sequences.append(x_anagram_sequences)
            total_sequences+=1

            input_sequences.append(y_anagram_sequences)
            total_sequences+=1

            input_sequences.append(z_anagram_sequences)
            total_sequences+=1

    input_sequences.append(text)

    for element in range(1, len(input_sequences)-1):

        if(input_sequences[element]==input_sequences[element-1]):
            del input_sequences[element-1]
            total_sequences-=1

print(input_sequences)

max_sequence_length = max([len(seq) for seq in input_sequences])
sequences = tokenizer.texts_to_sequences(input_sequences)
sequences = np.array(tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=max_sequence_length, padding='pre'))

x, y = sequences[:, :-1], sequences[:, -1]

print("=================================================================")
print(f"Total unique sequences: ({total_sequences+1})")
print(f"Total unique words: ({total_words})")
print(f"Dimensions of x: ({x.shape})")
print(f"Dimensions of y: ({y.shape})")
print("=================================================================")

