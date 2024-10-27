import numpy as np
import numpy as np
from django.contrib.staticfiles import finders
import matplotlib.pyplot as plt
import json
from io import StringIO

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def num_to_range(num, inMin, inMax, outMin, outMax):
    print(num)
    return outMin + (float(num - inMin) / float(inMax - inMin) * (outMax
                  - outMin))


def perceptronAPI(hours_studied : int, 
                  attendance : int, 
                  sleep_hours : int, 
                  physical_activity : str, 
                  home_distance : int) -> float:
    data = finders.find("model.json")
    with open(data, 'r') as file:
        data = json.load(file)
    weights = np.array(data["weights"]).T
    # преобразование к нужному формату
    hours_studied = hours_studied / 44
    attendance = attendance / 100
    sleep_hours = abs(7 - sleep_hours) / 3
    physical_activity = physical_activity / 6
    print(num_to_range(70, 40, 80, 20, 100))
    # вывод
    num = sigmoid(np.dot(np.array([
        [hours_studied,
         attendance,
         sleep_hours,
         physical_activity,
         ]]), weights))
    num *= 100
    num = int(num)
    return int(num_to_range(num, 0, 75, 0, 100))



def get_linear_nums(data : list[tuple[int, float]]) -> tuple[float, float]:
    
    n = len(data)
    
    x = np.array([x[0] for x in data])
    y = np.array([x[1] for x in data])
    
    m_x = np.mean(x)
    m_y = np.mean(y)
    
    SS_xy = np.sum(y * x) - n*m_y*m_x
    SS_xx = np.sum(x * x) - n*m_x * m_x
    
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1*m_x
    
    return (b_0, b_1)


def get_prediction_at_week(graph: tuple[float, float], week):
    return graph[0] + graph[1] * week


def get_graph_from_data(data : list[tuple[int, float]], b : tuple[float, float]):
    x = [x[0] for x in data]
    x = np.array(x)
    y = np.array([x[1] for x in data])
    
    
    #fig = plt.figure()
    plt.scatter(x, y, color = "m", marker= 'o', s= 30)
    x = [x[0] for x in data]
    x.append(number_of_weeks)
    x = np.array(x)
    y_pred = b[0] + b[1] * x
    plt.plot(x, y_pred, color="g")
    
    plt.xlabel('Недели')
    plt.gca().set_xlim([0, number_of_weeks + 1])
    plt.gca().set_ylim([0, y.max() * 1.2])
    plt.ylabel(name)
    
    imgdata = StringIO()
    fig.savefig(imgdata, format="svg")
    imgdata.seek(0)
    
    data = imgdata.getvalue()
    return data