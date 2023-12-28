import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','moontag_project.settings')
import django
django.setup()
from moontag_app.models import AccessRecord,Topic,Webpage
import random
from faker import Faker

fake = Faker()

topics = ['Search','Social','Sport']

def add_topic ():
    t = Topic.objects.get_or_create(top_name = random.choice(topics))[0]
    t.save()
    return t

def population (integer):
    for i in range(integer):
        top = add_topic()
        fake_url = fake.url()
        fake_date = fake.date()
        fake_name = fake.company()
        webpg = Webpage.objects.get_or_create(topic = top,url = fake_url,name = fake_name)[0]
        acc_rec = AccessRecord.objects.get_or_create(name = webpg,date = fake_date)

def main ():
    if __name__ == '__main__':
        print('populating script!')
        population(10)
        print('population complete')

main()