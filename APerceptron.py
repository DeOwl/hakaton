
import numpy

def sigmoid(x):
    return 1/(1+numpy.exp(-x))
training_inputs = numpy.array([[0,0,1],[1,1,1],[0,1,1]])
training_outputs = numpy.array([[0,1,1,0]]).T
numpy.random.seed(1)
synaptic_weights = 2 * numpy.random.random((3,1)) - 1

for i in range(20000):
    input_layer = training_inputs
    outputs = sigmoid(numpy.dot(input_layer, synaptic_weights))

    err = training_outputs - outputs
    adjustments = numpy.dot(input_layer.T, err*(outputs*(1-outputs)))
    synaptic_weights += adjustments
new_inputs = numpy.array([[1,0,0]])
outputs = sigmoid(numpy.dot(new_inputs, synaptic_weights))
print("Новая ситуация")
print(outputs)