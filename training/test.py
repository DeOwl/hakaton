import numpy as np
import time
from numpy import genfromtxt


start_time = time.time()

_data = genfromtxt('dataset1.csv', delimiter=';', skip_header=True, 
                     converters={0: lambda x: float(x) / 24, # часы учебы
                                 1: lambda x: float(x) / 100, # посещаемость
                                 2: lambda x: abs(7 - float(x)) / 24, # часы сна
                                 3: lambda x: abs(3- float(x)) / 24, # часы физической активности
                                 4: lambda x: 0.0 if x.encode('utf-8') == b'Near' else 0.5 if x.encode('utf-8') == b'Moderate' else 1.0, # дистанция от дома
                                 5: lambda x: float(x) / 100 # оценка
                                 })


# Min-Max нормализация - в диапазоне от 0 до 1
def min_max_normalize(data):
    return (data - np.min(data, axis=0)) / (np.max(data, axis=0) - np.min(data, axis=0))




training_inputs = _data[:, 0:4]  # Включаем первые пять столбцов

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

training_outputs = _data[:, 5:]

np.random.seed(1)

synaptic_weights = 2 * np.random.random((4, 1)) - 1  

for i in range(10000):
    input_layer = training_inputs
    outputs = sigmoid(np.dot(input_layer, synaptic_weights))
    err = 2 * (training_outputs - outputs) / (input_layer.size)
    adjustment = np.dot(input_layer.T, err * (outputs * (1 - outputs)))
    synaptic_weights += adjustment
    


    
new_outputs = sigmoid(np.dot(training_inputs, synaptic_weights))


print(synaptic_weights)
print(training_outputs[0 : 10])
print(new_outputs[0 : 10])

print("Среднеквадратическое отклонение:", err.std() ** 0.5)
print("Средняя ошибка:", np.absolute(err).mean())

print("Время работы:", time.time() - start_time, "seconds")

