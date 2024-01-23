import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
import keras
from multiprocessing import Process, Pipe

tokenizer = keras.preprocessing.text.Tokenizer()
datas = [{"id": 1, "text": "Teste de anagrama neural"}]

input_sequences = []
text_divisions = []

def insert_element(element_list, connection):
    
    filtered_elements = []

    for element in element_list:
        if(not element in filtered_elements and element != []):
            filtered_elements.append(element)
    
    connection.send(filtered_elements)
    connection.close()

for data in datas:
    text = data['text']
    tokenizer.fit_on_texts([text])
    
    for index in range(0, len(text.split())):
    
        text_divisions += [
            text.split()[:],
            [text.split()[index]],
            text.split()[:index],
            text.split()[index:],
            text.split()[index-1:index+1],
        ]

    parent_conn, child_conn = Pipe()
    process = Process(target=insert_element, args=(text_divisions, child_conn,))
    process.start()

    input_sequences = parent_conn.recv()
    if (process.join()): pass

for id in range(1, len(input_sequences)):
    print(f'\n{input_sequences[id]}')
print()

max_sequence_length = max([len(seq) for seq in input_sequences])
sequences = tokenizer.texts_to_sequences(input_sequences)
sequences = np.array(keras.preprocessing.sequence.pad_sequences(sequences, maxlen=max_sequence_length, padding='pre'))

total_words = (len(tokenizer.word_index) + 1)

x, y = sequences[:, :-1], sequences[:, -1]
y = keras.utils.to_categorical(y, num_classes=total_words)

model = keras.models.Sequential()
model.add(keras.layers.Embedding(total_words, 100, input_length=max_sequence_length - 1))
model.add(keras.layers.LSTM(100))
model.add(keras.layers.Dense(total_words, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(x, y, epochs=1000)

model.summary()

def predict_text(seed_text, next_words, model):

    for _ in range(next_words):

        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = keras.preprocessing.sequence.pad_sequences([token_list], maxlen=(max_sequence_length-1), padding='pre')
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
#print(f"Total unique sequences: ({total_sequences+1})")
print(f"Total unique words: ({total_words})")
print(f"Dimensions of x: ({x.shape})")
print(f"Dimensions of y: ({y.shape})")
print("=================================================================")

print(predict_text("Teste", 3, model))
