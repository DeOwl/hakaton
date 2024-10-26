import numpy as np
import numpy as np
from numpy import genfromtxt

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

synaptic_weights = np.array([[ 0.32622339],
 [ 0.78667649],
 [-0.02907133],
 [-0.05508095],
 [-0.05724099],])


def num_to_range(num, inMin, inMax, outMin, outMax):
    print(num)
    return outMin + (float(num - inMin) / float(inMax - inMin) * (outMax
                  - outMin))


def perceptronAPI(hours_studied : int, 
                  attendance : int, 
                  sleep_hours : int, 
                  physical_activity : str, 
                  home_distance : int) -> float:
    # преобразование к нужному формату
    hours_studied = hours_studied / 44
    attendance = attendance / 100
    sleep_hours = abs(7 - sleep_hours) / 3
    physical_activity = physical_activity / 6
    home_distance = 0.0 if home_distance == 'near' else 0.5 if home_distance == 'moderate' else 1.0
    print(num_to_range(70, 40, 80, 20, 100))
    # вывод
    num = sigmoid(np.dot(np.array([
        [hours_studied,
         attendance,
         sleep_hours,
         physical_activity,
         home_distance
         ]]), synaptic_weights))
    num *= 100
    num = int(num)
    return num_to_range(num, 40, 80, 20, 100)
