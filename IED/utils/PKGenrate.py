import random,string
from datetime import datetime


def generate_resource_key(title='XXRE'):
    return title + datetime.now().strftime('%y%m%d%H%M%S') + ''.join(random.sample(string.ascii_letters + string.digits, 4))


def generate_user_key(title='XXUS'):
    return title + datetime.now().strftime('%y%m%d%H%M%S') + ''.join(random.sample(string.ascii_letters + string.digits, 4))