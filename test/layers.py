import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import keras

numbers = [keras.layers.LSTM(10) for _ in range(1000)]
for number in numbers: print('\n', number.get_config())
