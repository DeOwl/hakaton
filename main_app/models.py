from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class subject_model(models.Model):
    subject_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    subject_name = models.CharField(max_length=200)
    count_weeks = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    count_lessons = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        managed = True
        db_table = 'subjects'

class week_model(models.Model):
    week_id = models.AutoField(primary_key=True)
    subject = models.ForeignKey('subject_model', on_delete=models.CASCADE)
    week_num = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    avg_sleep = models.FloatField(default=7, validators=[MinValueValidator(0), MaxValueValidator(24)])
    avg_phys_activity = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(20)])
    lessons_visited = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    time_spent = models.FloatField(default=7, validators=[MinValueValidator(0), MaxValueValidator(50)])

    class Meta:
        managed = True
        db_table = 'weeks'
        constraints = [
            models.UniqueConstraint(fields=['week_num', 'subject_id'], name='unique item in plant')
        ]

#class user_model(models.Model):
#    id = models.AutoField(primary_key=True)
#    class Meta:
#        managed = False
 #       db_table = 'auth_user'