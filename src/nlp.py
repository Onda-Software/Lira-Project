import tensorflow as tf
import time

start_time = time.time()

tokenizer = tf.keras.layers.TextVectorization(
    max_tokens=1000,
    output_mode='int',
    output_sequence_length=30
)

x_train_text = ["Eu gosto de macas", "O sol esta brilhando", "Vamos ao parque"]
y_train_text = ["frutas", "tempo bom", "diversao ao ar livre"]

tokenizer.adapt(x_train_text)

x_train_encoded = tokenizer(x_train_text)
y_train_encoded = tokenizer(y_train_text)

vocab = tokenizer.get_vocabulary()

# Criar uma sequência de saída com uma dimensão a mais para corresponder ao tamanho do vocabulário
y_train_encoded = tf.keras.utils.to_categorical(y_train_encoded, num_classes=len(vocab))

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=len(vocab), output_dim=64, input_length=30),
    tf.keras.layers.LSTM(64, return_sequences=True), 
    tf.keras.layers.Dense(len(vocab), activation="softmax")
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
model.fit(x_train_encoded, x_train_encoded, epochs=100)

test = tf.constant([["Eu gosto de macas"]])
test_encoded = tokenizer(test)

prediction = model.predict(test_encoded)

predicted_indices = tf.argmax(prediction, axis=-1)[0].numpy()
print("\nValores dos índices previstos:", predicted_indices)

# Converter as previsões de volta para texto
predicted_sequence = []
for idx in predicted_indices:
    if idx < len(vocab):
        predicted_sequence.append(vocab[idx])
    else:
        predicted_sequence.append("<OOV>")  # Trate índices fora do vocabulário como OOV (out of vocabulary)

decoded_prediction = " ".join(predicted_sequence)

print("Sequência de previsão decodificada:", decoded_prediction)

end_time = time.time()
print("\nExcecution time is: ", end_time - start_time)
