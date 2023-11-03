from database import MongoDatabase
import tensorflow as tf
import numpy as np
from json import load

client = MongoDatabase('test', 'test')
client.connect()

json_datas = load(open('../database/data/data.json'))
MongoDatabase.insert(json_datas)

datas = MongoDatabase.get_datas()

global text
text = ""

print(len(datas))
# Tokenização do texto
tokenizer = tf.keras.preprocessing.text.Tokenizer()
input_sequences = []
total_words = ""

for data in datas:
    text = data['text']
    tokenizer.fit_on_texts([text])


    for i in range(1, len(text.split())):
        n_gram_sequence = text.split()[:i+1]
        input_sequences.append(n_gram_sequence)

print(input_sequences)
# Preparação de dados de entrada e saída
max_sequence_length = max([len(seq) for seq in input_sequences])
sequences = tokenizer.texts_to_sequences(input_sequences)

model = tf.keras.models.load_model('./models/model.keras')

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
while True:
    
    text_predict = str(input("\nPlease enter a pre text for predict: "))
    size_predict = int(input("Plese enter with a size for predict: "))
    generated_text = generate_text(text_predict, size_predict, model, max_sequence_length)
    print(f"\nPredicted text is: {generated_text}\n")

