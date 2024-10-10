from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='appp'

urlpatterns=[
    path('index/<int:id>',views.index,name='index'),
    path('registration/',views.registration,name='registration'),
    path('login_2/',views.login,name='login_2'),
    path('home/<int:id>',views.home,name='home'),
    path('delete/<int:id>',views.delete,name='delete'),
    path('changepassword/<int:id>',views.changepassword,name='changepassword'),
    path('logout/',views.logout,name='logout'),
    path('about/<int:id>',views.about,name='about'),
    path('service/<int:id>',views.service,name='service'),
    path('contact/<int:id>',views.contact,name='contact'),
    path('team/<int:id>',views.team,name='team'),
    path('appointment/<int:id>',views.appointment1,name='appointment'),
    path('',views.login,name='login'),
    path('doctorindex/<int:id>',views.doctorindex,name='doctorindex'),
    path('view_disease/<int:id>',views.view_disease,name='view_disease'),
    path('view_appointment/<int:id>',views.view_appointment,name='view_appointment'),
    path('schedule/<int:id>',views.schedule,name='schedule'),
    path('predict/<int:id>',views.predict,name='predict'),
    path('complete_appointment/<int:appointment_id>/', views.complete_appointment, name='complete_appointment'),  
    path('prediction_images/<int:id>', views.prediction_images, name='prediction_images'),
    path('chat_dr/<int:id>/', views.chat_dr, name='chat_dr'),
    path('chat_pt/<int:id>/', views.chat_pt, name='chat_pt'),
    path('send-messege/<int:id>/', views.send_message, name='send_messege'),
    path('recieve_message/<int:id>/', views.receive_messages, name='recieve_message'),
    path("<str:chat_view>/<str:username>/", views.chat_view, name="chat_view"),
    path('logout/<int:id>', views.logout_view, name='logout'),
    path('appointment-success/', views.appointment_success, name='appointment_success'),  # F   


]
urlpatterns += static(settings.STATIC_URL)