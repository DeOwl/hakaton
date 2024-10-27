from django.shortcuts import render
from main_app.apiPerceptron import perceptronAPI
from main_app.models import subject_model, week_model

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


def user_ratePrediction(request):
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
    return render(request, 'user_page.html', data)

    # get_sugjects by user_id из таблицы Subjects 
    # TODO
def get_subjects(request, user_id: int):
    subjects = subject_model.objects.filter(user_id=user_id)
    subjects_results = []
    for subject in subjects:
        weeks_data = week_model.objects.filter(subject=subject.id).all()
        sleep_data = [(x.week_num, x.avg_sleep) for x in weeks_data]
        physical_activity_data = [(x.week_num, x.avg_phys_activity) for x in weeks_data]
        lessons_data = [(x.week_num, x.lessons_visited) for x in weeks_data]
        time_data = [(x.week_num, x.time_spent) for x in weeks_data]
        count_weeks_of_subject = subject.count_weeks
        count_lessons_of_subject = subject.count_lessons

        result = funct(sleep_data, physical_activity_data, lessons_data, time_data, count_weeks_of_subject, count_lessons_of_subject)
        subjects_results.append({'subject': subject, 'result': result})
    return render(request, 'user_page.html', {'subjects': subjects})
    
    # get_weeks by subject_id из таблицы Weeks
def get_weeks(subject_id: int):
    weeks = week_model.objects.filter(subject_id=subject_id)
    return weeks
    
    # post_subject в таблицу Subjects + редирект
def post_subject(user_id: int, subject_name: str):
    subject_model.objects.create(user_id=user_id, subject_name=subject_name, num_weeks=0, num_lessons=0)
    return redirect('subjects')
    
    # update_subject в таблице Subjects + редирект
def update_subject(subject_id: int, subject_name: str):
    subject = subject_model.objects.get(id=subject_id)
    subject.subject_name = subject_name
    subject.save()
    return redirect('subjects')
    
# delete_subject в таблице Subjects
def delete_subject(subject_id: int):
    week_model.objects.filter(subject_id=subject_id).delete()
    subject_model.objects.get(id=subject_id).delete()
        

# post_week в таблицу Weeks + редирект
def post_week(subject_id: int, 
              week_name: str,
              week_number: int,
              avg_sleep_hours: int,
              avg_physical_activity: int, 
              lessons_visited: int,
              time_spent: int):
    week_model.objects.create(subject_id=subject_id, week_name=week_name, 
                    week_number=week_number, avg_sleep_hours=avg_sleep_hours, 
                    avg_physical_activity=avg_physical_activity, lessons_visited=lessons_visited, 
                    time_spent=time_spent)
    return redirect('weeks')
    
    # update_week в таблице Weeks + редирект
def update_week(week_id: int, week_name: str, week_number: int, avg_sleep_hours: int, avg_physical_activity: int, lessons_visited: int, time_spent: int):
    week = week_model.objects.get(id=week_id)
    week.week_name = week_name
    week.week_number = week_number
    week.avg_sleep_hours = avg_sleep_hours
    week.avg_physical_activity = avg_physical_activity
    week.lessons_visited = lessons_visited
    week.time_spent = time_spent
    week.save()
    return redirect('weeks')
    
    # delete_week в таблице Weeks
def delete_week(week_id: int):
    week_model.objects.get(id=week_id).delete()

    
    

    






                  