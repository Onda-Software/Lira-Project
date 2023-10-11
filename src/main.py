import tensorflow as tf
from tensorflow import keras
import tensorflow_datasets as tfds
from sklearn.feature_extraction.text import CountVectorizer

physical_devices = tf.config.list_physical_devices('GPU')

if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

dataset = tfds.load('ag_news_subset')

ds_train = dataset['train']
ds_test = dataset['test']

print(f"Length of train dataset = {len(ds_train)}")
print(f"Length of test dataset = {len(ds_test)}")

classes = ['World', 'Sports', 'Bussines', 'Sci/Tech']

# for i, x in zip(range(5), ds_train):
#    print(f"\n{x['label']} ({classes[x['label']]}) -> {x['title']} {x['description']}")

vocab_size = 50000
vectorizer = keras.layers.experimental.preprocessing.TextVectorization(max_tokens=vocab_size)
vectorizer.adapt(ds_train.take(500).map(lambda x: x['title'] + ' ' + x['description']))

vocab = vectorizer.get_vocabulary()
vocab_size = len(vocab)
print(vocab[:10])
print(f"\nLength of vocabulary: {vocab_size}\n")

print(vectorizer('I love to play with my words'))

sc_vetorizer = CountVectorizer()
corpus = ['I like hot dogs.', 'The dog ran fast.', 'Its hot outside.']
sc_vetorizer.fit_transform(corpus)
print(sc_vetorizer.transform(['My dog likes hot dogs on a hot day.']).toarray())

def to_bow(text):
    return tf.reduce_sum(tf.one_hot(vectorizer(text), vocab_size), axis=0)

print(to_bow('My dog likes hot dogs on a hot day.').numpy())

batch_size = 128

ds_train_bow = ds_train.map(lambda x: (to_bow(x['title'] + x['description']), x['label'])).batch(batch_size)
ds_test_bow = ds_test.map(lambda x: (to_bow(x['title']+x['description']),x['label'])).batch(batch_size)

model = keras.models.Sequential([
    keras.layers.Dense(4,activation='softmax',input_shape=(vocab_size,))
])

model.compile(loss='sparse_categorical_crossentropy',optimizer='adam',metrics=['acc'])
model.fit(ds_train_bow,validation_data=ds_test_bow)

