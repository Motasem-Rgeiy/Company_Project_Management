from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def is_valid_email(email_address):
    
    try:
        validate_email(email_address)
        return True
    
    except ValidationError:
        return False



def process_emails(email_list, chunk_size):

    for i in range(0, len(email_list), chunk_size):
        if len(email_list) <= i + chunk_size:
            yield email_list[i : len(email_list)]
        else:
            yield email_list[i : i+chunk_size]