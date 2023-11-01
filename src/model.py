from database import MongoDatabase
import tensorflow as tf
import numpy as np
import json

client = MongoDatabase('test_database', 'test_collection')
client.connect()

json_datas = json.load(open('../database/data/data.json'))
MongoDatabase.insert(json_datas)

datas = MongoDatabase.get_datas()

global text
text = ""

print(datas)
# Tokenização do texto
tokenizer = tf.keras.preprocessing.text.Tokenizer()

for data in datas:
    tokenizer.fit_on_texts([data['text']])
    print(data['text'])

total_words = len(tokenizer.word_index) + 1

# Sequências de treinamento
input_sequences = []
for i in range(1, len(text.split())):
    n_gram_sequence = text.split()[:i+1]
    input_sequences.append(n_gram_sequence)


# Preparação de dados de entrada e saída
max_sequence_length = max([len(seq) for seq in input_sequences])
sequences = tokenizer.texts_to_sequences(input_sequences)
sequences = np.array(tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=max_sequence_length, padding='pre'))
x, y = sequences[:, :-1], sequences[:, -1]

# Conversão de y em matriz one-hot
y = tf.keras.utils.to_categorical(y, num_classes=total_words)

# Verificações
print("Total unique words:", total_words)
print("Dimensions of x:", x.shape)
print("Dimensions of y:", y.shape)

# Construção do modelo
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Embedding(total_words, 100, input_length=max_sequence_length - 1))
model.add(tf.keras.layers.LSTM(100))
model.add(tf.keras.layers.Dense(total_words, activation='softmax'))

# Compilação do modelo
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Treinamento do modelo
model.fit(x, y, epochs=50000)

# Função para gerar texto
def generate_text(seed_text, next_words, model, max_sequence_length):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = tf.keras.preprocessing.sequence.pad_sequences([token_list], maxlen=max_sequence_length-1, padding='pre')
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

# Geração de texto
generated_text = generate_text("Text for", 2, model, max_sequence_length)
print(generated_text)
