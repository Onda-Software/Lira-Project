import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

import tensorflow as tf
import numpy as np
import joblib
import datetime

class TextCompletionModel():

    def __init__(self, dataset) -> None:
    
        self.dataset = dataset

    def load_model(self, path):
    
        return tf.keras.models.load_model(path)
        
    def build_model(self, debug=False, log=False):
   
        print("Version: ", tf.__version__)
        print("Eager mode: ", tf.executing_eagerly())
        print("GPU is", "available" if tf.config.list_physical_devices("GPU") else "NOT AVAILABLE")
        
        if debug == True:
            tf.debugging.experimental.enable_dump_debug_info(
                dump_root='../logs/dumps',
                tensor_debug_mode='FULL_HEALTH',
                circular_buffer_size=-1
            )
        
        tokenizer = tf.keras.preprocessing.text.Tokenizer()
        input_sequences = []
        total_words = ""

        for data in self.dataset:

            text = data['text']
            tokenizer.fit_on_texts([text])

            total_words = len(tokenizer.word_index) + 1

            for i in range(1, len(text.split())):

                n_gram_sequence = text.split()[:i+1]
                input_sequences.append(n_gram_sequence)

        max_sequence_length = max([len(seq) for seq in input_sequences])
        
        sequences = tokenizer.texts_to_sequences(input_sequences)
        sequences = np.array(tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=max_sequence_length, padding='pre'))

        x, y = sequences[:, :-1], sequences[:, -1]
        y = tf.keras.utils.to_categorical(y, num_classes=total_words)
        
        print("=================================================================")
        print(f"Total unique words: ({total_words})")
        print(f"Dimensions of x: ({x.shape})")
        print(f"Dimensions of y: ({y.shape})")
        print("=================================================================")
    
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Embedding(total_words, 100, input_length=max_sequence_length - 1))
        model.add(tf.keras.layers.LSTM(100))
        model.add(tf.keras.layers.Dense(total_words, activation='softmax'))

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        if log == True:

            log_dir = "../logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)   
            
            model.fit(x=x, y=y, validation_data=[x, y], epochs=1000, callbacks=[tensorboard_callback])
        
        else:
            model.fit(x=x, y=y, validation_data=[x, y], epochs=1000)

        model.summary()
        model.save("./models/sequential.keras")

        with open('./tokenizers/tokenizer.gz', 'wb') as hadle:
            joblib.dump(tokenizer, hadle)
        

    def predict_text(self, seed_text, next_words, model):
             
        tokenizer = joblib.load('./tokenizers/tokenizer.gz')

        for _ in range(next_words):

            token_list = tokenizer.texts_to_sequences([seed_text])[0]
            token_list = tf.keras.preprocessing.sequence.pad_sequences([token_list], maxlen=13, padding='pre')
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
