import requests
import tensorflow as tf
import tensorflow_text as tf_text
import numpy as np

url = "https://github.com/tensorflow/text/blob/master/tensorflow_text/python/ops/test_data/test_wp_en_vocab.txt?raw=true"
request = requests.get(url)
filepath = "vocab.txt"
open(filepath, 'wb').write(request.content)

tokenizer = tf_text.BertTokenizer(filepath, token_out_type=tf.string, lower_case=True)
tokens = tokenizer.tokenize(["What you know you can't explain, but you feel it."])
print(tokens.to_list())

tokenizer = tf_text.UnicodeCharTokenizer()
tokens = tokenizer.tokenize(["What you know you can't explain, but you feel it."])
print(tokens.to_list())

print("=================================================================")

detokenized_text = np.squeeze(np.array(tokenizer.detokenize(tokens)))
print(detokenized_text)

print("=================================================================")

docs = tf.data.Dataset.from_tensor_slices([['Never tell me the odds.'], ["It's a trap!"]])
tokenizer = tf_text.WhitespaceTokenizer()
tokenized_docs = docs.map(lambda x: tokenizer.tokenize(x))
iterator = iter(tokenized_docs)

print(next(iterator).to_list())
print(next(iterator).to_list())
