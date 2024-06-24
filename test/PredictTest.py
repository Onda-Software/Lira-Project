import gc, sys
gc.enable()
sys.path.append('./src/')

from MultilayerPerceptron import MultilayerPerceptron

model = MultilayerPerceptron.load_model('models/Linux/sequential.keras')
question = str(input("Pergunta: "))
predict = MultilayerPerceptron.predict_text(question, int(20), model)

print(f"Resposta: {predict}")
