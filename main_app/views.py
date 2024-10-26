from django.shortcuts import render

#Функция, производящая расчет прогнозируемой оценки при помощи обученного парцептрона
def neuralCalc(attendance, hours_studied, sleep_hours, 
    physical_activity, home_distance):
    PredictedRating = 98
    return PredictedRating
# Create your views here.
def ratePrediction(request):
    attendance = request.GET.get('attendance','')
    hours_studied = request.GET.get('hours_studied','')
    sleep_hours = request.GET.get('sleep_hours','')
    physical_activity = request.GET.get('physical_activity','')
    home_distance = request.GET.get('home_distance','')
    PredictedRating = neuralCalc(attendance, hours_studied, sleep_hours, 
    physical_activity, home_distance)
    data = {'data':{'PredictedRating':PredictedRating, 'attendance':attendance, 'hours_studied':hours_studied, 'sleep_hours':sleep_hours, 
    'physical_activity':physical_activity, 'home_distance':home_distance}}
    return render(request, 'neural_predict_page.html', data)
                  