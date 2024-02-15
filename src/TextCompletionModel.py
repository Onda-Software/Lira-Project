import datetime
import joblib
import keras
import numpy as np
import tensorflow as tf

class TextCompletionModel():

    def __init__(self, dataset) -> None:    
        self.dataset = dataset
    
    @staticmethod
    def load_model(path):
        return keras.models.load_model(path)

    def build_model(self, system="unix" ,debug=False, log=False):
        
        print("Version: ", tf.__version__)
        print("Eager mode: ", tf.executing_eagerly())
        print("GPU is", "available" if tf.config.list_physical_devices("GPU") else "NOT AVAILABLE")
        
        if debug == True:
            tf.debugging.experimental.enable_dump_debug_info(
                dump_root='./logs/dumps',
                tensor_debug_mode='FULL_HEALTH',
                circular_buffer_size=-1
            )
        
        tokenizer = keras.preprocessing.text.Tokenizer()
        input_sequences = []
        total_words = 0x00
        total_sequences = 0x00

        for data in self.dataset:
            text = data['text']
            tokenizer.fit_on_texts([text])
            
            for index in range(1, len(text.split())):
			    
                x_anagram_sequences = text.split()[:index]
                y_anagram_sequences = text.split()[index:]
                z_anagram_sequences = text.split()[index-1:index+1]
			    
                if(x_anagram_sequences!=[] and y_anagram_sequences!=[] and z_anagram_sequences!= []):   
                     
                    input_sequences.append(x_anagram_sequences)
                    input_sequences.append(y_anagram_sequences)
                    input_sequences.append(z_anagram_sequences)

                    total_sequences+=3
            
            input_sequences.append([text])
            print(text)
            for element in range(1, len(input_sequences)-1):
                
                if(input_sequences[element]==input_sequences[element-1]):
                    del input_sequences[element-1]
                    total_sequences-=1
        
        max_sequence_length = max([len(seq) for seq in input_sequences])
        
        sequences = tokenizer.texts_to_sequences(input_sequences)
        sequences = np.array(keras.preprocessing.sequence.pad_sequences(sequences, maxlen=max_sequence_length, padding='pre'))

        total_words = (len(tokenizer.word_index) + 1)

        x, y = sequences[:, :-1], sequences[:, -1]
        y = keras.utils.to_categorical(y, num_classes=total_words)
        
        print("============================================")
        print(f"Total unique sequences: ({total_sequences+1})")
        print(f"Total unique words: ({total_words})")
        print(f"Dimensions of x: ({x.shape})")
        print(f"Dimensions of y: ({y.shape})")
        print("============================================")
        
        model = keras.models.Sequential()
        model.add(keras.layers.Embedding(total_words, 100, input_length=max_sequence_length - 1))
        model.add(keras.layers.LSTM(100))
        model.add(keras.layers.Dense(total_words, activation='softmax'))

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        if log == True:

            log_dir = "./logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)   
            
            model.fit(x=x, y=y, validation_data=[x, y], epochs=1000, callbacks=[tensorboard_callback])
        
        else:
            model.fit(x=x, y=y, validation_data=[x, y], epochs=1000)
        
        model.summary()
        model.save(f"./models/{system}/sequential.keras")

        with open('./tokenizers/tokenizer.gz', 'wb') as hadle:
            joblib.dump(tokenizer, hadle)
    
    @staticmethod
    def predict_text(seed_text, predict_length, model):
        
        tokenizer = joblib.load('./tokenizers/tokenizer.gz')

        for _ in range(predict_length):

            token_list = tokenizer.texts_to_sequences([seed_text])[0]
            token_list = keras.preprocessing.sequence.pad_sequences([token_list], maxlen=12, padding='pre')
             
            predicted_probabilities = model.predict(token_list)[0]
            predicted_index = np.argmax(predicted_probabilities)
            output_word = ""
            
            for word, index in tokenizer.word_index.items():
                 
                if(predicted_index == index):
                    output_word = word
                    break
            
            seed_text += " " + output_word
        
        return seed_text
