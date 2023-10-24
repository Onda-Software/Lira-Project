from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf

# Dados de exemplo
text = "Este é um exemplo de previsão de texto usando TensorFlow em Python. Vamos construir um modelo de linguagem simples."

# Tokenização do texto
tokenizer = Tokenizer()
tokenizer.fit_on_texts([text])
total_words = len(tokenizer.word_index) + 1

# Sequências de treinamento
input_sequences = []
for i in range(1, len(text.split())):
    n_gram_sequence = text.split()[:i+1]
    input_sequences.append(n_gram_sequence)

# Padronização das sequências
max_sequence_length = max([len(seq) for seq in input_sequences])
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_length, padding='pre')

x, y = input_sequences[:, :-1], input_sequences[:, -1]

# Construção do modelo
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Embedding(total_words, 100, input_length=max_sequence_length - 1))
model.add(tf.keras.layers.LSTM(100))
model.add(tf.keras.layers.Dense(total_words, activation='softmax'))

# Compilação do modelo
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Treinamento do modelo
model.fit(x, y, epochs=100, verbose=1)

# Função para gerar texto
def generate_text(seed_text, next_words, model, max_sequence_length):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_length-1, padding='pre')
        predicted = model.predict_classes(token_list, verbose=0)
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word
    return seed_text

# Geração de texto
generated_text = generate_text("Este é", 10, model, max_sequence_length)
print(generated_text)
