from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .helper import is_valid_email, process_emails
import time
from django.core.mail import send_mail
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.urls import reverse
from django.conf import settings
from . import models, forms
from django.core.cache import cache
from accounts.models import UserRoles
from .tasks import  get_emails
import json
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import gettext_lazy as _

# Create your views here.


#unsubscribed feature

signer = TimestampSigner()


@require_POST
@csrf_exempt
def subscribe_view(request):
  
    email_address = json.loads(request.body).get('user_email')

    if not is_valid_email(email_address):

        print('Invalid email!')
        return JsonResponse({}, status=500)

    
    subscriber = models.Subscriber.objects.filter(email=email_address).last()
    if not subscriber:
         models.Subscriber.objects.create(email=email_address)

    elif subscriber.is_active:
         return JsonResponse({'message':'This email is already exist!'})
         
         
    token = signer.sign(email_address)

    confirm_url = request.build_absolute_uri(
        reverse('email_confirm', kwargs={'token':token})
    )

    send_mail(
        subject='Confirm your newsletter subscription.',
        message=f'Please, confirm your identity to subscribe to our newsletter before 24 by click {confirm_url} before 24 hours',
        from_email= 'motasem@example.com',
        recipient_list=[email_address],
    )
        
    return JsonResponse({'status':'success'})




#confirm the email and create a new subscriber record
@require_GET
def email_confirm(request, token):

    if cache.get(token):
         return HttpResponse('Invalid Link')
    
    try:
        email_address = signer.unsign(token, max_age=86400) #A day

        subscriber = models.Subscriber.objects.filter(email=email_address).last()

        if not subscriber:
             return HttpResponse('Not found!')

        if subscriber.is_active:
             print('Checked by is_active!')
             cache.set(token, True, 86000)
             return HttpResponse('Invalid Link2')
        
        subscriber.is_active = True
        subscriber.save()

        cache.set(token, True, 86000)

        return render(request, 'subscribe/email_confirm_success.html')



    except SignatureExpired as e:
        return  HttpResponse('The email request is expired, try to subscribe again')

    except BadSignature:
            return  HttpResponse('Invalid link, try to subscribe again')





@login_required
@require_GET
@permission_required('newsletter.view_newsletter', raise_exception=True)
def newsletter_list(request):
  
    active_subscribers_count = models.Subscriber.objects.filter(is_active=True).count()
     
    newsletters = models.Newsletter.objects.filter(publisher = request.user)

    form = forms.NewsletterCreateForm()
    context = {
          
              'current_manager': request.user, 
              'total_subscribers':active_subscribers_count,
              'newsletters': newsletters,
              'form': form,
             }
         
         
    return render(request, 'newsletter/newsletter.html', context)
     




#Background Tasks
  #Send emails to all subscribers
  #1 get all subscriber emails from database and put them in Redis
  #2 get 25 emails per task
  #3 celery get 25 emails one at a time, sends them, again and again
@csrf_exempt
@permission_required('newsletter.add_newsletter', raise_exception=True)
def newsletter_operations(request):
     
        form = forms.NewsletterCreateForm(request.POST)
        if form.is_valid():
                
            #Needs JS logic to complete page design
                get_emails.delay(form.cleaned_data['title'], form.cleaned_data['body'])

                models.Newsletter.objects.create(title=form.cleaned_data['title'], 
                                                 body=form.cleaned_data['body'],
                                                 publisher=request.user,
                                                 )
                
                return JsonResponse({'message':_("The email has been sent to all subscribers.")})

    
        error_msg = list(form.errors.values())[0][0]
        return JsonResponse({'message':error_msg})