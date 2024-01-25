from cgitb import html
import email
from django.shortcuts import redirect, render
from requests import request
from .forms import RegistrationForm, login_form, match_form
import os
from django.contrib.auth import login, logout, authenticate
from .models import MatchForm, Room, Message, Registration, ResumeText
from django.http import HttpResponse, JsonResponse
from main.resume_matchmaking_utils import *
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
import random
import string
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Create your views here.
def home(request):
    form = login_form()
    if request.method == 'POST':
        form = login_form(request.POST)

        if form.is_valid():
                form.save()
                login_email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                request.session['username' ] = login_email
                request.session['password'] = password
                filtered_user = Registration.objects.filter(email=login_email)
                user_auth = Registration.objects.filter(email=login_email).count()
                pwd_auth = Registration.objects.filter(password=password).count()
                if user_auth >= 1 and pwd_auth >= 1:
                    print(filtered_user)
                    return redirect('/match')
                else:
                    messages.error(request, 'Invalid login information! | Check your username and password.')
                    login_form()

    return render(request, 'main/home.html', {"form": form})

def about(request):
    return render(request, 'registration/about.html')

def sign_up(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            pdf_name = request.FILES['pdf']._name
            print(os.getcwd())
            pdf_path ='resumes/'+ pdf_name
            resume_string = convert_pdf_to_txt(pdf_path)
            clean_resume_string = clean_text(resume_string, remove_punctuation = True,
            remove_stopwords = True, remove_num = True)
            username_value = form.data['email']
            resume_text = ResumeText(username=username_value, 
                                        resume_text=clean_resume_string)
            resume_text.save()
            return redirect('/home')
        else:
            RegistrationForm()
    context = {'form1': form}
    return render(request, 'registration/sign_up.html', context)

def chat(request):
    return render(request, 'chat/room.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'chat/chat.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })


def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})


def matchForm(request):
    form = match_form()
    if request.method == 'POST':
        form = match_form(request.POST)
        if form.is_valid():
            form.save()
            job_path = form.cleaned_data['job_path']
            company_name = form.cleaned_data['company_name']
            test = Registration.objects
            filter_one = Registration.objects.filter(Position=job_path)
            filter_two = filter_one.filter(Company=company_name)
            login_email = request.session['username'] 
            email_potential_matches =list(filter_two.values_list('email'))
            print(email_potential_matches)
            if len(email_potential_matches) == 0:
                messages.error(request, 'No Matches Found')
                match_form()
                return redirect('/match')
            elif len(email_potential_matches) > 1:
                user_clean_resume = list(ResumeText.objects.filter(username=login_email).values_list('resume_text'))[0][0]
                list_of_scores = []
                for x in email_potential_matches:
                    potential_email = x[0]
                    clean_resume = list(ResumeText.objects.filter(username=potential_email).values_list('resume_text'))[0][0]
                    score = calculate_jaccard(clean_resume.split(' '), user_clean_resume.split(' '))
                    list_of_scores.append(score)
                max_value = max(list_of_scores)
                index = list_of_scores.index(max_value)
                match_email = email_potential_matches[index][0]
            else:
                match_email = email_potential_matches[0][0]

            characters = string.ascii_uppercase
            room_code = ''.join(random.choice(characters) for i in range(5))
            API_key = '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'
            user_message = Mail(from_email='aetheranalyticsgroup@gmail.com',
                                to_emails=login_email,
                                subject=f'Chat Room Code for {job_path} at {company_name}',
                                plain_text_content=f'Your Room Code is {room_code}',
                                html_content=f'Your Room Code is {room_code}')
                                
            try:
                sg = SendGridAPIClient(API_key)
                response = sg.send(user_message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e.message)

            match_message = Mail(from_email='aetheranalyticsgroup@gmail.com',
                                to_emails=match_email,
                                subject=f'Chat Room Invite Code for {job_path} at {company_name}',
                                plain_text_content=f'Someone is looking for job advice. Join your room using - {room_code}',
                                html_content=f'Someone is looking for job advice. Join your room using - {room_code}')
            try:
                sg = SendGridAPIClient(API_key)
                response = sg.send(match_message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e.message)
            return redirect('/homeroom')
        else: 
            form = match_form()

    
    return render(request, 'registration/MatchForm.html', {"form": form})
                
            


    


