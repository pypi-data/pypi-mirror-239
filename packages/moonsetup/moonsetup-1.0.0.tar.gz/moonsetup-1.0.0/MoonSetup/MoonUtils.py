import random
import string

def generaterandomstring():
    return ''.join(random.choice(string.ascii_letters) for i in range(10))