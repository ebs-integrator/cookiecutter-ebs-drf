import logging

from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)

from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from raven.contrib.django.raven_compat.models import client


class ApiMiddleware(MiddlewareMixin):

    @staticmethod
    def process_exception(request, response):
        client.captureException()

        return JsonResponse({
            'exception': str(response),
            'detail':    _('Something Went Wrong. Please contact support')
        }, status=500)
