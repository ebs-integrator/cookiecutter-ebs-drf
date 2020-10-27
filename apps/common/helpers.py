import binascii
import hashlib
import logging
import os
import random

import requests
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext as _
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.exceptions import ValidationError

from apps.common.constants import *
from apps.common.permissions import AllowOnlyIP

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Enjoy",
    ),
    validators=['ssv'],
    public=True,
    permission_classes=(AllowOnlyIP,)
)

logger = logging.getLogger(__name__)


def compute_hash(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def send_emails(response, emails, **kwargs):
    message = response['htmlContent']
    for key, value in kwargs.items():
        message = message.replace('{{%s}}' % key, value)
    send_mail(
        response['subject'],
        'email_plaintext_message',
        'info@eurasiaprecept.org',
        emails,
        html_message=message,
    )


def send_sms(phone_number, msg):
    params = {
        'username': settings.SMS_USERNAME,
        'userid': settings.SMS_USERID,
        'handle': settings.SMS_HANDLE,
        'from': settings.SMS_FROM,
        'msg': msg,
        'to': phone_number,
    }
    response = requests.get('https://api.budgetsms.net/sendsms/', params=params)
    print(response)


def get_sms_message(user, sms_message_type, **kwargs):
    last_name = user.last_name
    session_name = kwargs.get('session_name', '')
    start_end_date = kwargs.get('start_end_date', '')
    session_registration_link = kwargs.get('session_registration_link', '')
    city = kwargs.get('city', '')
    link = kwargs.get('link', '')
    faculty = kwargs.get('faculty', '')
    issue_description = kwargs.get('issue_description', '')
    grade_outstandings = kwargs.get('grade_outstandings', '')
    event_list = kwargs.get('event_list', '')
    grade_type = kwargs.get('grade_type', '')
    course_name = kwargs.get('course_name', '')
    grade_outstanding = kwargs.get('grade_outstanding', '')
    professor_name = kwargs.get('professor_name', '')
    days = kwargs.get('days', '')
    session_link = kwargs.get('session_link', '')
    sms_message = {
        SESSION_INVITATION_ST: _(
            f'Dragă {last_name} Ești invitat să participi la sesiunea {session_name} a facultății {faculty} din {start_end_date}, '
            f'care se va petrece în {city}. Dacă dorești să te înregistrezi la această sesiune, folosește butonul de mai jos: '
            f'{session_registration_link}.'
        ),
        SESSION_REGISTER: _('SESSION_REGISTER'),
        SESSION_DATE_MODIFIED: _(
            f'Dragă {last_name}, Au apărut unele modificări cu privire la organizarea sesiunii {session_name} din {start_end_date}. '
            f'Informația nouă o poți vizualiza mai jos sau urmând linkul spre cabinetul tău. \n {link}'),
        SESSION_REMINDER: _(
            f'Dragă {last_name}, Îți amintim că sesiunea {session_name} începe în {days}. Detaliile sesiunii le găsești mai jos: '
            f'{session_link}'),
        ISSUE_CONFIRMATION: _(f'Dragă {last_name}, Cererea ta a fost trimisă cu succes! \n {issue_description}'),
        MONTHLY_NEWSLETTER: _(f'{event_list}'),
        OUTSTANDING_REMINDER: _(
            f'Dragă {last_name} Îți amintim că deții restanțe pentru {session_name} la nota {grade_type}. Te rugăm să prezinți '
            f'{grade_outstanding} spre verificare profesorului {professor_name}.'),
        MANUAL_REMINDER: _(
            f'Dragă {last_name}, Îți amintim că deții restanțe pentru {session_name} la nota {grade_type}. Te rugăm să prezinți '
            f'{grade_outstandings} spre verificare profesorului {professor_name}.'),
        SESSION_INVITATION_PROF: _(
            f'Dragă {last_name}, Ești invitat să predai sesiunea {session_name}, cursul {course_name}, în {city}. Te rugăm să folosești '
            f'linkul de mai jos pentru a vizualiza detaliile sesiunii și pentru a răspunde invitației. \n {link}'),
        EVENT_INVITATION_PROF: _('EVENT_INVITATION_PROF'),
        SESSION_INVITATION_ACCEPT_PROF: _('SESSION_INVITATION_ACCEPT_PROF'),
        SESSION_REMINDER_6_MONTH: _('SESSION_REMINDER_6_MONTH'),
        REQUEST_SESSION_ACCEPTED: _('REQUEST_SESSION_ACCEPTED'),
        EVENT_INVITATION_CORD: _('EVENT_INVITATION_CORD'),
        REQUEST_SESSION_ADMIN: _('REQUEST_SESSION_ADMIN'),
        ISSUE_RECEIVE: _('ISSUE_RECEIVE'),
        SESSION_WITHOUT_PROF: _('SESSION_WITHOUT_PROF'),
    }
    return sms_message[sms_message_type]


def generate_token(min_length=10, max_length=50):
    """ generates a pseudo random code using os.urandom and binascii.hexlify """
    # determine the length based on min_length and max_length
    length = random.randint(min_length, max_length)

    # generate the token using os.urandom and hexlify
    return binascii.hexlify(
        os.urandom(max_length)
    ).decode()[0:length]


def generate_code(length=6):
    range_start = 10 ** (length - 1)
    range_end = (10 ** length) - 1
    return random.randint(range_start, range_end)


def validate_dates(attrs):
    if attrs.get('end_date', None) and attrs['end_date'] < timezone.now():
        raise ValidationError({"end_date": "Start date can not be in past"})
    if attrs.get('start_date', None) and attrs['start_date'] < timezone.now():
        raise ValidationError({"start_date": "Start date can not be in past"})
    if attrs.get('end_date', None) and attrs.get('start_date', None) and attrs['end_date'] < attrs['start_date']:
        raise ValidationError({"end_date": "End date can not be lower than start date"})
    if attrs.get('end_date', None) and attrs.get('start_date', None) and attrs['start_date'] > attrs['end_date']:
        raise ValidationError({"end_date": "Start date can not be higher than end date"})
