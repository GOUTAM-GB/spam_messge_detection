from django.db import models

# Create your models here.
class UserRegistrationModel(models.Model):
    name = models.CharField(max_length=100)
    loginid = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    mobile = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=100)
    locality = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    role = models.CharField(max_length=50, default='User')

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = 'UserRegistrations'

class UserActivityLog(models.Model):
    user_loginid = models.CharField(max_length=100)
    user_role = models.CharField(max_length=50)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'UserActivityLog'

class PredictionReport(models.Model):
    user_loginid = models.CharField(max_length=100)
    algorithm_name = models.CharField(max_length=100)
    input_text = models.CharField(max_length=5000)
    input_type = models.CharField(max_length=50, default='text')
    prediction_result = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'PredictionReport'
