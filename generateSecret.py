import random
import string

def generate_secret_key():
    characters = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(random.choice(characters) for i in range(50))
    return secret_key

print(generate_secret_key())
