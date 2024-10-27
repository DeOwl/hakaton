from django.shortcuts import render
from main_app.apiPerceptron import perceptronAPI
from django.shortcuts import render

def sub_view(request):
    context = {
        'app_title': 'Анализ успеваемости',
        'app_title': 'Авторизация', 
        'app_title': 'Мои предметы',
        'app_title': 'Предмет 1' 
    }
    return render(request, 'sub.html', context)


#Функция, производящая расчет прогнозируемой оценки при помощи обученного парцептрона
def neuralCalc(attendance, hours_studied, sleep_hours, 
    physical_activity, home_distance):
    PredictedRating =  perceptronAPI(int(hours_studied), int(attendance), int(sleep_hours), int(physical_activity), home_distance)
    return PredictedRating
# Create your views here.
def ratePrediction(request):
    attendance = request.GET.get('attendance','')
    print(attendance)
    hours_studied = request.GET.get('hours_studied','')
    print(hours_studied)
    sleep_hours = request.GET.get('sleep_hours','')
    print(sleep_hours)
    physical_activity = request.GET.get('physical_activity','')
    print(physical_activity)
    home_distance = request.GET.get('home_distance','')
    print(home_distance)
    if attendance != "" and hours_studied != "" and sleep_hours != "" and physical_activity != "" and home_distance != "":
        
        PredictedRating = neuralCalc(attendance, hours_studied, sleep_hours, 
        physical_activity, home_distance)
    else:
        PredictedRating = ""
    data = {'data':{'PredictedRating':PredictedRating, 'attendance':attendance, 'hours_studied':hours_studied, 'sleep_hours':sleep_hours, 
    'physical_activity':physical_activity, 'home_distance':home_distance}}
    return render(request, 'neural_predict_page.html', data)

def reg_ratePrediction(request):
    return render(request, 'reg.html')
def auth_ratePrediction(request):
    return render(request, 'auth.html')
def user_ratePrediction(request):
    return render(request, 'user_page.html')
def sub_ratePrediction(request):
    return render(request, 'sub.html')    