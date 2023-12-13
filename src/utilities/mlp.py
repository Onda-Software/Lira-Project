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
model.fit(x_train, y_train, epochs=60000)
model.summary()

# Teste do modelo
x_test1 = tf.constant([[8, 7]])
x_test2 = tf.constant([[10, 30]])
x_test3 = tf.constant([[2, 9]])

# Realizar a previsão como forma de teste
prediction1 = model.predict(x_test1)
prediction1 = np.squeeze(prediction1)

end_time = time.time()
print("Excecution time is: ", end_time - start_time)

while True:
    value1 = int(input("\nFirst value for sum prediction:  "))
    value2 = int(input("Second value for sum prediction: "))
    prediction = np.squeeze(model.predict(tf.constant([[value1, value2]])))
    print("Prediction value: ", prediction)
    print("Expected: ", tf.keras.backend.eval(value1 + value2))
