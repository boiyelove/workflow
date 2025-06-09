import random
import hashlib
from datetime import datetime
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import EmailVerification

def code_generator(codepulse):
    """Generate a unique verification code"""
    code = hashlib.sha1(str(random.random()).encode())
    code.update(codepulse.encode())
    code.update(str(datetime.utcnow()).encode())
    code = code.hexdigest()
    return code

def verify_email(email, actiontype=None, action='/'):
    """Create or get email verification record"""
    defaults = {
        'action': action or '/',
        'actiontype': actiontype or 'VERIFICATION'
    }
    
    # Check if this is a test email that should be auto-verified
    auto_verify = False
    if hasattr(settings, 'AUTO_VERIFY_TEST_USERS') and settings.AUTO_VERIFY_TEST_USERS:
        if hasattr(settings, 'TEST_EMAIL_DOMAIN') and settings.TEST_EMAIL_DOMAIN:
            if email.endswith(f"-test@{settings.TEST_EMAIL_DOMAIN}"):
                defaults['confirmed'] = True
                auto_verify = True
    
    emailverificationObj, created = EmailVerification.objects.get_or_create(
        email=email,
        defaults=defaults
    )
    
    if created:
        base, domain = str(email).split("@")
        code_exists = True
        while code_exists:
            verification_key = code_generator(base)[:10]
            code_exists = EmailVerification.objects.filter(slug=verification_key).exists()
        
        emailverificationObj.slug = verification_key
        if action:
            emailverificationObj.action = action
        if actiontype:
            emailverificationObj.actiontype = actiontype
        emailverificationObj.save()
        
        # Only send email if not auto-verified
        if not auto_verify:
            emailverificationObj.send_activation_email()
    
    return emailverificationObj

def email_password(user, password):
    """Send password email to user"""
    message = render_to_string("accounts/newsletter/password_email.txt", {
        "website": settings.SITE_NAME,
        "password": password,
        'user': user,
    })
    subject = "New Padlock Information"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

def is_test_email(email):
    """Check if an email is a test email based on settings"""
    if hasattr(settings, 'TEST_EMAIL_DOMAIN') and settings.TEST_EMAIL_DOMAIN:
        return email.endswith(f"-test@{settings.TEST_EMAIL_DOMAIN}")
    return False
