import gc, platform, sys, unittest

gc.enable()
sys.path.append('./src/')
from MultilayerPerceptron import MultilayerPerceptron

class MultilayerPerceptron(unittest.TestCase):

    def test_load_model(self):
        self.assertEqual('', MultilayerPerceptron.load_model(f'./models/{os_type}/sequential.keras'))

    def test_build(self):
        self.assertEqual(None, MultilayerPerceptron.build_model)

    def test_predict_test(self):
        seed_text = "HTML"
        size_predict = 5
        model = MultilayerPerceptron.load_model(f'./models/{os_type}/sequential.keras')
        predict = MultilayerPerceptron.predict_text(seed_text, int(size_predict), model)
        self.assertEqual('', predict)

if __name__ == "__main__":
    unittest.main()