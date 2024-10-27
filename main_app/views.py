
from django.shortcuts import render
from main_app.apiPerceptron import perceptronAPI
from django.shortcuts import render
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import logout


from django.contrib.auth import authenticate
from rest_framework.decorators import authentication_classes, permission_classes
from main_app.permissions import IsAuth, IsAuthManager
from rest_framework.permissions import  AllowAny

from .redis import session_storage
import uuid
from .auth import Auth_by_Session, AuthIfPos

def sub_view(request):
    subjects = subject_model.objects.filter(user_id=id)
    names = []
    for sub in subjects:
        names.append(sub.subject_name)
        
    context = {
        'app_title': 'Анализ успеваемости',
        'app_title': 'Авторизация', 
        'app_title': 'Мои предметы',
        'app_title': names 
    }
    return render(request, context)

from main_app.apiPerceptron import perceptronAPI, get_result_for_subject
from django.shortcuts import render, redirect
from main_app.apiPerceptron import perceptronAPI, get_result_for_subject, get_graph_from_data, get_linear_nums
from main_app.models import subject_model, week_model

#Функция, производящая расчет прогнозируемой оценки при помощи обученного парцептрона
def neuralCalc(attendance, hours_studied, sleep_hours, 
    physical_activity):
    PredictedRating =  perceptronAPI(int(hours_studied), int(attendance), int(sleep_hours), int(physical_activity))
    return PredictedRating


# Главная страница
def ratePrediction(request):
    session_id = request.COOKIES.get('session_id')
    if session_id is None:
        user = None
    try:
        user_name = session_storage.get(session_id).decode('utf-8')
        user = User.objects.get(username=user_name)
    except:
        user = None
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
    'physical_activity':physical_activity}, "user":user}
    return render(request, 'neural_predict_page.html', data)


def reg_ratePrediction(request):
    return render(request, 'reg.html', {'user' : None})
def auth_ratePrediction(request):
    user = None
    return render(request, 'auth.html', {'user' : user})
def user_ratePrediction(request):
    return render(request, 'user_page.html')
def sub_ratePrediction(request):
    return render(request, 'sub.html')    


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
    
# страница юзера
def get_subjects(request, id: int):
    session_id = request.COOKIES.get('session_id')
    if session_id is None:
        return redirect("mainForm")
    try:
        user_name = session_storage.get(session_id).decode('utf-8')
        user = User.objects.get(username=user_name)
    except:
        return redirect("mainForm")
    

    if (id != user.id):
        return redirect("mainForm")
    
    
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

        result = get_result_for_subject(sleep_data, physical_activity_data,  time_data, lessons_data, count_weeks_of_subject, count_lessons_of_subject)
        subjects_results.append({'subject': subject, 'result': result})
    return render(request, 'user_page.html', {
        'subjects_results': subjects_results, "user": user}
        )
    
    # страница предметов
def get_weeks(request, subject_id: int):
    session_id = request.COOKIES.get('session_id')
    if session_id is None:
        return redirect("mainForm")
    try:
        user_name = session_storage.get(session_id).decode('utf-8')
        user = User.objects.get(username=user_name)
    except:
        return redirect("mainForm")
    
    weeks_data = week_model.objects.filter(subject_id=subject_id).order_by("week_num")
    count_weeks = len(weeks_data)
    # если недель нет, то нет результата
    if count_weeks != 0:
        sleep_data = [(x.week_num, x.avg_sleep) for x in weeks_data]
        physical_activity_data = [(x.week_num, x.avg_phys_activity) for x in weeks_data]
        lessons_data = [(x.week_num, x.lessons_visited) for x in weeks_data]
        time_data = [(x.week_num, x.time_spent) for x in weeks_data]
        count_weeks_of_subject = subject_model.objects.get(subject_id=subject_id).count_weeks
        count_lessons_of_subject = subject_model.objects.get(subject_id=subject_id).count_lessons
        graph_sl = get_graph_from_data(sleep_data, get_linear_nums(sleep_data), count_weeks_of_subject, "сон", 12, 0)
        graph_les = get_graph_from_data(lessons_data, get_linear_nums(lessons_data), count_weeks_of_subject, "посещаемость", count_lessons_of_subject, 0)
        graph_time = get_graph_from_data(time_data, get_linear_nums(time_data), count_weeks_of_subject, "часы занятий", 50, 0)
        graph_phys = get_graph_from_data(physical_activity_data, get_linear_nums(physical_activity_data), count_weeks_of_subject, "физическая активность", 14, 0)
        result = get_result_for_subject(sleep_data, physical_activity_data, time_data, lessons_data, count_weeks_of_subject, count_lessons_of_subject)
    else:
        graph_sl = None
        graph_les = None
        graph_time = None
        graph_phys = None
        count_lessons_of_subject = 0
        result = 0
    subject = subject_model.objects.get(subject_id = subject_id)
    return render(request, 'subject_page.html', {'subject_id' : subject_id,
                                                 'app_title' : subject.subject_name + ": " + str(result),
                                                 'user_id' : user.id, 
                                                 "user" : user , 
                                                 'weeks': weeks_data,
                                                 'graph_sl': graph_sl,
                                                 'graph_les': graph_les,
                                                 'graph_time':graph_time, 
                                                 'graph_phys':graph_phys,
                                                 'result': result,
                                                 'lesson_count' : count_lessons_of_subject})
    
    # создать предмет с редиректом на юзера
def post_subject(request, user_id):
    user = User.objects.get(id = user_id)
    subject_name = request.POST.get("title")
    num_weeks = request.POST.get("count_weeks")
    num_lessons = request.POST.get("count_lessons")
    subject_model.objects.create(user_id=user, subject_name=subject_name, count_weeks=num_weeks, count_lessons=num_lessons)
    return redirect("uForm", id = user_id)
    
    # обновить предмет с редиректом на юзера
def update_subject(subject_id: int, subject_name: str):
    subject = subject_model.objects.get(id=subject_id)
    subject.subject_name = subject_name
    subject.save()
    return redirect('user_page.html')
    
# удалить предмет с редиректом на юзера
def delete_subject(subject_id: int):
    week_model.objects.filter(subject_id=subject_id).delete()
    subject_model.objects.get(id=subject_id).delete()
    return redirect('user_page.html')
        

# создать неделю с редиректом на предмет
def post_week(request, subject_id: int):
    week_number =  request.POST.get("week_num")
    avg_sleep_hours =  request.POST.get("sleep_timeme")
    avg_physical_activity =  request.POST.get("avg_phys_activity")
    lessons_visited =  request.POST.get("lessons_visited")
    time_spent =  request.POST.get("time_spent")
    subject = subject_model.objects.get(subject_id=subject_id)
    week_model.objects.create(subject=subject, 
                              week_num=week_number, 
                              avg_sleep=avg_sleep_hours,
                              avg_phys_activity = avg_physical_activity,
                              lessons_visited = lessons_visited,
                              time_spent = time_spent)
    return redirect('weeks', subject_id=subject_id)
    
    # обновить неделю с редиректом на предмет
def update_week(week_id: int, week_name: str, week_number: int, avg_sleep_hours: int, avg_physical_activity: int, lessons_visited: int, time_spent: int):
    week = week_model.objects.get(id=week_id)
    week.week_name = week_name
    week.week_number = week_number
    week.avg_sleep_hours = avg_sleep_hours
    week.avg_physical_activity = avg_physical_activity
    week.lessons_visited = lessons_visited
    week.time_spent = time_spent
    week.save()
    return redirect('subject_page.html')
    
    # удалить неделю с редиректом на предмет
def delete_week(week_id: int):
    week_model.objects.get(id=week_id).delete()
    week_model.objects.get(id=week_id).delete()
    return redirect('subject_page.html')



@permission_classes([AllowAny])
def Create_User(request):
    """
    Функция регистрации новых пользователей
    Если пользователя c указанным в request email ещё нет, в БД будет добавлен новый пользователь.
    """
    if User.objects.filter(email=request.data['email']).exists():
        return redirect(".")
    email = request.POST.get("email")
    password = request.POST.get("password")
    name = request.POST.get("name")
    user = User.objects.create_user(name, email, password)
    return redirect(".")


@permission_classes([AllowAny])
def Login_User(request):
    email = request.POST.get("email") # допустим передали username и password
    password = request.POST.get("password")
    print(email, password)
    user = authenticate(username=email, password=password)
    if user is not None:
        session_id = str(uuid.uuid4())
        session_storage.set(session_id, email)
        response = redirect('uForm', id=user.id)
        response.set_cookie("session_id", session_id, samesite="lax")
        return response
    return redirect('aForm')


@permission_classes([IsAuth])
def logout_user(request):

    """
    деавторизация
    """
    session_id = request.COOKIES["session_id"]
    print(session_id)
    if session_storage.exists(session_id):
        session_storage.delete(session_id)
        response = redirect('mainForm')
        response.delete_cookie("session_id")
        return response
    return redirect("mainForm")