import requests
import tensorflow as tf
import tensorflow_text as tf_text

url = "https://github.com/tensorflow/text/blob/master/tensorflow_text/python/ops/test_data/test_wp_en_vocab.txt?raw=true"
r = requests.get(url)
filepath = "vocab.txt"
print(open(filepath, 'wb').write(r.content))

tokenizer = tf_text.BertTokenizer(filepath, token_out_type=tf.string, lower_case=True)
tokens = tokenizer.tokenize(["What you know you can't explain, but you feel it."])
print(tokens.to_list())

tokenizer = tf_text.UnicodeCharTokenizer()
tokens = tokenizer.tokenize(["What you know you can't explain, but you feel it."])
print(tokens.to_list())
strings = tokenizer.detokenize(tokens)
print(strings.numpy())

docs = tf.data.Dataset.from_tensor_slices([['Never tell me the odds.'], ["It's a trap!"]])
tokenizer = tf_text.WhitespaceTokenizer()
tokenized_docs = docs.map(lambda x: tokenizer.tokenize(x))
iterator = iter(tokenized_docs)
print(next(iterator).to_list())
print(next(iterator).to_list())

