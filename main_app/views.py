from django.shortcuts import render, redirect
from main_app.apiPerceptron import perceptronAPI, get_result_for_subject
from main_app.models import subject_model, week_model

#Функция, производящая расчет прогнозируемой оценки при помощи обученного парцептрона
def neuralCalc(attendance, hours_studied, sleep_hours, 
    physical_activity):
    PredictedRating =  perceptronAPI(int(hours_studied), int(attendance), int(sleep_hours), int(physical_activity))
    return PredictedRating


# Главная страница
def ratePrediction(request):
    attendance = request.GET.get('attendance','')
    print(attendance)
    hours_studied = request.GET.get('hours_studied','')
    print(hours_studied)
    sleep_hours = request.GET.get('sleep_hours','')
    print(sleep_hours)
    physical_activity = request.GET.get('physical_activity','')
    print(physical_activity)
    if attendance != "" and hours_studied != "" and sleep_hours != "" and physical_activity != "":
        
        PredictedRating = neuralCalc(int(attendance) / 100, hours_studied, sleep_hours, 
        physical_activity)
    else:
        PredictedRating = ""
    data = {'data':{'PredictedRating':PredictedRating, 'attendance':attendance, 'hours_studied':hours_studied, 'sleep_hours':sleep_hours, 
    'physical_activity':physical_activity}}
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
    if attendance != "" and hours_studied != "" and sleep_hours != "" and physical_activity != "":
        
        PredictedRating = neuralCalc(attendance, hours_studied, sleep_hours, physical_activity)
    else:
        PredictedRating = ""
    data = {'data':{'PredictedRating':PredictedRating, 'attendance':attendance, 'hours_studied':hours_studied, 'sleep_hours':sleep_hours, 
    'physical_activity':physical_activity}}
    return render(request, 'user_page.html', data)

    # get_sugjects by user_id из таблицы Subjects 
    # TODO
    
# страница предметов
def get_subjects(request, id: int):
    subjects = subject_model.objects.filter(user_id=id)
    subjects_results = []
    for subject in subjects:
        weeks_data = week_model.objects.filter(subject=subject).all()
        count_weeks = len(weeks_data)
        # если недель нет, то нет результата
        if count_weeks == 0:
            subjects_results.append({'subject': subject, 'result': 0})
            continue
        sleep_data = [(x.week_num, x.avg_sleep) for x in weeks_data]
        physical_activity_data = [(x.week_num, x.avg_phys_activity) for x in weeks_data]
        lessons_data = [(x.week_num, x.lessons_visited) for x in weeks_data]
        time_data = [(x.week_num, x.time_spent) for x in weeks_data]
        count_weeks_of_subject = subject.count_weeks
        count_lessons_of_subject = subject.count_lessons

        result = get_result_for_subject(sleep_data, physical_activity_data, lessons_data, time_data, count_weeks_of_subject, count_lessons_of_subject)
        print("111" + str(result))
        subjects_results.append({'subject': subject, 'result': result})
    
    return render(request, 'user_page.html', {
        'subjects': subjects,
        'subjects_results': subjects_results}
        )
    
    # страница недель
def get_weeks(request, subject_id: int):
    weeks = week_model.objects.filter(subject_id=subject_id)
    return render(request, 'weeks_page.html', {'weeks': weeks})
    
    # создать предмет
def post_subject(request, user_id: int, subject_name: str):
    subject_model.objects.create(user_id=user_id, subject_name=subject_name, num_weeks=0, num_lessons=0)
    return render(request, 'subjects')
    
    # update_subject в таблице Subjects + редирект
def update_subject(subject_id: int, subject_name: str):
    subject = subject_model.objects.get(id=subject_id)
    subject.subject_name = subject_name
    subject.save()
    return redirect('user_page.html')
    
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

    
    

    






                  