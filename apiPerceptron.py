import numpy as np
from test import sigmoid, synaptic_weights

# с типами данных
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
    home_distance = 0.0 if home_distance == 'Near' else 0.5 if home_distance == 'Moderate' else 1.0
    home_distance = home_distance / 3
    # вывод
    return sigmoid(np.dot(np.array([
        [hours_studied,
         attendance,
         sleep_hours,
         physical_activity,
         home_distance
         ]]), synaptic_weights))

print("!!!!", perceptronAPI(40, 84, 7, 3, 'Near'))
print("@@@", perceptronAPI(23, 84, 7, 3, 'Near'))