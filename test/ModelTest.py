import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from multiprocessing import Process, Pipe
import gc, joblib ,keras, tensorflow as tf, numpy as np

gc.enable()

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

for _ in range (0, 10):
    model.train_on_batch(x=x, y=y)
    model.fit(x=x, y=y, epochs=10)

print(tf.shape(x)[0])
print(tf.shape(y)[0])
print(x.shape)
print(y.shape)
print(model.summary())

with open('./tokenizers/tokenizer.gz', 'wb') as hadle:
    joblib.dump(tokenizer, hadle)

def predict_text(seed_text, predict_length, model):
        
    tokenizer = joblib.load('./tokenizers/tokenizer.gz')

    for _ in range(predict_length):

        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = keras.preprocessing.sequence.pad_sequences([token_list], maxlen=3, padding='pre')
             
        predicted_probabilities = model.predict(token_list)[0]
        predicted_index = np.argmax(predicted_probabilities)
        output_word = ""
            
        for word, index in tokenizer.word_index.items():
             
            if(predicted_index == index):
                output_word = word
                break
            
        seed_text += " " + output_word
        
    return seed_text

print(predict_text('Teste', 3, model))
