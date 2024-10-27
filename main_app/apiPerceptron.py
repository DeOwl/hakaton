import numpy as np
import numpy as np
from django.contrib.staticfiles import finders
import matplotlib.pyplot as plt
import json
from io import StringIO

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def num_to_range(num, inMin, inMax, outMin, outMax):
    return outMin + (float(num - inMin) / float(inMax - inMin) * (outMax
                  - outMin))

#расчет резултата по числам
def perceptronAPI(hours_studied : float, 
                  attendance : float, 
                  sleep_hours : float, 
                  physical_activity : float) -> float:
    data = finders.find("model.json")
    with open(data, 'r') as file:
        data = json.load(file)
    weights = np.array(data["weights"]).T
    print(hours_studied, attendance, sleep_hours, physical_activity)
    # преобразование к нужному формату
    hours_studied = min(50.0, max(hours_studied, 0.0))
    hours_studied = hours_studied / 44
    attendance = min(1.0, max(attendance, 0.0))
    sleep_hours = min(11.0, max(sleep_hours, 4.0))
    sleep_hours = abs(7 - sleep_hours) / 3
    physical_activity = min(14, max(physical_activity, 0))
    physical_activity = physical_activity / 6
    print(hours_studied, attendance, sleep_hours, physical_activity)
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


#функция предсказания результатов успеваемости
def get_result_for_subject(data_sleep: list[tuple[int, float]], 
                           data_pha: list[tuple[int, float]],
                           data_time: list[tuple[int, float]] , 
                           data_lesson: list[tuple[int, int]], 
                           week_num:int, 
                           count_lesson: int) -> int:
    sleep = get_prediction_at_week(get_linear_nums(data_sleep), week_num / 2)
    phys_act = get_prediction_at_week(get_linear_nums(data_pha), week_num / 2)
    print(data_lesson)  
    lesson  = get_prediction_at_week(get_linear_nums(data_lesson), week_num)
    print(lesson)
    time = get_prediction_at_week(get_linear_nums(data_time), week_num / 2)
    return(perceptronAPI(time, lesson / count_lesson, sleep, phys_act))
    
    

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



def get_graph_from_data(data : list[tuple[int, float]], b : tuple[float, float], number_of_weeks, name, max_d, min_d):
    x = [x[0] for x in data]
    x = np.array(x)
    y = np.array([x[1] for x in data])
    
    
    fig = plt.figure()
    plt.scatter(x, y, color = "m", marker= 'o', s= 30)
    x = [x[0] for x in data]
    x.append(number_of_weeks)
    x = np.array(x)
    y_pred = b[0] + b[1] * x
    plt.plot(x, y_pred, color="g")
    
    plt.xlabel('Недели')
    plt.gca().set_xlim([0, number_of_weeks + 1])
    
    y_pred_last = b[0] + b[1] * number_of_weeks
    plt.gca().set_ylim([0, max(y.max(), y_pred_last) + 1])
    plt.ylabel(name)
    
    imgdata = StringIO()
    fig.savefig(imgdata, format="svg")
    imgdata.seek(0)
    
    data = imgdata.getvalue()
    return data


# ищем наиболее влияющий на результат параметр
# для этого изменяем существующие на определенный процент и смотрим на результат в sigmoid
def apiRecomend(hours_studied : float, 
                               attendance : float, 
                               sleep_hours : float, 
                               physical_activity : float) -> list[tuple[float, str]]:
    original_hours_studied = hours_studied
    original_attendance = attendance
    original_sleep_hours = sleep_hours
    original_physical_activity = physical_activity
    # вывод
    original_num = perceptronAPI(hours_studied, attendance, sleep_hours, physical_activity)
    # влияние сна на результат
    sleep_coeff = 0
    sleep_num = original_num
    for i in range(0, 8):
        new_coeff = 0.7 + i * 0.1
        n_sleep_hours = original_hours_studied * new_coeff
        new_sleep_num = perceptronAPI(hours_studied, attendance, n_sleep_hours, physical_activity)
        if (new_sleep_num > sleep_num):
            sleep_num = new_sleep_num
            sleep_coeff = new_coeff
    # влияние физической активности на результат
    physical_activity_coeff = 0
    physical_activity_num = original_num
    for i in range(0, 8):
        new_coeff = 0.7 + i * 0.1
        n_physical_activity = original_hours_studied * new_coeff
        new_pa = perceptronAPI(hours_studied, attendance, sleep_hours, n_physical_activity)
        if (new_pa > physical_activity_num):
            physical_activity_num  = new_pa
            physical_activity_coeff = new_coeff
    # влияние посещаемости на результат
    att_coeff = 0
    att_num = original_num
    for i in range(0, 8):
        new_coeff = 0.7 + i * 0.1
        n_att = original_attendance * new_coeff
        new_att = perceptronAPI(hours_studied, n_att, sleep_hours, physical_activity)
        if (new_att > att_num):
            att_num  = new_att
            att_coeff = new_coeff
    attendance = original_attendance * 1.1
    attendance_num = perceptronAPI(hours_studied, attendance, sleep_hours, physical_activity)
    # влияние времени на результат
    hours_studied = original_hours_studied * 1.1 
    hours_studied_num = perceptronAPI(hours_studied, attendance, sleep_hours, physical_activity)
    # наиболее влияющий параметр
    num = max(original_num, sleep_num, physical_activity_num, attendance_num, hours_studied_num)
    print("nums", original_attendance, original_hours_studied, original_sleep_hours, original_physical_activity)
    # сортировка по убыванию nums
    list_nums = [[sleep_hours * sleep_coeff, "sleep_hours"], 
                 [physical_activity * physical_activity_coeff, "physical_activity"], 
                 [attendance * att_coeff, "attendance"], 
                 [hours_studied_num, "hours_studied"]]
    list_nums.sort(reverse=True)
    print("list_nums", list_nums)
    return list_nums