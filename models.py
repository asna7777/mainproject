from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q


# Create your models here.
class Register(models.Model):
    Name=models.CharField(max_length=10)
    Password=models.CharField(max_length=10)
    Email=models.EmailField(max_length=20)
    place=models.CharField(max_length=20)
    Age=models.IntegerField()
    usertype=models.CharField(max_length=20)

class Appointment(models.Model):
     
    Name=models.CharField(max_length=10)
    Email=models.EmailField(max_length=20)
    place=models.CharField(max_length=20)
    Age=models.IntegerField()
    Phone=models.IntegerField(10)
    Date=models.DateField()
    time = models.DateTimeField(auto_now_add=True)
    dr_id=models.IntegerField()
    predict = models.ImageField(upload_to='predictions/', blank=True, null=True)    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Viewed', 'Viewed'),
        ('Completed','Completed')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    



class Chat(models.Model):
    sender = models.CharField(max_length=50)
    receiver = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return f'{self.sender} to {self.receiver} at {self.timestamp}'
    


  
class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # You can add more fields if needed

    def __str__(self):
        return self.user.username



from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
User = get_user_model()

# Create your models here.

class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)