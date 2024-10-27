from django.shortcuts import render
from main_app.apiPerceptron import perceptronAPI

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


    # get_sugjects by user_id из таблицы Subjects 
    def get_subjects(user_id: int):
        subjects = Subjects.objects.filter(user_id=user_id)
        return subjects
    
    # get_weeks by subject_id из таблицы Weeks
    def get_weeks(subject_id: int):
        weeks = Weeks.objects.filter(subject_id=subject_id)
        return weeks
    
    # post_subject в таблицу Subjects + редирект
    def post_subject(user_id: int, subject_name: str):
        Subjects.objects.create(user_id=user_id, subject_name=subject_name, num_weeks=0, num_lessons=0)
        return redirect('subjects')
    
    # update_subject в таблице Subjects + редирект
    def update_subject(subject_id: int, subject_name: str):
        subject = Subjects.objects.get(id=subject_id)
        subject.subject_name = subject_name
        subject.save()
        return redirect('subjects')
    
    # delete_subject в таблице Subjects
    def delete_subject(subject_id: int):
        Weeks.objects.filter(subject_id=subject_id).delete()
        Subjects.objects.get(id=subject_id).delete()
        

    # post_week в таблицу Weeks + редирект
    def post_week(subject_id: int, 
                  week_name: str,
                  week_number: int,
                  avg_sleep_hours: int,
                  avg_physical_activity: int, 
                  lessons_visited: int,
                  time_spent: int):
        Weeks.objects.create(subject_id=subject_id, week_name=week_name, 
                             week_number=week_number, avg_sleep_hours=avg_sleep_hours, 
                             avg_physical_activity=avg_physical_activity, lessons_visited=lessons_visited, 
                             time_spent=time_spent)
        return redirect('weeks')
    
    # update_week в таблице Weeks + редирект
    def update_week(week_id: int, week_name: str, week_number: int, avg_sleep_hours: int, avg_physical_activity: int, lessons_visited: int, time_spent: int):
        week = Weeks.objects.get(id=week_id)
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
        Weeks.objects.get(id=week_id).delete()

    
    

    



                  