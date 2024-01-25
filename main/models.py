from distutils.command.upload import upload
from django.db import models
from datetime import datetime
import pandas as pd

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




# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=1000)

class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=100)
    room = models.CharField(max_length=100)

class Registration(models.Model):
    email = models.EmailField(max_length=60)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    University = models.CharField(max_length=60)
    Years_of_Experience = models.CharField(max_length=60, choices=YEARS, default='1-2')
    Company = models.CharField(max_length=100)
    Position = models.CharField(max_length=100, choices=POSITION, default='Position')
    Department = models.CharField(max_length=60)
    State = models.CharField(max_length=60, choices=STATE, default='#Enter State')
    City = models.CharField(max_length=60, choices=CITIES, default='#Enter City')
    pdf = models.FileField(upload_to='resumes/')


    def __str__(self):
        return self.email

    
class ResumeText(models.Model):
    username = models.CharField(max_length=100)
    resume_text = models.CharField(max_length=100000)

class MatchForm(models.Model):
    job_path = models.CharField(max_length=100, choices=POSITION, default='Position')
    company_name = models.CharField(max_length=100)

class login(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=60)