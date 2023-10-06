import tensorflow as tf
import numpy as np
import time

start_time = time.time()

# Conjunto de dados de entrada
x_train = tf.constant([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12], [13, 14], [15, 16], [17, 18], [19, 20]])

# Conjunto de dadso de saída
y_train = tf.constant([[3], [7], [11], [15], [19], [23], [27], [31], [35], [39]])

# Criação do modelo (construção senquencial com camadas de conexão completa)
model = tf.keras.Sequential([
   tf.keras.layers.Dense(1, use_bias=False),
])

# Compilação do modelo
# Adam (Estimativa de Momento Adaptativo)
# MSE (Erros Quadráticos Médios)
model.compile(optimizer='adam', loss='mse')
model.fit(x_train, y_train, epochs=100000)

# Teste do modelo
x_test1 = tf.constant([[8, 7]])
x_test2 = tf.constant([[10, 30]])
x_test3 = tf.constant([[2, 9]])

# Realizar a previsão como forma de teste
prediction1 = model.predict(x_test1)
prediction1 = np.squeeze(prediction1)

prediction2 = model.predict(x_test2)
prediction2 = np.squeeze(prediction2)

prediction3 = model.predict(x_test3)
prediction3 = np.squeeze(prediction3)

end_time = time.time()

print("\nPredictions:", prediction1, " | ", prediction2, " | ", prediction3)
print("Valores Esperados:", x_test1[0][0] + x_test1[0][1], " | ", x_test2[0][0] + x_test2[0][1], " | ", x_test3[0][0] + x_test3[0][1])

print("Excecution time is: ", end_time - start_time)
