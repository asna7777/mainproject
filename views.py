
import datetime
from django.shortcuts import render,redirect
from django.contrib import messages
from.forms import RegisterForm, LoginForm,ChangepasswordForm,PredictionForm
from .models import Register,Appointment
from django.contrib.auth import logout as logouts
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Appointment
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_http_methods

from django.contrib.auth import logout
from django.shortcuts import redirect

from django.conf import settings
from django.core.mail import send_mail






from django.utils.dateparse import parse_date

# Create your views here.

def registration(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['Name']
            age=form.cleaned_data['Age']
            place=form.cleaned_data['place']
            email=form.cleaned_data['Email']
            usertype=form.cleaned_data['usertype']
            password=form.cleaned_data['Password']
            confirmpassword=form.cleaned_data['ConfirmPassword']

            user=Register.objects.filter(Email=email).exists()
            if user:
                messages.warning(request,'Email Alredy exist')
                return redirect('/login_2')
            elif password!=confirmpassword:
                messages.warning(request,'Password Mismatch')
            else:
                tab=Register(Name=name,Age=age,place=place,Email=email,Password=password,usertype=usertype)
                tab.save()

                

                
    else:
        form=RegisterForm() 
    return render(request,'registration.html',{'form':form})
    
def login_2(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['Email']
            password=form.cleaned_data['Password']
            print(email)
            print(password)
            try:
                user=Register.objects.get(Email=email)
                print(user.Email)
                if not user:
                    messages.warning(request,'Email does not exist')
                    return redirect('/login_2')
                elif password!=user.Password:
                    messages.warning(request,'Password Incorrect')
                    return redirect('/login_2')
                else:
                    messages.success(request,'')
                    return redirect('/home/%s' % user.id)
            except:
                messages.warning(request,'Email or Password incorrect')
                return redirect('/login_2')
    else:
        form=LoginForm()
    return render(request,'login_2.html',{'form':form})

def home(request,id):
        user=Register.objects.get(id=id)
        return render(request,'home.html',{'user':user})

def about(request,id):
    return render(request,'about.html',{'id':id})

def  service(request,id):
    return render(request,'service.html',{'id':id})

def  contact(request,id):
        return render(request,'contact.html',{'id':id})


def team(request,id):
    return render(request,'team.html',{'id':id})





def index(request,id):
        return render(request,'index.html',{'id':id})




def logout_view(request):
    logout(request)
    return redirect('login')  



def delete(request,id):
    user=Register.objects.get(id=id)
    user.delete()
    messages.success(request,'SUCCESS')
    return redirect('/')

def changepassword(request,id):
    user=Register.objects.get(id=id)
    if request.method=='POST':
        form=ChangepasswordForm(request.POST or None)
        if form.is_valid():
            oldpassword=form.cleaned_data['OldPassword']
            newpassword=form.cleaned_data['NewPassword']
            confirmpassword=form.cleaned_data['ConfirmPassword']

            if oldpassword!= user.Password:
                messages.warning(request,"incorrect")
                return redirect('/changepassword/%s' % user.id)
            elif oldpassword==newpassword: 
                messages.warning(request, "password similar")
                return redirect('/changepassword/%s' % user.id)
            elif newpassword!=confirmpassword:
                messages.warning(request,"password new")
                return redirect('/changepassword/%s'% user.id)
            else:
                user.Password=newpassword
                user.save()
                messages.success(request,"change success")
    else:
        form=ChangepasswordForm()
        return render(request,'changepassword.html',{'user':user, 'form':form})

def logout_view(request,id):
    logouts(request)
    messages.success(request,'SUCCESS',{id:'id'})
    return redirect('/')



def login(request):
    if request.method=='POST':
            email=request.POST['email']
            password=request.POST['pswd']
           
            try:
                user=Register.objects.get(Email=email)
                print(user.Email)
                if not user:
                    messages.warning(request,'Email does not exist')
                    return redirect('registration/')
                elif password!=user.Password:
                    messages.warning(request,'Password Incorrect')
                    return redirect('/')
                else:
                    messages.success(request,'Success')
                if user.usertype=='doctor':
                    return redirect('doctorindex/%s'% user.id) 
                else:
                    return redirect('index/%s'% user.id)
            except:
                messages.warning(request,'Email or Password incorrect')
                return redirect('/')
                    
    else:
       return render(request,'login.html')
    
def doctorindex(request,id):
    return render(request,'doctorindex.html',{'id':id})

def view_disease(request,id):
    return render(request,'view_disease.html',{'id':id})

def view_appointment(request,id):
    all_appointment = Appointment.objects.all()
    
        # Fetch pending appointments
    pending_appointments = Appointment.objects.filter(status='Pending')
    
    # Fetch viewed appointments
    viewed_appointments = Appointment.objects.filter(status='Viewed')

    # Fetch completed appointments
    completed_appointments = Appointment.objects.filter(status='Completed')

    context = {
        'pending_appointments': pending_appointments,
        'viewed_appointments': viewed_appointments,
        'completed_appointments': completed_appointments,
        'all_appointment':all_appointment,
        'id': id,
    }
    
    return render(request,'view_appointment.html',context)

def schedule(request,id):
    return render(request,'schedule.html',{'id':id})





def predict(request, id):
    if request.method == 'POST':
        form = PredictionForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data, including the uploaded image
            form.save()
            return redirect('prediction_success')  # Redirect to success page or another view
    else:
        # Handle GET request, render the form
        form = PredictionForm(initial={'dr_id': id})  # Initialize the form with 'id' passed from the URL

    context = {
        'form': form,
        'id': id,
    }
    return render(request, 'predict.html', context)


# def appointment1(request,id):
#     if request.method=='POST':
#             name=request.POST['Name']

#             dr_id=request.POST['dr_id']
#             name=request.POST['Name']
#             email=request.POST['Email']
#             age=request.POST['Age']
#             place=request.POST['place']
#             phone=request.POST['Phone']
#             date=request.POST['Date']                     
#             prediction=request.POST['predict']
#             # time=request.POST['time']   
#             sql = Appointment(dr_id=dr_id,Name=name,Email=email,Age=age,place=place,Phone=phone,Date=date,predict=prediction)   
#             sql.save()
#     else:
       
#         drs = Register.objects.filter(usertype="doctor")
#         return render(request,'appointment.html',{'id':id,'drs':drs})
def appointment1(request, id):
    if request.method == 'POST':
        # Retrieve data from POST request
        name = request.POST.get('Name')
        dr_id = request.POST.get('dr_id')
        email = request.POST.get('Email')
        age = request.POST.get('Age')
        place = request.POST.get('place')
        phone = request.POST.get('Phone')
        date = request.POST.get('Date')
        
        prediction = request.FILES.get('predict')  # Assuming 'predict' is an ImageField

        # Create Appointment object and save to database
        appointment = Appointment(
            dr_id=dr_id,
            Name=name,
            Email=email,
            Age=age,
            place=place,
            Phone=phone,
            Date=date,
            predict=prediction  # Assuming 'predict' is an ImageField
        )
        appointment.save()

        subject = 'Appointment booked'
        message = f'Hi {name}, ypur appointment are succes fully booked .'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail( subject, message, email_from, recipient_list )







        return render(request, 'appointment.html', {'id': id})
        

    else:
        # Fetch list of doctors for appointment form
        drs = Register.objects.filter(usertype="doctor")
        return render(request, 'appointment.html', {'id': id, 'drs': drs})

# views.py




@csrf_exempt
def complete_appointment(request, appointment_id):
    if request.method == 'POST':
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.status = 'Completed'
            appointment.save()
            return JsonResponse({'status': 'success'})
        except Appointment.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Appointment not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def prediction_images(request):
    appointments = Appointment.objects.all() 
     # Retrieve all appointments with prediction
    return render(request, 'prediction_images.html', {'appointments': appointments})


def chat_dr(request, id):
    return render(request, 'chat_dr.html', {'id': id})


def chat_pt(request, id):
    return render(request, 'chat_pt.html', {'id': id})


@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    data = json.loads(request.body)
    message_content = data.get('message', '')
    new_message = Message(sender='user', content=message_content)
    new_message.save()
    # Simulate a doctor's response
    doctor_response = "Doctor's response to: " + message_content
    Message.objects.create(sender='doctor', content=doctor_response)
    return JsonResponse({'message': doctor_response})

def receive_messages(request):
    messages = Message.objects.all().order_by('timestamp')
    message_list = [{'sender': msg.sender, 'content': msg.content} for msg in messages]
    return JsonResponse(message_list, safe=False)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import  Patient,Message
from django.db.models import Q

@login_required
def chat_view(request, patient_id):
    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        return redirect('home')  # Redirect to a safe page if the patient doesn't exist

    current_user = request.user
    current_patient = Patient.objects.get(user=current_user)
    
    # Get messages exchanged between current patient and the other patient
    messages = Message.objects.filter(
        (Q(sender=current_patient) & Q(receiver=patient)) |
        (Q(sender=patient) & Q(receiver=current_patient))
    ).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(sender=current_patient, receiver=patient, content=content)
        return redirect('chat', patient_id=patient_id)

    context = {
        'messages': messages,
        'patient': patient,
    }
    return render(request, 'chat_dr/chat_pt.html', context)






def appointment_success(request,id):
    return render(request, 'appointment_success.html', {'id': id})
