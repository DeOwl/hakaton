import numpy as np
from numpy import genfromtxt

my_data = genfromtxt('dataset1.csv', delimiter=';', skip_header=True, 
                     converters={0: lambda x: int(x) / (7 * 24), # часы учебы
                                 1: lambda x: int(x) / 100, # посещаемость
                                 2: lambda x: abs(8 - int(x)) / 24, # часы сна
                                 3: lambda x: int(x) / ( 7 * 24), # часы физической активности
                                 4: lambda x: 0.0 if x.encode('utf-8') == 'Near' else 0.5 if x.encode('utf-8') == 'Moderate' else 1.0, # дистанция от дома
                                 5: lambda x: int(x) / 100 # оценка
                                 })

_data = genfromtxt('dataset1.csv', delimiter=';', skip_header=True, 
                     converters={0: lambda x: float(x) / (44), # часы учебы
                                 1: lambda x: float(x) / 100, # посещаемость
                                 2: lambda x: abs(7 - float(x)) / 3, # часы сна
                                 3: lambda x: float(x) / (6), # часы физической активности
                                 4: lambda x: 0.0 if x.encode('utf-8') == 'Near' else 0.5 if x.encode('utf-8') == 'Moderate' else 1.0, # дистанция от дома
                                 5: lambda x: float(x) / 100 # оценка
                                 })

print(my_data)

# Min-Max нормализация - в диапазоне от 0 до 1
def min_max_normalize(data):
    return (data - np.min(data, axis=0)) / (np.max(data, axis=0) - np.min(data, axis=0))




training_inputs = _data[:, 0:5]  # Включаем первые пять столбцов

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

training_outputs = _data[:, 5:]

np.random.seed(1)

synaptic_weights = 2 * np.random.random((5, 1)) - 1  

for i in range(5000):
    input_layer = training_inputs
    outputs = sigmoid(np.dot(input_layer, synaptic_weights))
    err = training_outputs - outputs
    adjustment = np.dot(input_layer.T, err * (outputs * (1 - outputs)))
    adjustment = adjustment / (input_layer.size)
    synaptic_weights += adjustment
    
new_outputs = sigmoid(np.dot(training_inputs, synaptic_weights))
print(synaptic_weights)
print(training_outputs[0 : 10])
print(new_outputs[0 : 10])
print(sigmoid(np.dot(np.array([
    [0.23,
     0.84,
     (7 / 10),
     (3 / 6),
     (0 / 3)
     ]]), synaptic_weights)))
