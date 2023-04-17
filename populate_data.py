import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VWR.settings')

import django
django.setup()

#Fake Pop Script
from draft.models import User
from faker import Faker

fakegen = Faker()
def populate(N=5):
    for entry in range(N):
        fake_first_name = fakegen.first_name()
        fake_last_name = fakegen.last_name()
        fake_email = fakegen.unique.email()
        usr = User.objects.get_or_create(first_name=fake_first_name ,last_name=fake_last_name ,email=fake_email)


if __name__ =='__main__':
    print('Populating script!')
    populate(10)
    print('Populating complete!')

    
