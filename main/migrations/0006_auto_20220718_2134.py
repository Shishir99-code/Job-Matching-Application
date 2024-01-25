# Generated by Django 3.1.4 on 2022-07-19 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20220718_2134'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', models.FileField(upload_to='resume/pdfs/')),
            ],
        ),
        migrations.AlterField(
            model_name='mentoration',
            name='State',
            field=models.CharField(choices=[(' #Enter State Full  ', ' #Enter State Full  '), ('Alabama', 'Alabama'), ('Alaska', 'Alaska'), ('American Samoa', 'American Samoa'), ('Arizona', 'Arizona'), ('Arkansas', 'Arkansas'), ('California', 'California'), ('Colorado', 'Colorado'), ('Connecticut', 'Connecticut'), ('Delaware', 'Delaware'), ('Federated States of Micronesia', 'Federated States of Micronesia'), ('Florida', 'Florida'), ('Georgia', 'Georgia'), ('Guam', 'Guam'), ('Hawaii', 'Hawaii'), ('Idaho', 'Idaho'), ('Illinois', 'Illinois'), ('Indiana', 'Indiana'), ('Iowa', 'Iowa'), ('Kansas', 'Kansas'), ('Kentucky', 'Kentucky'), ('Louisiana', 'Louisiana'), ('Maine', 'Maine'), ('Marshall Islands', 'Marshall Islands'), ('Maryland', 'Maryland'), ('Massachusetts', 'Massachusetts'), ('Michigan', 'Michigan'), ('Minnesota', 'Minnesota'), ('Mississippi', 'Mississippi'), ('Missouri', 'Missouri'), ('Montana', 'Montana'), ('Nebraska', 'Nebraska'), ('Nevada', 'Nevada'), ('New Hampshire', 'New Hampshire'), ('New Jersey', 'New Jersey'), ('New Mexico', 'New Mexico'), ('New York', 'New York'), ('North Carolina', 'North Carolina'), ('North Dakota', 'North Dakota'), ('Northern Mariana Islands', 'Northern Mariana Islands'), ('Ohio', 'Ohio'), ('Oklahoma', 'Oklahoma'), ('Oregon', 'Oregon'), ('Palau', 'Palau'), ('Pennsylvania', 'Pennsylvania'), ('Puerto Rico', 'Puerto Rico'), ('Rhode Island', 'Rhode Island'), ('South Carolina', 'South Carolina'), ('South Dakota', 'South Dakota'), ('Tennessee', 'Tennessee'), ('Texas', 'Texas'), ('US Armed Forces Europe', 'US Armed Forces Europe'), ('US Armed Forces Pacific', 'US Armed Forces Pacific'), ('Utah', 'Utah'), ('Vermont', 'Vermont'), ('Virgin Islands', 'Virgin Islands'), ('Virginia', 'Virginia'), ('Washington', 'Washington'), ('Washington, D.C.', 'Washington, D.C.'), ('West Virginia', 'West Virginia'), ('Wisconsin', 'Wisconsin'), ('Wyoming', 'Wyoming'), (float("nan"), float("nan"))], default='#Enter State', max_length=60),
        ),
    ]
