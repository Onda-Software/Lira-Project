import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import tensorflow as tf
import numpy as np
from json import load

tokenizer = tf.keras.preprocessing.text.Tokenizer()

datas = load(open('./database/data//data.json'))
datas = [{"id": 1, "text": "Teste de anagrama neural"}]

input_sequences = []
total_words = 0x00
total_sequences = 0x00

for data in datas:
    text = data['text']
    tokenizer.fit_on_texts([text])
    
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

    input_sequences.append([text])

    for element in range(1, len(input_sequences)-1):

        if(input_sequences[element]==input_sequences[element-1]):
            del input_sequences[element-1]
            total_sequences-=1

print(input_sequences)

max_sequence_length = max([len(seq) for seq in input_sequences])
sequences = tokenizer.texts_to_sequences(input_sequences)
sequences = np.array(tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=max_sequence_length, padding='pre'))

total_words = (len(tokenizer.word_index) + 1)

x, y = sequences[:, :-1], sequences[:, -1]
y = tf.keras.utils.to_categorical(y, num_classes=total_words)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Embedding(total_words, 100, input_length=max_sequence_length - 1))
model.add(tf.keras.layers.LSTM(100))
model.add(tf.keras.layers.Dense(total_words, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(x, y, epochs=1000)

model.summary()

def predict_text(seed_text, next_words, model):

    for _ in range(next_words):

        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = tf.keras.preprocessing.sequence.pad_sequences([token_list], maxlen=(max_sequence_length-1), padding='pre')
        predicted_probabilities = model.predict(token_list)[0]
        
        # Escolher a próxima palavra com base na probabilidade
        predicted_index = np.argmax(predicted_probabilities)
        output_word = ""
         
        for word, index in tokenizer.word_index.items():
            if index == predicted_index:
                output_word = word
                break
        seed_text += " " + output_word
        
    return seed_text

print("=================================================================")
print(f"Total unique sequences: ({total_sequences+1})")
print(f"Total unique words: ({total_words})")
print(f"Dimensions of x: ({x.shape})")
print(f"Dimensions of y: ({y.shape})")
print("=================================================================")

print(predict_text("Teste", 3, model))
