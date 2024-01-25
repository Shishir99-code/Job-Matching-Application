from email.policy import default
from pyexpat import model
from selectors import DefaultSelector
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from numpy import require
import pandas as pd
import os
from requests import request
from .models import MatchForm, Registration, login
from django.forms import ModelForm

         
CHOICES = [
    ('Limited', 'LIMITED'),
    ('Moderate', 'MODERATE'),
    ('Free', 'FREE'),
    ]

YEARS = [
    ('Years', 'Years'),
    ('0-1', '0-1'),
    ('1-2', '1-2'),
    ('2-3', '2-3'),
    ('3-4', '3-4'),
    ('4-5', '4-5'),
    ('5+', '5+'),
]

df_location = pd.read_csv("Data/us_cities_states_counties.csv", sep='|')
df_company = pd.read_csv("Data/nasdaq-listed.csv")
df_position = pd.read_csv("Data/job-phrase-list.csv")


print("here")

# Dictionaries for all states and cities
unique_positions = pd.unique(df_position['Position'])
positions_dictionary = list(map(lambda x, y:(x,y), unique_positions, unique_positions))
unique_states = pd.unique(df_location['State full'].sort_values())
states_dictionary = list(map(lambda x, y:(x,y), unique_states, unique_states))
unique_cities = pd.unique(df_location['City'].sort_values())
cities_dictionary = list(map(lambda x, y:(x,y), unique_cities, unique_cities))

unique_company = pd.unique(df_company['Company Name'].sort_values())
company_dictionary = list(map(lambda x, y:(x,y), unique_company, unique_company))



COMPANY = company_dictionary
STATE = states_dictionary
CITIES = cities_dictionary
POSITION = positions_dictionary

class RegistrationForm(ModelForm):
    first_name = forms.CharField(max_length=64, required=True)
    last_name = forms.CharField(max_length=64, required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    University = forms.CharField(required=True)
    Position = forms.ChoiceField(choices=POSITION, required=False)
    Years_of_Experience = forms.ChoiceField(choices=YEARS, required=False)
    Company = forms.CharField(max_length=60, required=False)
    Department = forms.CharField(required=False)
    State = forms.ChoiceField(choices=STATE, required=False)
    City = forms.ChoiceField(choices=CITIES, required=False)
    

    class Meta:
        model = Registration
        fields = '__all__'

class match_form(ModelForm):

    class Meta:
        model = MatchForm
        fields = '__all__'

class login_form(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'style':'max-width: 24em'}))
    email = forms.EmailField(
    max_length=64,
    widget=forms.TextInput(attrs={'style':'max-width: 24em'}),
    required=True)
    

    class Meta:
        model = login
        fields = '__all__'
