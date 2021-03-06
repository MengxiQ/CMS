"""
WSGI config for CMS project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from CMS.apps.tools.testTools import pingTimer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CMS.settings')

application = get_wsgi_application()


# 定时任务
pingTimer(1)