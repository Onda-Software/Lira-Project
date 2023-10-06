# import tensorflow as tf
# import tensorflow_probability as tfp

# # Pretend to load synthetic data set.
# features = tfp.distributions.Normal(loc=0., scale=1.).sample(int(100e3))
# labels = tfp.distributions.Bernoulli(logits=1.618 * features).sample()

# # Specify model.
# model = tfp.glm.Bernoulli()

# # Fit model given data.
# coeffs, linear_response, is_converged, num_iter = tfp.glm.fit(
#     model_matrix=features[:, tf.newaxis],
#     response=tf.cast(labels, dtype=tf.float32),
#     model=model)
# # ==> coeffs is approximately [1.618] (We're golden!)

# print(coeffs)




# import tensorflow_hub as hub

# model = hub.KerasLayer("https://tfhub.dev/google/nnlm-en-dim128/2")
# embeddings = model(["The rain in Spain.", "falls", "mainly", "In the plain!"])

# print(embeddings.shape)  #(4,128)




# import os
# import shutil

# import tensorflow as tf
# import tensorflow_hub as hub
# import tensorflow_text as text
# import matplotlib.pyplot as plt

# tf.get_logger().setLevel('ERROR')
