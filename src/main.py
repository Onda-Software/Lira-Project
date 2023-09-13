import tensorflow as tf
import numpy as np

# Conjunto de dados de entrada
x_train = tf.constant([
    [1, 2],
    [3, 4],
    [5, 6],
    [7, 8],
    [9, 10],
    [11, 12],
    [13, 14],
    [15, 16],
    [17, 18],
    [19, 20]
])

# Conjunto de dadso de saída
y_train = tf.constant([
    [3],
    [7],
    [11],
    [19],
    [29],
    [39],
    [49],
    [59],
    [69],
    [79]
])

# Criação do modelo (construção senquencial com camadas de conexão completa)
model = tf.keras.Sequential([
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(64, activation='relu'),
  tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compilação do modelo
# Adam (Estimativa de Momento Adaptativo)
# MSE (Erros Quadráticos Médios)
model.compile(optimizer='adam', loss='mse')
model.fit(x_train, y_train, epochs=100)

# Teste do modelo (Não está preciso)
x_test = tf.constant([[7, 1]])

# Realizar a previsão como forma de teste
prediction = model.predict(x_test)
prediction = np.squeeze(prediction)

print("\nPredictions:", prediction)

# MLP, pesos e bias







import tensorflow as tf
import tensorflow_probability as tfp

# Pretend to load synthetic data set.
features = tfp.distributions.Normal(loc=0., scale=1.).sample(int(100e3))
labels = tfp.distributions.Bernoulli(logits=1.618 * features).sample()

# Specify model.
model = tfp.glm.Bernoulli()

# Fit model given data.
coeffs, linear_response, is_converged, num_iter = tfp.glm.fit(
    model_matrix=features[:, tf.newaxis],
    response=tf.cast(labels, dtype=tf.float32),
    model=model)
# ==> coeffs is approximately [1.618] (We're golden!)

print(coeffs)







import tensorflow_hub as hub

model = hub.KerasLayer("https://tfhub.dev/google/nnlm-en-dim128/2")
embeddings = model(["The rain in Spain.", "falls", "mainly", "In the plain!"])

print(embeddings.shape)  #(4,128)





import os
import shutil

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
import matplotlib.pyplot as plt

tf.get_logger().setLevel('ERROR')
