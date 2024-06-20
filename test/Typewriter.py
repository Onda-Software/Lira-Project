import gc, time
gc.enable()

text = "Teste de maquina de escrever!."
stdout = ""

for i in range(len(text)):
    print(stdout, end='\r')
    stdout += text[i]
    time.sleep(0.05)
