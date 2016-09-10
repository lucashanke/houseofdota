import mock

from django.test import TestCase
from mock import patch
from app.business.recommendation_business import *

class NNRecommendationTest(TestCase):

    def test_recommend(self):
        self.assertEqual(NNRecommendation(None).recommend(None,None,None), None)
