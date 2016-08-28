import mock

from django.test import TestCase
from mock import patch

class StatisticsServiceTest(TestCase):
    fixtures = ['matches.json']
