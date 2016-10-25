from __future__ import absolute_import

default_app_config = 'ET.apps.EtConfig'

from .celery import app as celery_app
