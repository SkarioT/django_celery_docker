from django.test import TestCase

# Create your tests here.

#_________celery____
from datetime import datetime, timedelta
from django_celery_beat.models import PeriodicTask, IntervalSchedule,ClockedSchedule
from . import tasks
import json
#------------------------

