from django.core.management.base import BaseCommand
from event.models import Event
import datetime
import random


names = ['people','history','way','art','world','information','map','two','family','government','health','system','computer','meat','year','thanks','music','person','reading','method','data','food','understanding','theory','law','bird','literature','problem','software','control','knowledge','power','ability',]

locations = ['New York','Los Angeles','Chicago','Houston','Philadelphia','Phoenix','San Antonio','San Diego','Dallas','San Jose','Austin','Indianapolis','Jacksonville','San Francisco','Columbus','Charlotte','Fort Worth','Detroit','El Paso','Memphis']

categories = ["MUSIC","ART","PARTY","SPORT","BUSINESS"]



def name_generator():
    return " ".join([names[random.randrange(0, len(names))] for i in range(3)])

def category_generator():
    return categories[random.randrange(0, len(categories))]

def location_generator():
    return locations[random.randrange(0, len(locations))]

def is_free():
    index = random.randint(0,1)
    if index == 0:
        return False
    return True

def date_generator():
    year = random.randint(2019, 2025)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return datetime.date(year, month, day)

class Command(BaseCommand):
    help = 'generate random event'

    def handle(self, *args, **options):
        for i in range(50):
            name = name_generator()
            slug = name
            date = date_generator()
            category = category_generator()
            location = location_generator()
            free = is_free()

            event = Event(name=name, slug=slug, date=date, category=category, location=location, free=free)
            event.save()
            
        self.stdout.write(self.style.SUCCESS("event created successfully!"))
