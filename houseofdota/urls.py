"""houseofdota URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework import routers
from django.contrib.auth.decorators import login_required

from app.api.match_viewset import MatchViewset
from app.api.statistics_view import *
from app.api.nn_training_result_view import NnTrainingResultViewset
from app.api.heroes_view import *
from app.api.recommendation_view import *
from authentication.views import *

router = routers.SimpleRouter()
router.register(r'matches', MatchViewset)
router.register(r'nn_results', NnTrainingResultViewset)

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^admin/', admin.site.urls),
    url(r'^heroes/$', heroes_list),
    url(r'^nn_performance/$', TemplateView.as_view(template_name='nn_performance.html')),
    url(r'^recommendation/$', TemplateView.as_view(template_name='recommendation.html')),
    url(r'^recommendation/bundles/$', hero_recommendations_for_bundle),
    url(r'^recommendation/counters/$', counter_recommendations_for_hero),
    url(r'^statistics/$', TemplateView.as_view(template_name='statistics.html')),
    url(r'^statistics/heroes/$', heroes_statistics),
    url(r'^oauth/', include('social_django.urls')),
    url(r'^logout', login_required(LogoutView.as_view(), login_url='/'), name='logout')
]

urlpatterns += router.urls
urlpatterns += staticfiles_urlpatterns()
