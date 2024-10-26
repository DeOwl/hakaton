import numpy as np
from numpy import genfromtxt
my_data = genfromtxt('data.csv', delimiter=';', skip_header=True, 
                     converters={0: lambda x: int(x) / 100,
                                 1: lambda s:  1.0 if s == b"Yes" else 0.0,
                                 2: lambda x: (abs(8 - int(x)) / 24),
                                 3: lambda x: int(x) / 5,
                                 4: lambda x: int(x) / 100
                                 })

training_inputs = my_data[:, 0:4]

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

training_outputs = my_data[:, 4:]

np.random.seed(1)

synaptic_weights = 2 * np.random.random((4, 1)) - 1


for i in range(500):
    input_layer = training_inputs
    outputs = sigmoid(np.dot(input_layer, synaptic_weights))
    err = training_outputs - outputs
    adjustment = np.dot(input_layer.T, err * (outputs * (1 - outputs)))
    adjustment = adjustment / (input_layer.size)
    synaptic_weights += adjustment
    
new_outputs = sigmoid( np.dot(training_inputs, synaptic_weights))
print(synaptic_weights)
print(training_outputs[0 : 10])
print(new_outputs[0 : 10])
print(sigmoid(np.dot(np.array([[0.84,0.0,(4 / 24),(3/5)]]), synaptic_weights)))