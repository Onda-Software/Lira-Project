import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import datetime, joblib, keras, gc
import numpy as np
import tensorflow as tf

gc.enable()

class MultilayerPerceptron():

    def __init__(self, dataset) -> None:    
        self.dataset = dataset
    
    @staticmethod
    def load_model(path):
        return keras.models.load_model(path)

    def build_model(self, system="unix" ,debug=False, log=False):
        
        print("Version: ", tf.__version__)
        print("Eager mode: ", tf.executing_eagerly())
        print("GPU IS", "AVAILABLE" if tf.config.list_physical_devices("GPU") else "NOT AVAILABLE")
        
        if debug == True:
            tf.debugging.experimental.enable_dump_debug_info(
                dump_root='./logs/dumps',
                tensor_debug_mode='FULL_HEALTH',
                circular_buffer_size=-1
            )
        
        tokenizer = keras.preprocessing.text.Tokenizer()
        input_sequences = []
        total_sequences = 0
        iterator = 0
        print("\nLoading data...")

        for data in self.dataset:
            
            print(iterator)
            clean_seq = []
            iterator += 1
            text = data.text
            tokenizer.fit_on_texts([text])
            input_sequences.append(text.split()[:])
            
            for index in range(1, len(text.split())):
			    
                input_sequences.append(text.split()[index])
                input_sequences.append(text.split()[index:])
                input_sequences.append(text.split()[:index])
                input_sequences.append(text.split()[index-1:index+1])
			     
            for seq in input_sequences:
                if seq not in clean_seq:
                    clean_seq.append(seq)
            
            total_sequences += len(clean_seq)
            #input_sequences += clean_seq
             
            if(iterator % 97 == 0):
                  
                max_sequence_length = max(map(len, input_sequences))
                
                with open('database/max_sequence_length.txt', 'w') as writer:
                    writer.write(f"{max_sequence_length-1}") 
                
                sequences = tokenizer.texts_to_sequences(input_sequences)
                sequences = np.array(keras.preprocessing.sequence.pad_sequences(sequences, maxlen=max_sequence_length, padding='pre'))
                
                total_words = (len(tokenizer.word_index) + 1)
                input_sequences = []
                x, y = sequences[:, :-1], sequences[:, -1]
                y = keras.utils.to_categorical(y, num_classes=total_words)
                
                print("\n============================================")
                print(f"Total unique sequences: ({total_sequences+1})")
                print(f"Total unique words: ({total_words})")
                print(f"Dimensions of x: ({x.shape})")
                print(f"Dimensions of y: ({y.shape})")
                print("============================================\n")
                
                model = keras.models.Sequential()
                model.add(keras.layers.Embedding(total_words, 100, input_length=max_sequence_length - 1))
                model.add(keras.layers.LSTM(100))
                model.add(keras.layers.Dense(total_words, activation='softmax'))

                model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
                
                model_checkpoint_callback = keras.callbacks.ModelCheckpoint(
                    filepath='./ckpt/checkpoint.model.keras',
                    monitor='val_accuracy',
                    mode='auto',
                    save_freq='epoch'
                )
                
                if log == True:
                     
                    log_dir = "./logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                    tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)   
                     
                    model.fit(x=x, y=y, validation_data=[x, y], epochs=1, callbacks=[tensorboard_callback])
                else:
                    model.fit(x=x, y=y, epochs=100, callbacks=[model_checkpoint_callback])
                    #model.train_on_batch(x=x, y=y)
                
                model.summary()
                model.save(f"./models/{system}/sequential.keras")

                with open('./tokenizers/tokenizer.gz', 'wb') as hadle:
                    joblib.dump(tokenizer, hadle)
    
    @staticmethod
    def predict_text(seed_text, predict_length, model):
        
        tokenizer = joblib.load('./tokenizers/tokenizer.gz')

        for _ in range(predict_length):
            
            with open('database/max_sequence_length.txt', 'r') as reader:
                max_sequence_length = int(reader.read())
 
            token_list = tokenizer.texts_to_sequences([seed_text])[0]
            token_list = keras.preprocessing.sequence.pad_sequences([token_list], maxlen=max_sequence_length, padding='pre')
             
            predicted_probabilities = model.predict(token_list)[0]
            predicted_index = np.argmax(predicted_probabilities)
            output_word = ""
            
            for word, index in tokenizer.word_index.items():
                 
                if(predicted_index == index):
                    output_word = word
                    break
            
            seed_text += " " + output_word
        
        return seed_text
